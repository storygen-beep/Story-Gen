import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:path/path.dart' as p;

import '../data/library_store.dart';
import '../data/models.dart';

/// Keeps a copy of every game's browser storage outside the WebView.
///
/// SugarCube and most HTML games save into localStorage. WebView storage can
/// be wiped (iOS evicts it under storage pressure, a reinstall drops it, a
/// changed origin hides it). So a script injected before the game's own code
/// mirrors every localStorage write to Flutter, and Flutter keeps it in
/// `saves/<id>/current.json` plus timestamped backups.
///
/// On launch the same script puts our copy back for any key the WebView has
/// lost, which is what makes saves survive.
class SaveStore {
  SaveStore(this.paths);
  final AppPaths paths;

  static const maxBackups = 10;

  /// Minimum gap between automatic backups. A game writes storage on every
  /// passage; a backup per write would push real history out in minutes.
  static const autoBackupGap = Duration(minutes: 2);

  final _current = <String, Map<String, String>>{};

  /// Every key a game has ever written. All games share one origin, so this
  /// is how a restore knows which keys are this game's to remove.
  final _owned = <String, Set<String>>{};
  final _dirty = <String, Timer>{};
  final _lastAuto = <String, DateTime>{};

  String _currentFile(String id) => p.join(paths.savesDir(id), 'current.json');
  String _backupDir(String id) => p.join(paths.savesDir(id), 'backups');
  String _ownedFile(String id) => p.join(paths.savesDir(id), 'keys.json');

  Future<Set<String>> owned(String gameId) async {
    final cached = _owned[gameId];
    if (cached != null) return cached;
    final f = File(_ownedFile(gameId));
    final keys = <String>{};
    if (await f.exists()) {
      try {
        keys.addAll((jsonDecode(await f.readAsString()) as List).cast<String>());
      } on FormatException {
        // Rebuilt from current.json below.
      }
    }
    keys.addAll((await current(gameId)).keys);
    return _owned[gameId] = keys;
  }

  Future<Map<String, String>> current(String gameId) async {
    final cached = _current[gameId];
    if (cached != null) return cached;
    final f = File(_currentFile(gameId));
    final map = <String, String>{};
    if (await f.exists()) {
      try {
        map.addAll((jsonDecode(await f.readAsString()) as Map).cast<String, String>());
      } on FormatException {
        // Torn write. The newest backup is the fallback.
        final b = await backups(gameId);
        if (b.isNotEmpty) map.addAll(await _readBackup(gameId, b.first.id));
      }
    }
    return _current[gameId] = map;
  }

  /// Called from the WebView for every localStorage write while [gameId] runs.
  Future<void> onStorageEvent(String gameId, String op, String? key, String? value) async {
    final map = await current(gameId);
    switch (op) {
      case 'set':
        if (key == null || value == null || map[key] == value) return;
        map[key] = value;
        (await owned(gameId)).add(key);
      case 'remove':
        if (key == null || map.remove(key) == null) return;
      case 'clear':
        if (map.isEmpty) return;
        map.clear();
      default:
        return;
    }
    _dirty[gameId]?.cancel();
    _dirty[gameId] = Timer(const Duration(milliseconds: 600), () => _flush(gameId));
  }

  Future<void> _flush(String gameId) async {
    _dirty.remove(gameId)?.cancel();
    final map = _current[gameId];
    if (map == null) return;
    await Directory(paths.savesDir(gameId)).create(recursive: true);
    final tmp = File('${_currentFile(gameId)}.tmp');
    await tmp.writeAsString(jsonEncode(map));
    await tmp.rename(_currentFile(gameId));
    final keys = await owned(gameId);
    keys.addAll(map.keys);
    await File(_ownedFile(gameId)).writeAsString(jsonEncode(keys.toList()));

    final last = _lastAuto[gameId];
    if (last == null || DateTime.now().difference(last) >= autoBackupGap) {
      await backupNow(gameId, reason: 'auto');
    }
  }

  /// Flush pending writes; called when the player leaves a game.
  Future<void> flushAll() async {
    for (final id in _dirty.keys.toList()) {
      await _flush(id);
    }
  }

  Future<SaveBackup?> backupNow(String gameId, {required String reason}) async {
    final map = await current(gameId);
    if (map.isEmpty) return null;
    final dir = Directory(_backupDir(gameId));
    await dir.create(recursive: true);
    final now = DateTime.now();
    final id = '${now.millisecondsSinceEpoch}_$reason';
    final body = jsonEncode(map);
    await File(p.join(dir.path, '$id.json')).writeAsString(body);
    _lastAuto[gameId] = now;
    await _prune(gameId);
    return SaveBackup(id: id, createdAt: now, sizeBytes: body.length, keyCount: map.length, reason: reason);
  }

  Future<List<SaveBackup>> backups(String gameId) async {
    final dir = Directory(_backupDir(gameId));
    if (!await dir.exists()) return [];
    final out = <SaveBackup>[];
    await for (final f in dir.list()) {
      if (f is! File || !f.path.endsWith('.json')) continue;
      final stem = p.basenameWithoutExtension(f.path);
      final parts = stem.split('_');
      final ms = int.tryParse(parts.first);
      if (ms == null) continue;
      final len = await f.length();
      out.add(SaveBackup(
        id: stem,
        createdAt: DateTime.fromMillisecondsSinceEpoch(ms),
        sizeBytes: len,
        keyCount: -1,
        reason: parts.length > 1 ? parts.sublist(1).join('_') : 'auto',
      ));
    }
    out.sort((a, b) => b.createdAt.compareTo(a.createdAt));
    return out;
  }

  Future<void> _prune(String gameId) async {
    final all = await backups(gameId);
    for (final b in all.skip(maxBackups)) {
      await File(p.join(_backupDir(gameId), '${b.id}.json')).delete();
    }
  }

  Future<Map<String, String>> _readBackup(String gameId, String backupId) async =>
      (jsonDecode(await File(p.join(_backupDir(gameId), '$backupId.json')).readAsString()) as Map).cast<String, String>();

  /// Makes [backupId] the game's storage. The current state is backed up
  /// first, so a restore can itself be undone. Takes effect the next time the
  /// game opens (the restore script overwrites, see [injectionScript]).
  Future<void> restore(String gameId, String backupId) async {
    await backupNow(gameId, reason: 'before-restore');
    final data = await _readBackup(gameId, backupId);
    _current[gameId] = Map.of(data);
    _pendingForce.add(gameId);
    await _flush(gameId);
  }

  final _pendingForce = <String>{};

  /// One file the player can keep or move to another device.
  Future<List<int>> exportBytes(Game game) async => utf8.encode(jsonEncode({
        'format': 'folio-saves',
        'version': 1,
        'game': {'title': game.title, 'ifid': game.ifid, 'version': game.version},
        'exportedAt': DateTime.now().toIso8601String(),
        'storage': await current(game.id),
      }));

  /// Accepts a file made by [exportBytes]. Returns false if it is not one.
  Future<bool> importBytes(String gameId, List<int> bytes) async {
    try {
      final j = jsonDecode(utf8.decode(bytes)) as Map;
      if (j['format'] != 'folio-saves') return false;
      final storage = (j['storage'] as Map).cast<String, String>();
      await backupNow(gameId, reason: 'before-import');
      _current[gameId] = Map.of(storage);
      _pendingForce.add(gameId);
      await _flush(gameId);
      return true;
    } on Object {
      return false;
    }
  }

  Future<void> deleteAll(String gameId) async {
    _current.remove(gameId);
    _owned.remove(gameId);
    final d = Directory(paths.savesDir(gameId));
    if (await d.exists()) await d.delete(recursive: true);
  }

  /// Script run at document start, before any game code.
  ///
  /// Normal launch: puts back keys the WebView lost, never overwrites a key
  /// the WebView still has (the WebView copy can be newer if the app was
  /// killed before our flush). After a restore or import: overwrites, and
  /// removes this game's keys that the restored state does not have.
  Future<String> injectionScript(String gameId) async {
    final data = await current(gameId);
    final force = _pendingForce.remove(gameId);
    final own = force ? (await owned(gameId)).toList() : const <String>[];
    return '''
(function () {
  var DATA = ${jsonEncode(data)};
  var FORCE = ${force ? 'true' : 'false'};
  var OWN = ${jsonEncode(own)};
  var ls;
  try { ls = window.localStorage; } catch (e) { return; }
  var proto = Storage.prototype, set = proto.setItem, rem = proto.removeItem, clr = proto.clear;
  try {
    if (FORCE) {
      OWN.forEach(function (k) { if (!(k in DATA)) rem.call(ls, k); });
    }
    for (var key in DATA) { if (FORCE || ls.getItem(key) === null) set.call(ls, key, DATA[key]); }
  } catch (e) {}
  var queue = [];
  function send(op, k, v) {
    var b = window.flutter_inappwebview;
    if (b && b.callHandler) { b.callHandler('folioStorage', op, k, v); return; }
    queue.push([op, k, v]);
  }
  window.addEventListener('flutterInAppWebViewPlatformReady', function () {
    var q = queue; queue = [];
    q.forEach(function (a) { window.flutter_inappwebview.callHandler('folioStorage', a[0], a[1], a[2]); });
  });
  proto.setItem = function (k, v) { set.call(this, k, v); if (this === ls) send('set', String(k), String(v)); };
  proto.removeItem = function (k) { rem.call(this, k); if (this === ls) send('remove', String(k), null); };
  proto.clear = function () { clr.call(this); if (this === ls) send('clear', null, null); };
})();
''';
  }
}
