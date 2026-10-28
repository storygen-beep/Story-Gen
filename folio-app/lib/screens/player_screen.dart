import 'dart:async';
import 'dart:collection';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:wakelock_plus/wakelock_plus.dart';

import '../data/models.dart';
import '../state.dart';
import '../theme/app_theme.dart';
import '../theme/tokens.dart';
import '../ui/folio_icon.dart';
import '../ui/widgets.dart';

/// Replica screen 5: the game, full screen, with a bar the player can pull
/// down.
class PlayerScreen extends ConsumerStatefulWidget {
  const PlayerScreen({super.key, required this.id});
  final String id;
  @override
  ConsumerState<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends ConsumerState<PlayerScreen> {
  late final Game _game = ref.read(gameProvider(widget.id))!;
  late final Future<String> _script = ref.read(servicesProvider).saves.injectionScript(widget.id);
  var _controls = false;
  var _landscape = false;
  String? _loadError;

  @override
  void initState() {
    super.initState();
    _applySystemUi(_game.options);
    ref.read(libraryProvider.notifier).markPlayed(widget.id);
  }

  void _applySystemUi(GameOptions o) {
    if (o.fullScreen) SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    WakelockPlus.toggle(enable: o.keepAwake);
    _setOrientation(switch (o.orientation) {
      GameOrientation.portrait => false,
      GameOrientation.landscape => true,
      GameOrientation.auto => null,
    });
  }

  void _setOrientation(bool? landscape) {
    SystemChrome.setPreferredOrientations(switch (landscape) {
      null => DeviceOrientation.values,
      true => [DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight],
      false => [DeviceOrientation.portraitUp],
    });
  }

  @override
  void dispose() {
    ref.read(servicesProvider).saves.flushAll();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    SystemChrome.setPreferredOrientations(DeviceOrientation.values);
    WakelockPlus.disable();
    super.dispose();
  }

  Future<void> _backupNow() async {
    final saves = ref.read(servicesProvider).saves;
    await saves.flushAll();
    final b = await saves.backupNow(widget.id, reason: 'manual');
    ref.invalidate(backupsProvider(widget.id));
    if (mounted) showToast(context, b == null ? 'Nothing to back up yet. Save in the game first.' : 'Backed up');
  }

  @override
  Widget build(BuildContext context) {
    final c = context.c;
    final services = ref.read(servicesProvider);
    final o = _game.options;
    final url = services.server.entryUrl(_game.id, _game.entryPath);

    return Scaffold(
      backgroundColor: c.gameBg,
      body: FutureBuilder<String>(
        future: _script,
        builder: (context, snap) {
          if (!snap.hasData) return const SizedBox.expand();
          return Stack(children: [
            Positioned.fill(
              child: SafeArea(
                child: InAppWebView(
                  initialUrlRequest: URLRequest(url: WebUri.uri(url)),
                  initialUserScripts: UnmodifiableListView([
                    UserScript(source: snap.data!, injectionTime: UserScriptInjectionTime.AT_DOCUMENT_START),
                  ]),
                  initialSettings: InAppWebViewSettings(
                    javaScriptEnabled: true,
                    domStorageEnabled: true,
                    databaseEnabled: true,
                    mediaPlaybackRequiresUserGesture: !o.inlineVideo,
                    allowsInlineMediaPlayback: true,
                    textZoom: o.textScale,
                    preferredContentMode: o.desktopLayout ? UserPreferredContentMode.DESKTOP : UserPreferredContentMode.RECOMMENDED,
                    supportZoom: false,
                    disallowOverScroll: true,
                    useShouldOverrideUrlLoading: true,
                    javaScriptCanOpenWindowsAutomatically: false,
                    isInspectable: kDebugMode,
                    transparentBackground: false,
                  ),
                  onWebViewCreated: (controller) {
                    controller.addJavaScriptHandler(
                      handlerName: 'folioStorage',
                      callback: (args) {
                        if (args.length < 3) return null;
                        services.saves.onStorageEvent(_game.id, '${args[0]}', args[1] as String?, args[2] as String?);
                        return null;
                      },
                    );
                  },
                  // Only the game's own pages load in the player. Links out of
                  // the game are dropped rather than replacing the game.
                  shouldOverrideUrlLoading: (controller, action) async {
                    final u = action.request.url;
                    final local = u != null && u.host == '127.0.0.1' && u.port == services.server.port;
                    return local || u?.scheme == 'about' || u?.scheme == 'blob' || u?.scheme == 'data'
                        ? NavigationActionPolicy.ALLOW
                        : NavigationActionPolicy.CANCEL;
                  },
                  onLoadStop: (controller, _) async {
                    // textZoom is Android only; this is the iOS equivalent.
                    if (o.textScale != 100 && defaultTargetPlatform == TargetPlatform.iOS) {
                      await controller.evaluateJavascript(source: "document.documentElement.style.webkitTextSizeAdjust='${o.textScale}%';");
                    }
                  },
                  onReceivedError: (controller, request, error) {
                    if (request.isForMainFrame ?? false) setState(() => _loadError = error.description);
                  },
                ),
              ),
            ),
            if (_loadError != null)
              Positioned.fill(
                child: ColoredBox(
                  color: c.gameBg,
                  child: Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(mainAxisSize: MainAxisSize.min, children: [
                        Text('The game did not load', style: FolioType.heading(c.gameFg)),
                        const SizedBox(height: 8),
                        Text(_loadError!, textAlign: TextAlign.center, style: FolioType.body(c.gameFg.withValues(alpha: 0.7), size: 14)),
                        const SizedBox(height: 16),
                        FolioButton(label: 'Back', onPressed: () => context.pop()),
                      ]),
                    ),
                  ),
                ),
              ),
            _overlay(context),
          ]);
        },
      ),
    );
  }

  Widget _overlay(BuildContext context) {
    final c = context.c;
    const ink = Color(0xFFF1EEE8);
    final top = MediaQuery.paddingOf(context).top;
    if (!_controls) {
      return Positioned(
        top: top + 8,
        left: 0,
        right: 0,
        child: Center(
          child: Material(
            color: const Color(0x24FFFFFF),
            shape: const StadiumBorder(),
            child: InkWell(
              customBorder: const StadiumBorder(),
              onTap: () => setState(() => _controls = true),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                child: Text('Show controls', style: FolioType.body(ink, size: 12, weight: FontWeight.w600)),
              ),
            ),
          ),
        ),
      );
    }
    Widget dockButton(FolioIcons icon, String label, VoidCallback onTap) => Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: Material(
              color: const Color(0xFF1F2125),
              borderRadius: BorderRadius.circular(12),
              child: InkWell(
                borderRadius: BorderRadius.circular(12),
                onTap: onTap,
                child: SizedBox(
                  height: 56,
                  child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                    FolioIcon(icon, color: c.gameFg),
                    const SizedBox(height: 4),
                    Text(label, style: FolioType.body(c.gameFg, size: 12, weight: FontWeight.w600)),
                  ]),
                ),
              ),
            ),
          ),
        );
    return Positioned.fill(
      child: Column(children: [
        Container(
          padding: EdgeInsets.fromLTRB(12, top + 12, 12, 24),
          decoration: const BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Color(0xBF000000), Color(0x00000000)])),
          child: Row(children: [
            FolioIconButton(icon: FolioIcons.back, tooltip: 'Leave game', onPressed: () => context.pop(), background: const Color(0x1AFFFFFF), borderColor: const Color(0x24FFFFFF), color: ink),
            const SizedBox(width: 8),
            Expanded(child: Text(_game.title, maxLines: 1, overflow: TextOverflow.ellipsis, style: FolioType.body(ink, size: 14, weight: FontWeight.w600))),
            FolioIconButton(icon: FolioIcons.full, tooltip: 'Hide controls', onPressed: () => setState(() => _controls = false), background: const Color(0x1AFFFFFF), borderColor: const Color(0x24FFFFFF), color: ink),
          ]),
        ),
        const Spacer(),
        Container(
          padding: EdgeInsets.fromLTRB(8, 10, 8, 14 + MediaQuery.paddingOf(context).bottom),
          decoration: const BoxDecoration(color: Color(0xFF141518), border: Border(top: BorderSide(color: Color(0xFF26292D)))),
          child: Row(children: [
            dockButton(FolioIcons.save, 'Back up now', _backupNow),
            dockButton(FolioIcons.load, 'Saves', () => context.push('/game/${widget.id}/saves')),
            dockButton(FolioIcons.rotate, 'Rotate', () {
              _landscape = !_landscape;
              _setOrientation(_landscape);
            }),
            dockButton(FolioIcons.sliders, 'Options', () => context.push('/game/${widget.id}/options')),
          ]),
        ),
      ]),
    );
  }
}
