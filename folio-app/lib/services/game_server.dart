import 'dart:async';
import 'dart:io';

import 'package:path/path.dart' as p;

/// Serves unpacked games over http://127.0.0.1 so they run like a website.
///
/// Why a server and not file://: browser storage (where SugarCube keeps its
/// saves) is tied to the page's origin. file:// origins are treated
/// inconsistently by WebViews, and some block storage outright. A fixed
/// `http://127.0.0.1:<port>` origin is stable across launches, so saves stay
/// where the game expects them. If the port is ever taken and we fall back to
/// another, SaveBridge restores the game's storage from our own backup.
class GameServer {
  GameServer(this.gamesDir);

  static const preferredPort = 47821;
  static const _fallbackPorts = [47822, 47823, 47824, 47825];

  final String gamesDir;
  HttpServer? _server;

  int get port => _server?.port ?? preferredPort;
  bool get running => _server != null;

  /// URL the WebView opens for a game.
  Uri entryUrl(String gameId, String entryPath) =>
      Uri(scheme: 'http', host: '127.0.0.1', port: port, pathSegments: ['g', gameId, ...entryPath.split('/')]);

  Future<void> start() async {
    if (_server != null) return;
    for (final port in [preferredPort, ..._fallbackPorts]) {
      try {
        _server = await HttpServer.bind(InternetAddress.loopbackIPv4, port);
        break;
      } on SocketException {
        continue;
      }
    }
    final server = _server;
    if (server == null) throw StateError('No free local port for the game server');
    server.autoCompress = false;
    server.listen(_handle, onError: (_) {});
  }

  Future<void> stop() async {
    await _server?.close(force: true);
    _server = null;
  }

  Future<void> _handle(HttpRequest req) async {
    final res = req.response;
    try {
      if (req.method != 'GET' && req.method != 'HEAD') {
        res.statusCode = HttpStatus.methodNotAllowed;
        return;
      }
      final segs = req.uri.pathSegments;
      if (segs.length < 3 || segs.first != 'g') {
        res.statusCode = HttpStatus.notFound;
        return;
      }
      final root = p.normalize(p.join(gamesDir, segs[1]));
      final path = p.normalize(p.joinAll([root, ...segs.skip(2)]));
      // Never serve outside the game's own folder (no ../ escapes).
      if (!p.isWithin(root, path)) {
        res.statusCode = HttpStatus.forbidden;
        return;
      }
      var file = File(path);
      if (!await file.exists()) {
        // Windows-made zips often differ in case from what the HTML asks for.
        file = await _caseInsensitive(root, segs.skip(2).toList()) ?? file;
        if (!await file.exists()) {
          res.statusCode = HttpStatus.notFound;
          return;
        }
      }
      await _sendFile(req, res, file);
    } catch (_) {
      res.statusCode = HttpStatus.internalServerError;
    } finally {
      await res.close().catchError((_) {});
    }
  }

  /// Video needs byte ranges: iOS refuses to play an mp4 that is served
  /// without them, and seeking needs them everywhere.
  Future<void> _sendFile(HttpRequest req, HttpResponse res, File file) async {
    final length = await file.length();
    final type = _mime[p.extension(file.path).toLowerCase()] ?? 'application/octet-stream';
    res.headers
      ..set(HttpHeaders.contentTypeHeader, type)
      ..set(HttpHeaders.acceptRangesHeader, 'bytes')
      ..set(HttpHeaders.cacheControlHeader, type.startsWith('text/html') ? 'no-store' : 'max-age=3600');

    final range = req.headers.value(HttpHeaders.rangeHeader);
    final m = range == null ? null : RegExp(r'bytes=(\d*)-(\d*)').firstMatch(range);
    if (m != null && length > 0) {
      var start = int.tryParse(m.group(1)!) ;
      var end = int.tryParse(m.group(2)!);
      if (start == null && end != null) {
        start = length - end; // suffix range: last N bytes
        end = length - 1;
      }
      start ??= 0;
      end = (end == null || end >= length) ? length - 1 : end;
      if (start > end || start >= length) {
        res.statusCode = HttpStatus.requestedRangeNotSatisfiable;
        res.headers.set(HttpHeaders.contentRangeHeader, 'bytes */$length');
        return;
      }
      res.statusCode = HttpStatus.partialContent;
      res.headers
        ..set(HttpHeaders.contentRangeHeader, 'bytes $start-$end/$length')
        ..contentLength = end - start + 1;
      if (req.method == 'GET') await res.addStream(file.openRead(start, end + 1));
      return;
    }
    res.contentLength = length;
    if (req.method == 'GET') await res.addStream(file.openRead());
  }

  Future<File?> _caseInsensitive(String root, List<String> segs) async {
    var dir = Directory(root);
    for (var i = 0; i < segs.length; i++) {
      final want = segs[i].toLowerCase();
      FileSystemEntity? hit;
      await for (final e in dir.list(followLinks: false)) {
        if (p.basename(e.path).toLowerCase() == want) {
          hit = e;
          break;
        }
      }
      if (hit == null) return null;
      if (i == segs.length - 1) return hit is File ? hit : null;
      if (hit is! Directory) return null;
      dir = hit;
    }
    return null;
  }

  static const _mime = <String, String>{
    '.html': 'text/html; charset=utf-8',
    '.htm': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.mjs': 'text/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json',
    '.txt': 'text/plain; charset=utf-8',
    '.xml': 'application/xml',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.avif': 'image/avif',
    '.ico': 'image/x-icon',
    '.mp4': 'video/mp4',
    '.m4v': 'video/mp4',
    '.mov': 'video/quicktime',
    '.webm': 'video/webm',
    '.mp3': 'audio/mpeg',
    '.m4a': 'audio/mp4',
    '.ogg': 'audio/ogg',
    '.opus': 'audio/ogg',
    '.wav': 'audio/wav',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.wasm': 'application/wasm',
  };
}
