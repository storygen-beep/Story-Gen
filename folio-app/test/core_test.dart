import 'dart:convert';
import 'dart:io';

import 'package:archive/archive_io.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:folio/data/library_store.dart';
import 'package:folio/data/models.dart';
import 'package:folio/services/game_server.dart';
import 'package:folio/services/importer.dart';
import 'package:folio/services/save_bridge.dart';
import 'package:path/path.dart' as p;

/// Builds a zip shaped like a real release: the game nested one folder deep,
/// plus macOS junk that must be ignored.
String _makeZip(Directory tmp, {required String html, Map<String, List<int>> extra = const {}}) {
  final archive = Archive()
    ..add(ArchiveFile.string('Night_Shift_v0.2.6/index.html', html))
    ..add(ArchiveFile.string('__MACOSX/Night_Shift_v0.2.6/._index.html', 'junk'));
  extra.forEach((name, bytes) => archive.add(ArchiveFile.bytes('Night_Shift_v0.2.6/$name', bytes)));
  final path = p.join(tmp.path, 'night_shift_v0.2.6.zip');
  File(path).writeAsBytesSync(ZipEncoder().encode(archive));
  return path;
}

void main() {
  late Directory tmp;
  setUp(() => tmp = Directory.systemTemp.createTempSync('folio_test_'));
  tearDown(() => tmp.deleteSync(recursive: true));

  group('importer', () {
    test('finds nested index.html, Twine story data, media and webm', () async {
      final zip = _makeZip(tmp,
          html: '<html><head><title>Night Shift v0.2.6</title></head><body>'
              '<tw-storydata name="Night Shift" ifid="ab12cd34-0000-4000-8000-000000000001" format="SugarCube" format-version="2.37.3"></tw-storydata>'
              '</body></html>',
          extra: {'videos/a.mp4': List.filled(100, 1), 'videos/b.webm': List.filled(50, 2), 'img/c.jpg': [1, 2, 3]});
      final d = await unpackAndDetect(zipPath: zip, stagingDir: p.join(tmp.path, 'stage'), originalName: 'night_shift_v0.2.6.zip');
      expect(d.title, 'Night Shift');
      expect(d.engine, 'SugarCube 2');
      expect(d.version, '0.2.6');
      expect(d.ifid, 'AB12CD34-0000-4000-8000-000000000001');
      expect(d.entryPath, 'Night_Shift_v0.2.6/index.html');
      expect(d.fileCount, 4, reason: '__MACOSX entry must not count');
      expect(d.mediaCount, 3);
      expect(d.webmCount, 1);
    });

    test('real game from this repo: First Term', () async {
      final html = File('../games/first_term/output/index.html');
      if (!html.existsSync()) return markTestSkipped('first_term not built');
      final zip = _makeZip(tmp, html: html.readAsStringSync());
      final d = await unpackAndDetect(zipPath: zip, stagingDir: p.join(tmp.path, 'stage'), originalName: 'first_term.zip');
      expect(d.title, 'First Term');
      expect(d.engine, 'SugarCube 2');
      expect(d.ifid, '83330C3F-9AB4-53E4-9750-35AFF86B9150');
    });

    test('zip without html is refused with a readable message', () async {
      final archive = Archive()..add(ArchiveFile.string('readme.txt', 'hi'));
      final path = p.join(tmp.path, 'x.zip');
      File(path).writeAsBytesSync(ZipEncoder().encode(archive));
      expect(() => unpackAndDetect(zipPath: path, stagingDir: p.join(tmp.path, 's'), originalName: 'x.zip'),
          throwsA(isA<ImportException>().having((e) => e.message, 'message', contains('No index.html'))));
    });
  });

  group('game server', () {
    late GameServer server;
    late HttpClient client;
    setUp(() async {
      final game = Directory(p.join(tmp.path, 'games', 'g1', 'Sub'))..createSync(recursive: true);
      File(p.join(game.path, 'index.html')).writeAsStringSync('<h1>hi</h1>');
      File(p.join(game.path, 'clip.mp4')).writeAsBytesSync(List.generate(1000, (i) => i % 256));
      File(p.join(tmp.path, 'secret.txt')).writeAsStringSync('nope');
      server = GameServer(p.join(tmp.path, 'games'));
      await server.start();
      client = HttpClient();
    });
    tearDown(() async {
      client.close(force: true);
      await server.stop();
    });

    Future<HttpClientResponse> get(String path, {String? range}) async {
      final req = await client.getUrl(Uri.parse('http://127.0.0.1:${server.port}$path'));
      if (range != null) req.headers.set(HttpHeaders.rangeHeader, range);
      return req.close();
    }

    test('serves the entry page as html with no-store', () async {
      final url = server.entryUrl('g1', 'Sub/index.html');
      expect(url.toString(), 'http://127.0.0.1:${server.port}/g/g1/Sub/index.html');
      final res = await get(url.path);
      expect(res.statusCode, 200);
      expect(res.headers.contentType?.mimeType, 'text/html');
      expect(res.headers.value(HttpHeaders.cacheControlHeader), 'no-store');
      expect(await utf8.decodeStream(res), '<h1>hi</h1>');
    });

    test('answers byte ranges, which iOS needs to play video', () async {
      final res = await get('/g/g1/Sub/clip.mp4', range: 'bytes=10-19');
      expect(res.statusCode, 206);
      expect(res.headers.value(HttpHeaders.contentRangeHeader), 'bytes 10-19/1000');
      final body = await res.fold<List<int>>([], (a, b) => a..addAll(b));
      expect(body, List.generate(10, (i) => i + 10));
      final open = await get('/g/g1/Sub/clip.mp4', range: 'bytes=990-');
      expect(open.headers.value(HttpHeaders.contentRangeHeader), 'bytes 990-999/1000');
      await open.drain<void>();
    });

    test('matches file names case-insensitively, like Windows-made zips expect', () async {
      final res = await get('/g/g1/sub/CLIP.MP4');
      expect(res.statusCode, 200);
      await res.drain<void>();
    });

    test('never serves outside the game folder', () async {
      final res = await get('/g/g1/..%2F..%2Fsecret.txt');
      expect(res.statusCode, anyOf(403, 404));
      await res.drain<void>();
    });
  });

  group('save store', () {
    late SaveStore saves;
    setUp(() => saves = SaveStore(AppPaths.at(tmp.path)));

    test('mirrors writes to disk and makes the first backup', () async {
      await saves.onStorageEvent('g1', 'set', 'SugarCube.ns.saves', 'slot-data');
      await saves.flushAll();
      final current = jsonDecode(File(p.join(tmp.path, 'saves', 'g1', 'current.json')).readAsStringSync());
      expect(current, {'SugarCube.ns.saves': 'slot-data'});
      expect(await saves.backups('g1'), hasLength(1));
    });

    test('keeps at most 10 backups', () async {
      await saves.onStorageEvent('g1', 'set', 'k', 'v');
      for (var i = 0; i < 14; i++) {
        await saves.backupNow('g1', reason: 'manual');
        await Future<void>.delayed(const Duration(milliseconds: 2));
      }
      expect(await saves.backups('g1'), hasLength(SaveStore.maxBackups));
    });

    test('export then import round-trips', () async {
      await saves.onStorageEvent('g1', 'set', 'k', 'v1');
      await saves.flushAll();
      final game = Game(id: 'g1', title: 'T', version: '1', engine: 'SugarCube 2', entryPath: 'index.html', sizeBytes: 0, fileCount: 1, mediaCount: 0, webmCount: 0, coverIndex: 0, addedAt: DateTime(2026));
      final bytes = await saves.exportBytes(game);
      await saves.onStorageEvent('g1', 'set', 'k', 'v2');
      expect(await saves.importBytes('g1', bytes), isTrue);
      expect((await saves.current('g1'))['k'], 'v1');
      expect(await saves.importBytes('g1', utf8.encode('{"not":"ours"}')), isFalse);
    });

    // Runs the injected script in node against a fake localStorage, so the
    // JavaScript is tested for real and not just as a string.
    Future<Map<String, dynamic>> runScript(String script, Map<String, String> before) async {
      final harness = '''
var store = ${jsonEncode(before)}; var sent = [];
function Storage() {}
Storage.prototype.getItem = function (k) { return k in store ? store[k] : null; };
Storage.prototype.setItem = function (k, v) { store[k] = String(v); };
Storage.prototype.removeItem = function (k) { delete store[k]; };
Storage.prototype.clear = function () { store = {}; };
Object.defineProperty(Storage.prototype, 'length', { get: function () { return Object.keys(store).length; } });
Storage.prototype.key = function (i) { return Object.keys(store)[i]; };
var ls = new Storage();
global.Storage = Storage;
global.window = { localStorage: ls, addEventListener: function () {},
  flutter_inappwebview: { callHandler: function (n, op, k, v) { sent.push([op, k, v]); } } };
$script
ls.setItem('game.new', 'x');
console.log(JSON.stringify({ store: store, sent: sent }));
''';
      final file = File(p.join(tmp.path, 'h.js'))..writeAsStringSync(harness);
      final r = await Process.run('node', [file.path]);
      expect(r.exitCode, 0, reason: '${r.stderr}');
      return jsonDecode(r.stdout as String) as Map<String, dynamic>;
    }

    test('script restores lost keys without overwriting live ones, then mirrors writes', () async {
      final hasNode = (await Process.run('which', ['node'])).exitCode == 0;
      if (!hasNode) return markTestSkipped('node not installed');
      await saves.onStorageEvent('g1', 'set', 'lost', 'from-backup');
      await saves.onStorageEvent('g1', 'set', 'live', 'old');
      final out = await runScript(await saves.injectionScript('g1'), {'live': 'newer', 'other.game': 'keep'});
      expect(out['store'], {'live': 'newer', 'other.game': 'keep', 'lost': 'from-backup', 'game.new': 'x'});
      expect(out['sent'], [
        ['set', 'game.new', 'x']
      ]);
    });

    test('after a restore the script overwrites and removes only this game\'s keys', () async {
      final hasNode = (await Process.run('which', ['node'])).exitCode == 0;
      if (!hasNode) return markTestSkipped('node not installed');
      await saves.onStorageEvent('g1', 'set', 'a', '1');
      await saves.flushAll();
      final first = (await saves.backups('g1')).first;
      await saves.onStorageEvent('g1', 'set', 'a', '2');
      await saves.onStorageEvent('g1', 'set', 'b', 'added-later');
      await saves.flushAll();
      await saves.restore('g1', first.id);
      final out = await runScript(await saves.injectionScript('g1'), {'a': '2', 'b': 'added-later', 'other.game': 'keep'});
      expect(out['store'], {'a': '1', 'other.game': 'keep', 'game.new': 'x'});
    });
  });
}
