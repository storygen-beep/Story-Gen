#!/bin/zsh
# Regenerate every person's scene section and concatenate into 5_scenes.toml, then rebuild 1_ and merge.
set -e
SP=/private/tmp/claude-501/-Users-a0000-Desktop-Desktop-Archive-Backup-story-gen-story-gen-web-app-story-gen-django/140557ba-caa7-405d-8551-8ec2923554fe/scratchpad/build
ROOT=/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django
PH=$ROOT/games/first_term/toml_phases
cd $ROOT && source venv/bin/activate
cd $SP
mkdir -p parts
for p in ${=PARTS:-ryan laura}; do python3 $p.py parts/$p.toml; done
{ echo "# First Term — 5 · scenes. Generated: one section per person (sources in the build's scratch scripts)."; for p in ${=PARTS:-ryan laura}; do cat parts/$p.toml; done } > $PH/5_scenes.toml
python3 gen_world.py $PH/1_metadata_and_locations.toml
cd $ROOT
python3 scripts/merge_toml_phases.py games/first_term --validate 2>&1 | tail -1
python3 manage.py package_from_toml --file games/first_term/toml_phases/7_final_game.toml --output games/first_term/output --gen-version v2 --dev 2>&1 | grep -v "player_portrait: clothing type\|Location image not found\|uncommon type\|external media\|NOT copied\|video_folder\|BROKEN\|Re-run with" | grep -i "error\|fail\|❌\|  - \|warn\|✗\|Package ready" | head -40
