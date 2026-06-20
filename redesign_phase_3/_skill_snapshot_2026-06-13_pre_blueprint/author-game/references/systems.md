# Optional game systems — the index (read the linked doctrine before wiring)

The engine ships five systems beyond the core NPC-arc/lane machinery. Four are **optional** (decide at
setup which the game uses); the HUD is always present. Each is easy to wire *wrong* in a way that
builds green but silently fails — so each row gives its TOML **home**, its **doctrine** file, and its
**ONE signature trap**. Homes are authoritative in `schema/02` §1.3; read the doctrine before wiring.

| System | TOML home | Doctrine | Signature trap (the thing that bites) |
|---|---|---|---|
| **Clothing** | `[settings]` + `[[clothing]]` | `doctrine/11` | **Two-part rule.** Clothing MAY gate **PUBLIC/world content + the exhibitionism meter** AND may **trigger ambient, in-character reactive-world events** (Lane 2/3 — `worn_corruption`-gated groping/cornering/etc., the reactive world). It must **NEVER gate an NPC's escalation spine / arc-progression** — gating a housemate's notice/hub/sex on `worn_corruption` is the *backwards on-ramp*. (Reactive Lane 2/3 events ARE "public content" the clothing doctrine permits; an NPC's *arc* is not.) |
| **Rent / economy** | `[settings.rent]` | `doctrine/12` | **Arm it after income:** set `start_after_flag` to an income/onboarding flag so the opening is rent-free. Pick `eviction_mode` (`game_end` vs `flag_set`); `due_day` is respected (don't assume Monday). |
| **Phone** | top-level **`[phone]`** (NOT `[settings]`) | `doctrine/13` | Phone triggers support **NO `day`/`time`/`weekday`/`location`/`random`** — use `days_since_flag` for time-relative delivery. Gate the device behind `purchase_flag`, and trigger threads on flags something actually sets. |
| **Customization** | `[[player.customization_fields]]` (+ per-NPC) | `doctrine/14` | Declaring the inputs is **half** the job — you MUST emit the **`@player` / `@<npc>` / `@<npc>.rel` output tokens** in prose, and **never bake a customizable name into a location / sidebar / quest label** (R2 — un-tokenizable surfaces print the raw default). |
| **HUD / sidebar** *(always on)* | `[[sidebar_items]]` | `reference/04` + `doctrine/09` §8 | **HUD = world model:** surface NPC location/arousal so the player can plan Lane 3. Use **`type = "npc_panel"`** (RTS House-card: `rows = ["arousal","corruption","location","next"]`; location from the NPC schedule; `next` = the Quests-page goal block (🎯 To advance + progress while climbing, 🔓 Ready/📍/🕒 when ready), reusing `renderQuestsGoalBlock`) or `trait_owner="npc"` trait items — **both supported now** (the old "no per-NPC sidebar" gotcha is stale). **The `next` block names PLACE + TIME-WINDOW + REQUIREMENT verbatim** (`14` L2 / G1 — "kitchen, 3–6 pm, needs her trust", not just "get closer"); a **cross-gated** next-step names the gating arc's state (`14` L7 / the machine `redesign_phase_3/22`). Sidebar visibility is **per-arc-shape**; energy/hygiene MUST surface; `stage`/`awareness` NEVER do. |

## How this lands in the workflow
- **Seed** (`references/step-0-1-seed.md`): decide which optional systems the game uses (clothing / rent /
  phone — yes/no) and record it in the design book; **ask explicitly whether the player or any NPC is
  customizable** — it's the easiest system to forget exists.
- **Beat-authoring** (`beat-authoring.md` self-audit): a beat that wires any of these honors the row's
  trap above + reads the linked doctrine. The scoping homes are also in `toml-gotchas.md`.
- **Don't restate the doctrine here** — this table is an index. The real design models (clothing's
  worn-vs-exhibitionism-vs-global axes, rent's RentDay flow, the phone app set, the `@`-token contract,
  the per-arc-shape sidebar table) live in the linked corpus files; open them before authoring.
