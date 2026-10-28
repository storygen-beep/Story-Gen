import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../data/models.dart';
import '../state.dart';
import '../theme/app_theme.dart';
import '../theme/tokens.dart';
import '../ui/folio_icon.dart';
import '../ui/format.dart';
import '../ui/widgets.dart';

/// Replica screen 6.
///
/// The replica showed parsed save slots. A SugarCube save file is compressed
/// inside the game's storage, so this first build shows what Folio itself
/// guarantees: backups of the whole save state, restore, export and import.
/// Slot-level reading is a follow-up.
class SavesScreen extends ConsumerWidget {
  const SavesScreen({super.key, required this.id});
  final String id;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final c = context.c;
    final game = ref.watch(gameProvider(id));
    if (game == null) return FolioScreen(children: [BackBar('Saves', onBack: () => context.pop())]);
    final syncOn = ref.watch(prefsProvider.select((p) => p.syncOn));
    final backups = ref.watch(backupsProvider(id));
    final saves = ref.read(servicesProvider).saves;

    Future<void> export() async {
      final bytes = await saves.exportBytes(game);
      final name = '${game.title.replaceAll(RegExp(r'[^A-Za-z0-9]+'), '_').toLowerCase()}_saves.json';
      final uri = await FilePicker.saveFile(fileName: name, bytes: Uint8List.fromList(bytes), mimeType: 'application/json');
      if (uri != null && context.mounted) showToast(context, 'Saves exported as $name');
    }

    Future<void> import() async {
      final files = await FilePicker.pickFiles(type: FileType.custom, allowedExtensions: ['json']);
      final f = files.firstOrNull;
      if (f == null) return;
      final ok = await saves.importBytes(id, await f.readAsBytes());
      ref.invalidate(backupsProvider(id));
      if (context.mounted) {
        showToast(context, ok ? 'Saves imported. They load next time you open the game.' : 'That file is not a Folio saves file.');
      }
    }

    Future<void> restore(SaveBackup b) async {
      await showFolioSheet<void>(context,
          title: 'Restore this backup?',
          body: 'From ${formatWhen(b.createdAt)}. Your current saves are backed up first, so you can undo this.',
          actions: (sheet) => [
                FolioButton(
                  label: 'Restore',
                  icon: FolioIcons.load,
                  kind: ButtonKind.primary,
                  expand: true,
                  onPressed: () async {
                    Navigator.pop(sheet);
                    await saves.restore(id, b.id);
                    ref.invalidate(backupsProvider(id));
                    if (context.mounted) showToast(context, 'Restored. It loads next time you open the game.');
                  },
                ),
                FolioButton(label: 'Cancel', expand: true, onPressed: () => Navigator.pop(sheet)),
              ]);
    }

    return FolioScreen(children: [
      BackBar('${game.title} saves', onBack: () => context.pop()),
      FolioBanner(
        kind: syncOn ? BannerKind.good : BannerKind.info,
        icon: syncOn ? FolioIcons.cloud : FolioIcons.info,
        title: syncOn ? 'Backed up and synced' : 'Backed up on this phone',
        body: 'Every time the game saves, Folio copies it to app storage${syncOn ? ' and the cloud' : ''}. '
            "Clearing browser data or updating the game can't lose it.",
      ),
      Row(children: [
        Expanded(child: FolioButton(label: 'Export all', icon: FolioIcons.export, onPressed: export)),
        const SizedBox(width: 10),
        Expanded(child: FolioButton(label: 'Import', icon: FolioIcons.import, onPressed: import)),
      ]),
      Section(
        label: 'Backups',
        children: [
          backups.when(
            loading: () => const SizedBox(height: 40),
            error: (e, _) => Meta('Could not read backups: $e'),
            data: (list) => list.isEmpty
                ? const Padding(padding: EdgeInsets.symmetric(vertical: 30), child: Meta('No saves yet. Save inside the game and it shows up here.', align: TextAlign.center))
                : Container(
                    padding: const EdgeInsets.only(left: 14),
                    decoration: BoxDecoration(border: Border(left: BorderSide(color: c.line, width: 2))),
                    child: Column(children: [
                      for (var i = 0; i < list.length; i++)
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 6),
                          child: Row(children: [
                            Expanded(
                              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                                Text('${formatWhen(list[i].createdAt)}${i == 0 ? ' · latest' : ''}', style: FolioType.body(c.fg, size: 14, weight: FontWeight.w600)),
                                Text('${backupReason(list[i].reason)} · ${formatSize(list[i].sizeBytes)}', style: FolioType.body(c.muted, size: 12.5)),
                              ]),
                            ),
                            FolioButton(label: 'Restore', small: true, onPressed: () => restore(list[i])),
                          ]),
                        ),
                    ]),
                  ),
          ),
        ],
      ),
      Meta('Folio keeps the last 10 backups per game. Restoring makes a backup of the current saves first.'),
    ]);
  }
}
