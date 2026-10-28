# Folio

An offline player for HTML5 and Twine games (SugarCube, Harlowe, Snowman) on
iOS and Android. The player imports a game zip, Folio unpacks it, runs it full
screen, and keeps a copy of every save outside the WebView so saves survive.
Cloud sync of saves (Supabase) is the paid feature.

The design is the web replica at https://claude.ai/artifact/AdV9u2Z8UGwgFwcXEpEJH5.
Colors, type, radii and icons in `lib/theme/` and `lib/ui/` are copied from it 1:1.

Lives inside the Story-Gen repo for now; it has no dependency on it.

## Run

```sh
flutter pub get
flutter run                      # offline build, no cloud
flutter run \
  --dart-define=SUPABASE_URL=https://<project>.supabase.co \
  --dart-define=SUPABASE_PUBLISHABLE_KEY=<key>   # with cloud sync available
flutter test                     # importer, local server, save bridge
flutter build apk --release      # Android
flutter build ipa                # iOS, needs a Mac with Xcode
```

## How it works

| Piece | File | What it does |
|---|---|---|
| Import | `lib/services/importer.dart` | Streams the zip to disk in a background isolate, finds `index.html` (even nested), reads Twine story data for title, engine and IFID, counts media and WebM files |
| Local server | `lib/services/game_server.dart` | Serves `games/<id>/` on `http://127.0.0.1:47821`. A fixed origin keeps browser storage (where saves live) stable. Supports byte ranges, which iOS needs to play video. Never serves outside the game folder |
| Save bridge | `lib/services/save_bridge.dart` | A script injected before the game's own code mirrors every `localStorage` write to Flutter, which writes `saves/<id>/current.json` and keeps 10 timestamped backups. On launch it puts back any key the WebView lost |
| Player | `lib/screens/player_screen.dart` | `flutter_inappwebview`, inline autoplay video, orientation lock, full screen, keep awake, text size, links out of the game blocked |
| Library | `lib/state.dart`, `lib/data/` | JSON on disk, written atomically. Updating a game keeps its id, so it keeps its URL and its saves |
| Cloud | `lib/services/cloud_sync.dart`, `supabase/migrations/0001_init.sql` | Save upload/download keyed on the game's IFID. Row level security: users see only their own rows; writing needs an active entitlement |

## Status

Done and tested (`flutter test`, 12 tests): import, detection, local server
with ranges and path safety, save mirroring, backups, restore, export/import,
and the injected JavaScript itself (run in node against a fake localStorage).

Built, not yet tried on a real phone: every screen, the player, native config
(Android cleartext for 127.0.0.1 only, iOS `NSAllowsLocalNetworking`).

Not built yet:
- Share sheet and "Open with" import (needs `receive_sharing_intent` and
  native intent / document-type config)
- Sign-in, the sync loop, RevenueCat purchase and its webhook Edge Function
- Reading individual SugarCube save slots (they are compressed inside storage;
  backups cover the whole save state today)
- Bundled font files (fonts load from Google Fonts on first launch and are
  cached; offline first launch falls back to the system font)

## To check on a real device first

1. Saves survive force-quit and reopen (SugarCube 2.30+ writes `localStorage`;
   confirm on both platforms).
2. Video autoplays inline on iPhone.
3. A 230 MB game unpacks without running out of memory.
