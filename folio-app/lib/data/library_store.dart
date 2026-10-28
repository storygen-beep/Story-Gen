import 'dart:convert';
import 'dart:io';

import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import 'models.dart';

/// On-disk layout, all inside the app's private support directory:
///
/// ```
/// library.json                 the game list
/// games/<id>/                  unpacked game files (served by GameServer)
/// saves/<id>/current.json      latest copy of the game's browser storage
/// saves/<id>/backups/<ts>.json snapshots, newest kept, oldest pruned
/// staging/<uuid>/              a zip being imported
/// ```
class AppPaths {
  AppPaths._(this.root);

  /// For tests: a layout rooted anywhere, without creating folders.
  AppPaths.at(this.root);

  final String root;

  static Future<AppPaths> resolve() async {
    final dir = await getApplicationSupportDirectory();
    final paths = AppPaths._(dir.path);
    for (final d in [paths.gamesDir, paths.savesRoot, paths.stagingDir]) {
      await Directory(d).create(recursive: true);
    }
    return paths;
  }

  String get libraryFile => p.join(root, 'library.json');
  String get gamesDir => p.join(root, 'games');
  String get savesRoot => p.join(root, 'saves');
  String get stagingDir => p.join(root, 'staging');
  String gameDir(String id) => p.join(gamesDir, id);
  String savesDir(String id) => p.join(savesRoot, id);
}

class LibraryStore {
  LibraryStore(this.paths);
  final AppPaths paths;

  Future<List<Game>> load() async {
    final f = File(paths.libraryFile);
    if (!await f.exists()) return [];
    try {
      final raw = jsonDecode(await f.readAsString()) as List;
      return raw.map((e) => Game.fromJson((e as Map).cast<String, Object?>())).toList();
    } on FormatException {
      // A half-written file from a crash. Keep it aside rather than lose it.
      await f.copy('${paths.libraryFile}.corrupt');
      return [];
    }
  }

  /// Write to a temp file then rename, so a crash never leaves a torn library.
  Future<void> save(List<Game> games) async {
    final tmp = File('${paths.libraryFile}.tmp');
    await tmp.writeAsString(jsonEncode(games.map((g) => g.toJson()).toList()));
    await tmp.rename(paths.libraryFile);
  }
}
