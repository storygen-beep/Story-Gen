#!/bin/zsh
# Regenerate scene sections, concatenate EVERY section into 5_scenes.toml, rebuild 1_, merge, package.
#
# Iteration 002 fix: iteration 001's copy ran in a scratch path and defaulted PARTS="ryan laura",
# then wrote 5_scenes.toml from PARTS alone, so a plain rerun dropped the other people's scenes.
# Now the scripts run from this folder, PARTS only picks which sections to REGENERATE, and the
# concatenation always walks ALL_PARTS in the order 0.1 shipped (verified byte-identical 2026-10-09).
# A part missing from parts/ stops the build instead of being silently left out.
set -e
HERE=${0:A:h}
ROOT=${HERE:h:h:h:h:h}
PH=$ROOT/games/first_term/toml_phases
ALL_PARTS=(ryan laura mark tom zoe hale jake cafe college pools extras home town)
cd $ROOT && source venv/bin/activate
cd $HERE
mkdir -p parts
for p in ${=PARTS:-$ALL_PARTS}; do python3 $p.py parts/$p.toml; done
for p in $ALL_PARTS; do [[ -s parts/$p.toml ]] || { echo "missing parts/$p.toml — run PARTS=$p first" >&2; exit 1; }; done
{ echo "# First Term — 5 · scenes. Generated: one section per person (sources in iterations/002/build_scripts)."; for p in $ALL_PARTS; do cat parts/$p.toml; done } > $PH/5_scenes.toml
python3 gen_world.py $PH/1_metadata_and_locations.toml
python3 phone.py $PH/8_phone.toml   # iteration 002, part 6: the phone is generated too
cd $ROOT
python3 scripts/merge_toml_phases.py games/first_term --validate 2>&1 | tail -1
python3 manage.py package_from_toml --file games/first_term/toml_phases/7_final_game.toml --output games/first_term/output --gen-version v2 --dev 2>&1 | grep -v "player_portrait: clothing type\|Location image not found\|uncommon type\|external media\|NOT copied\|video_folder\|BROKEN\|Re-run with" | grep -i "error\|fail\|❌\|  - \|warn\|✗\|Package ready" | head -40
