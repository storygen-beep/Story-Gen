# Optional game systems — the index (each has a full in-skill reference)

The engine ships five systems beyond the core NPC-arc/lane machinery. Four are **optional** (decide at
setup which the game uses); the HUD is always present. Each is easy to wire *wrong* in a way that
builds green but silently fails — so each row gives its TOML **home**, its **full in-skill reference**,
and its **ONE signature trap**. Every TOML home + engine field is in `references/engine-reference.md`
and the scoping gotchas in `references/toml-gotchas.md`; **read the linked reference before wiring.**

| System | TOML home | Full model | Signature trap (the thing that bites) |
|---|---|---|---|
| **Clothing** | `[settings]` + `[[clothing]]` | `references/clothing.md` | **Two-part rule.** Clothing MAY gate **PUBLIC/world content + the exhibitionism meter** AND may **trigger ambient, in-character reactive-world events** (Lane 2/3 — `worn_corruption`-gated groping/cornering/etc.). It must **NEVER gate an NPC's escalation spine / arc-progression** — gating a housemate's notice/hub/sex on `worn_corruption` is the *backwards on-ramp*. (Reactive Lane 2/3 events ARE "public content" clothing permits; an NPC's *arc* is not.) Plus: a `clothing_rule` needs a NON-EMPTY `slots_required` or the import hard-fails (`toml-gotchas.md`). |
| **Rent / economy** | `[settings.rent]` | `references/rent.md` | **Arm it after income:** set `start_after_flag` to an income/onboarding flag so the opening is rent-free. Pick `eviction_mode` (`game_end` vs `flag_set`); `due_day` is respected (don't assume Monday). Config MUST sit under `[settings.rent]` — bare keys are silently ignored. |
| **Phone** | top-level **`[phone]`** (NOT `[settings]`) | `references/phone.md` | Phone triggers support **NO `day`/`time`/`weekday`/`location`/`random`** — use `days_since_flag` for time-relative delivery. Gate the device behind `purchase_flag`; trigger threads on flags something actually sets. **Gate nesting: a thread's gate is `trigger.conditions = { version, items }` — one level deeper than a canvas trigger; the flat shape leaves `conditions` undefined → every thread fires at start (`toml-gotchas.md`).** |
| **Customization** | `[[player.customization_fields]]` (+ per-NPC `customizable`/`relationship_options`) | `references/customization.md` | Declaring the inputs is **half** the job — you MUST emit the **`@player` / `@<npc>` / `@<npc>.rel` output tokens** in prose, and **never bake a customizable name into a location / sidebar / quest label** (un-tokenizable surfaces print the raw default). |
| **HUD / sidebar** *(always on)* | `[[sidebar_items]]` | `references/hud.md` + `references/trait-catalog.md` §5 | **HUD = world model:** surface each in-scope NPC's location + arousal so the player can plan Lane 3. Use **`type = "npc_panel"`** (`rows = ["arousal","corruption","location","next"]`) or `trait_owner="npc"` trait items. **PLAYER bands — encode by type** (`trait-catalog.md` §5): `trait_words` = identity (corruption) · `trait_bar`+`bands`+`hide_value=true` = mood (arousal) · `trait_status_text` = body-need (hygiene/energy) · money stays a NUMBER. Band only where the word beats the number, and `[[traits.labels]] hidden=true` any banded stat so it doesn't print twice — but mind the NPC-panel name collision (`hud.md` §5). `stage`/`awareness` NEVER surface; energy/hygiene MUST. |

## How this lands in the workflow
- **Seed** (`references/step-0-1-seed.md`): decide which optional systems the game uses (clothing / rent /
  phone — yes/no) and record it in the design book; **ask explicitly whether the player or any NPC is
  customizable** — it's the easiest system to forget exists.
- **Beat-authoring** (`references/beat-authoring.md` self-audit): a beat that wires any of these honors the
  row's trap above **and reads the linked reference first**. The scoping homes + every build-breaker are
  also in `references/toml-gotchas.md`.
- **The full design models now live in-skill** — clothing's worn-vs-exhibitionism-vs-global axes, rent's
  RentDay flow, the phone app set + trigger vocab, the `@`-token contract, the `npc_panel` + per-arc-shape
  sidebar table — in the `references/*.md` files linked above. This table is the dispatcher; open the one
  you're wiring.
