import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../state.dart';
import '../theme/app_theme.dart';
import '../theme/tokens.dart';
import '../ui/folio_icon.dart';
import '../ui/format.dart';
import '../ui/widgets.dart';

/// Replica screen 4.
class GameScreen extends ConsumerWidget {
  const GameScreen({super.key, required this.id});
  final String id;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final c = context.c;
    final game = ref.watch(gameProvider(id));
    if (game == null) return const _Missing();
    final backups = ref.watch(backupsProvider(id)).value ?? const [];
    final syncOn = ref.watch(prefsProvider.select((p) => p.syncOn));

    Widget stat(String value, String label, {bool first = false}) => Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: BoxDecoration(border: first ? null : Border(left: BorderSide(color: c.line))),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(value, style: FolioType.mono(c.fg, size: 17)),
              Text(label, style: FolioType.body(c.muted, size: 12)),
            ]),
          ),
        );

    return Scaffold(
      backgroundColor: c.panel,
      body: ListView(padding: EdgeInsets.zero, children: [
        Stack(children: [
          GameCover(game: game, height: 230 + MediaQuery.paddingOf(context).top, big: true, square: true),
          Positioned(
            top: 14 + MediaQuery.paddingOf(context).top,
            left: 14,
            child: FolioIconButton(
              icon: FolioIcons.back,
              tooltip: 'Back to library',
              onPressed: () => context.canPop() ? context.pop() : context.go('/library'),
              background: const Color(0x59000000),
              borderColor: Colors.transparent,
              color: FolioColors.coverInk,
            ),
          ),
        ]),
        Padding(
          padding: const EdgeInsets.all(18),
          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Text(game.title, style: FolioType.display(c.fg)),
            const SizedBox(height: 4),
            Meta('${game.version.isEmpty ? '' : 'v${game.version} · '}${game.engine} · ${formatSize(game.sizeBytes)}', mono: true),
            const SizedBox(height: 16),
            FolioButton(
              label: game.lastPlayedAt == null ? 'Play' : 'Resume',
              icon: FolioIcons.play,
              kind: ButtonKind.primary,
              expand: true,
              height: 54,
              onPressed: () => context.push('/game/$id/play'),
            ),
            const SizedBox(height: 16),
            Container(
              decoration: BoxDecoration(color: c.surface, border: Border.all(color: c.line), borderRadius: BorderRadius.circular(14)),
              child: IntrinsicHeight(
                child: Row(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  stat('${backups.length}', 'backups', first: true),
                  stat(backups.isEmpty ? '—' : formatWhen(backups.first.createdAt), 'last backup'),
                  stat(syncOn ? 'On' : 'Off', 'cloud sync'),
                ]),
              ),
            ),
            const SizedBox(height: 16),
            FolioList(children: [
              FolioItem(icon: FolioIcons.save, title: 'Saves and backups', subtitle: 'Export, import, restore', chevron: true, onTap: () => context.push('/game/$id/saves')),
              FolioItem(icon: FolioIcons.update, title: 'Update from a newer zip', subtitle: 'Keeps every save', chevron: true, onTap: () => context.push('/import?update=$id')),
              FolioItem(icon: FolioIcons.sliders, title: 'Game settings', subtitle: 'Screen, video, text size, storage', chevron: true, onTap: () => context.push('/game/$id/options')),
            ]),
          ]),
        ),
      ]),
    );
  }
}

class _Missing extends StatelessWidget {
  const _Missing();
  @override
  Widget build(BuildContext context) => FolioScreen(children: [
        BackBar('Game not found', onBack: () => context.go('/library')),
        const Meta('This game was deleted.'),
      ]);
}
