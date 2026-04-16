"""
Management command to validate TOML game files for reachability issues.

This command analyzes a TOML game file to detect content that players cannot access
due to trait threshold gaps, broken flag chains, or other design issues.

Usage:
    python manage.py validate_game_toml path/to/game.toml
    python manage.py validate_game_toml path/to/game.toml --verbose --fix-suggestions

The command performs three-phase validation:
1. Syntax & Structure: TOML parsing, schema validation, reference integrity
2. Reachability Analysis: Trait gaps, flag chains, clip coverage
3. Report Generation: Errors, warnings, fix suggestions
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from django.core.management.base import BaseCommand, CommandError

from apps.projects.services.template_import import (
    GameTemplate,
    TemplateCanvas,
    TemplateChoice,
    normalize,
    parse_toml,
    validate,
)


@dataclass
class TraitGap:
    """Represents a trait threshold that cannot be reached."""
    canvas_id: str
    trait_key: str
    subject_type: str  # 'player' or 'npc'
    npc_id: Optional[str]
    starting_value: int
    max_reachable: int
    threshold_required: int
    gap: int


@dataclass
class BrokenFlagChain:
    """Represents a flag required by content but never set by reachable content."""
    flag_key: str
    required_by: List[str]  # canvas IDs
    set_by: Optional[str]  # canvas ID that sets it (if any)
    set_by_reachable: bool
    cascade_unreachable: List[str]  # canvases that become unreachable


@dataclass
class ClipCoverage:
    """Statistics about clip accessibility."""
    total_clips: int
    clips_in_base: int  # unconditional content
    clips_reachable: int
    clips_unreachable: int
    unreachable_clip_ids: List[str]


@dataclass
class ScheduleGap:
    """Represents a time period with no available content."""
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    duration_minutes: int
    locations_checked: List[str]


@dataclass
class ReachabilityReport:
    """Complete reachability analysis report."""
    trait_gaps: List[TraitGap]
    broken_chains: List[BrokenFlagChain]
    clip_coverage: ClipCoverage
    schedule_gaps: List[ScheduleGap]
    reachable_canvases: Set[str]
    unreachable_canvases: Set[str]
    warnings: List[str]


class ReachabilityAnalyzer:
    """Analyzes game template for reachability issues."""

    def __init__(self, template: GameTemplate):
        self.template = template
        self.canvas_map: Dict[str, TemplateCanvas] = {c.id: c for c in template.canvases}
        self.npc_map = {n.id: n for n in template.npcs}

    def analyze(self) -> ReachabilityReport:
        """Run complete reachability analysis."""
        # Initialize game state
        player_traits = dict(self.template.player.core_traits)
        npc_traits = {n.id: dict(n.core_traits) for n in self.template.npcs}

        # Find starting canvas
        starting_canvas = self.template.starting_canvas
        if not starting_canvas and self.template.canvases:
            starting_canvas = self.template.canvases[0].id

        # Build dependency graph and analyze reachability
        reachable = self._find_reachable_canvases(starting_canvas, player_traits, npc_traits)

        # Analyze trait gaps
        trait_gaps = self._analyze_trait_gaps(player_traits, npc_traits, reachable)

        # Analyze flag chains
        broken_chains = self._analyze_flag_chains(reachable)

        # Analyze clip coverage
        clip_coverage = self._analyze_clip_coverage(reachable)

        # Analyze schedule gaps
        schedule_gaps = self._analyze_schedule_gaps()

        # Determine unreachable canvases
        all_canvases = set(self.canvas_map.keys())
        unreachable = all_canvases - reachable

        # Generate warnings
        warnings = self._generate_warnings(reachable, clip_coverage, schedule_gaps)

        return ReachabilityReport(
            trait_gaps=trait_gaps,
            broken_chains=broken_chains,
            clip_coverage=clip_coverage,
            schedule_gaps=schedule_gaps,
            reachable_canvases=reachable,
            unreachable_canvases=unreachable,
            warnings=warnings,
        )

    def _find_reachable_canvases(
        self,
        starting_canvas: Optional[str],
        player_traits: Dict[str, Any],
        npc_traits: Dict[str, Dict[str, Any]],
    ) -> Set[str]:
        """BFS to find all reachable canvases from starting state."""
        if not starting_canvas:
            return set()

        reachable: Set[str] = set()
        flags: Set[str] = set()
        current_traits = dict(player_traits)
        current_npc_traits = {k: dict(v) for k, v in npc_traits.items()}

        # Use iterative approach - keep exploring until no new canvases found
        changed = True
        max_iterations = 100  # Prevent infinite loops

        iteration = 0
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            for canvas_id, canvas in self.canvas_map.items():
                if canvas_id in reachable:
                    continue

                # Check if canvas is reachable
                if self._can_reach_canvas(canvas, current_traits, current_npc_traits, flags):
                    reachable.add(canvas_id)
                    changed = True

                    # Apply effects from all choices in this canvas
                    self._apply_canvas_effects(
                        canvas, current_traits, current_npc_traits, flags
                    )

        return reachable

    def _can_reach_canvas(
        self,
        canvas: TemplateCanvas,
        player_traits: Dict[str, Any],
        npc_traits: Dict[str, Dict[str, Any]],
        flags: Set[str],
    ) -> bool:
        """Check if a canvas can be reached given current state."""
        # Starting canvas is always reachable
        if canvas.id == self.template.starting_canvas:
            return True
        if not self.template.starting_canvas and self.template.canvases:
            if canvas.id == self.template.canvases[0].id:
                return True

        # Check trigger conditions if present
        if canvas.trigger and canvas.trigger.conditions:
            conditions = canvas.trigger.conditions
            items = conditions.get("items", [])

            for item in items:
                if not self._check_condition(item, player_traits, npc_traits, flags):
                    return False

        return True

    def _check_condition(
        self,
        condition: Dict[str, Any],
        player_traits: Dict[str, Any],
        npc_traits: Dict[str, Dict[str, Any]],
        flags: Set[str],
    ) -> bool:
        """Check if a single condition is satisfied."""
        cond_type = condition.get("type", "")

        if cond_type == "trait":
            subject = condition.get("subject", "player")
            trait_key = condition.get("trait_key", "")
            operator = condition.get("operator", "gte")
            value = condition.get("value", 0)

            if subject == "player":
                current = player_traits.get(trait_key, 0)
            elif subject == "npc":
                npc_id = condition.get("npc_id", "")
                current = npc_traits.get(npc_id, {}).get(trait_key, 0)
            else:
                return True

            return self._compare(current, operator, value)

        elif cond_type == "flag":
            flag_key = condition.get("flag_key", "")
            return flag_key in flags

        # Unknown condition types are assumed to pass
        return True

    def _compare(self, current: Any, operator: str, value: Any) -> bool:
        """Compare values based on operator."""
        try:
            current = float(current) if current else 0
            value = float(value) if value else 0
        except (TypeError, ValueError):
            return True

        if operator == "gte":
            return current >= value
        elif operator == "gt":
            return current > value
        elif operator == "lte":
            return current <= value
        elif operator == "lt":
            return current < value
        elif operator == "eq":
            return current == value
        elif operator == "neq":
            return current != value
        return True

    def _apply_canvas_effects(
        self,
        canvas: TemplateCanvas,
        player_traits: Dict[str, Any],
        npc_traits: Dict[str, Dict[str, Any]],
        flags: Set[str],
    ) -> None:
        """Apply all possible effects from a canvas."""
        for node in canvas.nodes:
            if node.exit_block and node.exit_block.type == "choices":
                for choice in node.exit_block.choices:
                    self._apply_choice_effects(choice, player_traits, npc_traits, flags)

    def _apply_choice_effects(
        self,
        choice: TemplateChoice,
        player_traits: Dict[str, Any],
        npc_traits: Dict[str, Dict[str, Any]],
        flags: Set[str],
    ) -> None:
        """Apply effects from a choice (assumes player takes best path)."""
        # Apply trait effects
        for effect in choice.effects:
            target_type = effect.targetType
            trait = effect.trait
            op = effect.op
            value = effect.value

            if target_type == "player":
                if op == "add":
                    current = player_traits.get(trait, 0)
                    player_traits[trait] = current + value
                elif op == "set":
                    player_traits[trait] = value
            elif target_type == "npc":
                npc_id = effect.npcId
                if npc_id and npc_id in npc_traits:
                    if op == "add":
                        current = npc_traits[npc_id].get(trait, 0)
                        npc_traits[npc_id][trait] = current + value
                    elif op == "set":
                        npc_traits[npc_id][trait] = value

        # Apply flag effects
        for flag_effect in choice.flagEffects:
            flags.add(flag_effect.flag)

    def _analyze_trait_gaps(
        self,
        starting_player_traits: Dict[str, Any],
        starting_npc_traits: Dict[str, Dict[str, Any]],
        reachable: Set[str],
    ) -> List[TraitGap]:
        """Find trait thresholds that cannot be reached."""
        gaps: List[TraitGap] = []

        # Calculate max achievable traits from reachable content
        max_player_traits = dict(starting_player_traits)
        max_npc_traits = {k: dict(v) for k, v in starting_npc_traits.items()}

        for canvas_id in reachable:
            canvas = self.canvas_map.get(canvas_id)
            if not canvas:
                continue
            for node in canvas.nodes:
                if node.exit_block and node.exit_block.type == "choices":
                    for choice in node.exit_block.choices:
                        for effect in choice.effects:
                            if effect.op == "add" and effect.value > 0:
                                if effect.targetType == "player":
                                    current = max_player_traits.get(effect.trait, 0)
                                    max_player_traits[effect.trait] = current + effect.value
                                elif effect.targetType == "npc" and effect.npcId:
                                    if effect.npcId in max_npc_traits:
                                        current = max_npc_traits[effect.npcId].get(effect.trait, 0)
                                        max_npc_traits[effect.npcId][effect.trait] = current + effect.value

        # Check all canvases for unreachable thresholds
        for canvas_id, canvas in self.canvas_map.items():
            if canvas_id in reachable:
                continue

            if not canvas.trigger or not canvas.trigger.conditions:
                continue

            items = canvas.trigger.conditions.get("items", [])
            for item in items:
                if item.get("type") != "trait":
                    continue

                subject = item.get("subject", "player")
                trait_key = item.get("trait_key", "")
                threshold = item.get("value", 0)
                npc_id = item.get("npc_id")

                if subject == "player":
                    starting = starting_player_traits.get(trait_key, 0)
                    max_val = max_player_traits.get(trait_key, 0)
                elif subject == "npc" and npc_id:
                    starting = starting_npc_traits.get(npc_id, {}).get(trait_key, 0)
                    max_val = max_npc_traits.get(npc_id, {}).get(trait_key, 0)
                else:
                    continue

                if max_val < threshold:
                    gaps.append(TraitGap(
                        canvas_id=canvas_id,
                        trait_key=trait_key,
                        subject_type=subject,
                        npc_id=npc_id,
                        starting_value=int(starting),
                        max_reachable=int(max_val),
                        threshold_required=int(threshold),
                        gap=int(threshold - max_val),
                    ))

        return gaps

    def _analyze_flag_chains(self, reachable: Set[str]) -> List[BrokenFlagChain]:
        """Find flags that are required but never set by reachable content."""
        chains: List[BrokenFlagChain] = []

        # Map: flag -> canvas that sets it
        flag_setters: Dict[str, List[str]] = defaultdict(list)
        for canvas_id, canvas in self.canvas_map.items():
            for node in canvas.nodes:
                if node.exit_block and node.exit_block.type == "choices":
                    for choice in node.exit_block.choices:
                        for flag_effect in choice.flagEffects:
                            flag_setters[flag_effect.flag].append(canvas_id)

        # Map: flag -> canvases that require it
        flag_requirers: Dict[str, List[str]] = defaultdict(list)
        for canvas_id, canvas in self.canvas_map.items():
            if not canvas.trigger or not canvas.trigger.conditions:
                continue
            items = canvas.trigger.conditions.get("items", [])
            for item in items:
                if item.get("type") == "flag":
                    flag_key = item.get("flag_key", "")
                    flag_requirers[flag_key].append(canvas_id)

        # Find broken chains
        for flag_key, requirers in flag_requirers.items():
            setters = flag_setters.get(flag_key, [])

            # Check if any setter is reachable
            reachable_setters = [s for s in setters if s in reachable]

            if not reachable_setters:
                # Find cascade - what becomes unreachable due to this
                cascade = [r for r in requirers if r not in reachable]

                chains.append(BrokenFlagChain(
                    flag_key=flag_key,
                    required_by=requirers,
                    set_by=setters[0] if setters else None,
                    set_by_reachable=bool(reachable_setters),
                    cascade_unreachable=cascade,
                ))

        return chains

    def _analyze_clip_coverage(self, reachable: Set[str]) -> ClipCoverage:
        """Analyze how many clips are accessible."""
        all_clips: Set[str] = set()
        base_clips: Set[str] = set()
        reachable_clips: Set[str] = set()

        for canvas_id, canvas in self.canvas_map.items():
            for node in canvas.nodes:
                # Extract clips from blocks
                for block in node.blocks:
                    if block.get("type") == "clip":
                        clip_id = block.get("clip_id") or block.get("props", {}).get("clipId")
                        if clip_id:
                            all_clips.add(clip_id)

                            # Check if this is in base/unconditional content
                            is_base = self._is_base_content(canvas, node)
                            if is_base:
                                base_clips.add(clip_id)

                            if canvas_id in reachable:
                                reachable_clips.add(clip_id)

        unreachable_clips = all_clips - reachable_clips

        return ClipCoverage(
            total_clips=len(all_clips),
            clips_in_base=len(base_clips),
            clips_reachable=len(reachable_clips),
            clips_unreachable=len(unreachable_clips),
            unreachable_clip_ids=list(unreachable_clips),
        )

    def _is_base_content(self, canvas: TemplateCanvas, node) -> bool:
        """Check if content is unconditional (no trigger conditions)."""
        if not canvas.trigger:
            return True
        if not canvas.trigger.conditions:
            return True
        items = canvas.trigger.conditions.get("items", [])
        return len(items) == 0

    def _analyze_schedule_gaps(self) -> List[ScheduleGap]:
        """Find time periods where no content is available at any location."""
        if not self.template.time or not self.template.time.enabled:
            return []  # Time system disabled, no schedule gaps possible

        # Get all locations
        locations = [loc.id for loc in self.template.locations]
        if not locations:
            return []

        # Build schedule coverage per 30-minute slot (48 slots per day)
        # Each slot: set of location IDs that have content
        slots: Dict[int, Set[str]] = {i: set() for i in range(48)}

        # Map canvases to their time slots
        for canvas in self.template.canvases:
            if not canvas.trigger:
                continue  # No trigger = not location-based

            location = canvas.trigger.location
            if not location:
                continue

            # Check if this is unconditional content (no trait/flag requirements)
            is_unconditional = True
            if canvas.trigger.conditions:
                items = canvas.trigger.conditions.get("items", [])
                if items:
                    is_unconditional = False

            # Only count unconditional content for gap analysis
            # (gated content might not be available)
            if not is_unconditional:
                continue

            # Get schedules
            schedules = canvas.trigger.schedules or []
            if not schedules:
                # No schedule = always available during the day
                for slot in range(48):
                    slots[slot].add(location)
            else:
                for schedule in schedules:
                    start_time = schedule.start_time
                    end_time = schedule.end_time

                    if start_time and end_time:
                        start_slot = self._time_to_slot(start_time)
                        end_slot = self._time_to_slot(end_time)

                        # Handle schedule within a day
                        if start_slot <= end_slot:
                            for slot in range(start_slot, end_slot):
                                slots[slot].add(location)
                        else:
                            # Wraps around midnight
                            for slot in range(start_slot, 48):
                                slots[slot].add(location)
                            for slot in range(0, end_slot):
                                slots[slot].add(location)

        # Find gaps (consecutive slots with no content anywhere)
        gaps: List[ScheduleGap] = []
        gap_start: Optional[int] = None

        for slot in range(48):
            if not slots[slot]:  # No content at any location
                if gap_start is None:
                    gap_start = slot
            else:
                if gap_start is not None:
                    # Gap ended
                    duration = (slot - gap_start) * 30  # 30 min per slot
                    if duration >= 60:  # Only report gaps >= 1 hour
                        start_h, start_m = self._slot_to_time(gap_start)
                        end_h, end_m = self._slot_to_time(slot)
                        gaps.append(ScheduleGap(
                            start_hour=start_h,
                            start_minute=start_m,
                            end_hour=end_h,
                            end_minute=end_m,
                            duration_minutes=duration,
                            locations_checked=locations,
                        ))
                    gap_start = None

        # Handle gap at end of day
        if gap_start is not None:
            duration = (48 - gap_start) * 30
            if duration >= 60:
                start_h, start_m = self._slot_to_time(gap_start)
                gaps.append(ScheduleGap(
                    start_hour=start_h,
                    start_minute=start_m,
                    end_hour=23,
                    end_minute=59,
                    duration_minutes=duration,
                    locations_checked=locations,
                ))

        return gaps

    def _time_to_slot(self, time_str: str) -> int:
        """Convert HH:MM time string to slot index (0-47)."""
        try:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            return hour * 2 + (1 if minute >= 30 else 0)
        except (ValueError, IndexError):
            return 0

    def _slot_to_time(self, slot: int) -> Tuple[int, int]:
        """Convert slot index to (hour, minute)."""
        hour = slot // 2
        minute = 30 if slot % 2 else 0
        return hour, minute

    def _generate_warnings(
        self,
        reachable: Set[str],
        clip_coverage: ClipCoverage,
        schedule_gaps: List[ScheduleGap],
    ) -> List[str]:
        """Generate warnings about potential issues."""
        warnings: List[str] = []

        # Low clip reachability warning
        if clip_coverage.total_clips > 0:
            pct = (clip_coverage.clips_reachable / clip_coverage.total_clips) * 100
            if pct < 50:
                warnings.append(
                    f"Only {pct:.1f}% of clips are reachable - "
                    "consider lowering trait thresholds or adding more BASE content"
                )

        # Low base content warning
        if clip_coverage.total_clips > 0 and clip_coverage.clips_in_base == 0:
            warnings.append(
                "No clips in BASE (unconditional) content - "
                "players may see no clips if they miss progression triggers"
            )

        # Schedule gap warnings
        for gap in schedule_gaps:
            start = f"{gap.start_hour:02d}:{gap.start_minute:02d}"
            end = f"{gap.end_hour:02d}:{gap.end_minute:02d}"
            hours = gap.duration_minutes // 60
            mins = gap.duration_minutes % 60
            duration_str = f"{hours}h{mins:02d}m" if mins else f"{hours}h"
            warnings.append(
                f"Schedule gap {start}-{end} ({duration_str}) - "
                "no unconditional content triggers during this period"
            )

        return warnings


class Command(BaseCommand):
    help = "Validate TOML game file for reachability issues"

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
            help="Path to TOML game definition file",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Show detailed analysis",
        )
        parser.add_argument(
            "--fix-suggestions",
            action="store_true",
            help="Include specific fix recommendations",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output as JSON for CI/CD",
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        verbose = options["verbose"]
        fix_suggestions = options["fix_suggestions"]
        json_output = options["json"]

        # Phase 1: Syntax & Structure Validation
        template = self._validate_syntax(file_path)

        # Phase 2: Reachability Analysis
        report = self._analyze_reachability(template)

        # Phase 3: Report Generation
        if json_output:
            self._output_json(file_path, template, report)
        else:
            self._output_text(file_path, template, report, verbose, fix_suggestions)

    def _validate_syntax(self, file_path: str) -> GameTemplate:
        """Phase 1: Validate TOML syntax and structure."""
        # Parse TOML
        try:
            raw_data = parse_toml(file_path)
        except FileNotFoundError:
            raise CommandError(f"File not found: {file_path}")
        except Exception as e:
            raise CommandError(f"TOML parsing error: {e}")

        # Normalize to dataclass
        try:
            template = normalize(raw_data)
        except Exception as e:
            raise CommandError(f"Normalization error: {e}")

        # Run existing validation
        errors = validate(template)
        if errors:
            self.stdout.write(self.style.ERROR("❌ Structure validation failed:"))
            for err in errors:
                self.stdout.write(f"   - {err}")
            raise CommandError("TOML validation failed")

        return template

    def _analyze_reachability(self, template: GameTemplate) -> ReachabilityReport:
        """Phase 2: Run reachability analysis."""
        analyzer = ReachabilityAnalyzer(template)
        return analyzer.analyze()

    def _output_json(
        self,
        file_path: str,
        template: GameTemplate,
        report: ReachabilityReport,
    ) -> None:
        """Output results as JSON."""
        is_valid = (
            len(report.trait_gaps) == 0 and
            len(report.broken_chains) == 0 and
            report.clip_coverage.clips_unreachable == 0
        )

        output = {
            "file": file_path,
            "valid": is_valid,
            "errors": {
                "trait_gaps": [
                    {
                        "canvas_id": g.canvas_id,
                        "trait": f"{g.npc_id}.{g.trait_key}" if g.npc_id else g.trait_key,
                        "starting": g.starting_value,
                        "max_reachable": g.max_reachable,
                        "threshold": g.threshold_required,
                        "gap": g.gap,
                    }
                    for g in report.trait_gaps
                ],
                "broken_chains": [
                    {
                        "flag": c.flag_key,
                        "required_by": c.required_by,
                        "set_by": c.set_by,
                        "cascade_count": len(c.cascade_unreachable),
                    }
                    for c in report.broken_chains
                ],
            },
            "warnings": report.warnings,
            "clip_coverage": {
                "total": report.clip_coverage.total_clips,
                "reachable": report.clip_coverage.clips_reachable,
                "unreachable": report.clip_coverage.clips_unreachable,
                "percentage": (
                    (report.clip_coverage.clips_reachable / report.clip_coverage.total_clips * 100)
                    if report.clip_coverage.total_clips > 0 else 100
                ),
            },
            "schedule_gaps": [
                {
                    "start": f"{g.start_hour:02d}:{g.start_minute:02d}",
                    "end": f"{g.end_hour:02d}:{g.end_minute:02d}",
                    "duration_minutes": g.duration_minutes,
                }
                for g in report.schedule_gaps
            ],
            "canvas_summary": {
                "total": len(template.canvases),
                "reachable": len(report.reachable_canvases),
                "unreachable": len(report.unreachable_canvases),
            },
        }

        self.stdout.write(json.dumps(output, indent=2))

    def _output_text(
        self,
        file_path: str,
        template: GameTemplate,
        report: ReachabilityReport,
        verbose: bool,
        fix_suggestions: bool,
    ) -> None:
        """Output results as formatted text."""
        self.stdout.write("")
        self.stdout.write("=" * 50)
        self.stdout.write("  TOML VALIDATION REPORT")
        self.stdout.write("=" * 50)
        self.stdout.write(f"File: {file_path}")
        self.stdout.write("")

        # Syntax check results
        self.stdout.write("SYNTAX CHECK")
        self.stdout.write("  ✅ Valid TOML structure")
        self.stdout.write(f"  ✅ Schema version: {template.schema_version}")
        self.stdout.write("  ✅ All references resolve")
        self.stdout.write("")

        # Reachability results
        has_errors = False

        self.stdout.write("REACHABILITY ANALYSIS")

        # Trait gaps
        if report.trait_gaps:
            has_errors = True
            for gap in report.trait_gaps:
                trait_name = f"{gap.npc_id}.{gap.trait_key}" if gap.npc_id else gap.trait_key
                self.stdout.write("")
                self.stdout.write(self.style.ERROR(f"  ❌ TRAIT GAP: {gap.canvas_id}"))
                self.stdout.write(f"     Condition: {trait_name} >= {gap.threshold_required}")
                self.stdout.write(f"     Starting: {gap.starting_value}")
                self.stdout.write(f"     Max reachable: {gap.max_reachable}")
                self.stdout.write(f"     Gap: {gap.gap} points")

                if fix_suggestions:
                    self.stdout.write(self.style.WARNING(
                        f"     FIX: Lower threshold to {gap.max_reachable} OR "
                        f"increase effects by +{gap.gap}"
                    ))

        # Broken flag chains
        if report.broken_chains:
            has_errors = True
            for chain in report.broken_chains:
                self.stdout.write("")
                self.stdout.write(self.style.ERROR(f"  ❌ BROKEN FLAG CHAIN: {chain.flag_key}"))
                self.stdout.write(f"     Required by: {', '.join(chain.required_by)}")
                if chain.set_by:
                    self.stdout.write(f"     Set by: {chain.set_by} (UNREACHABLE)")
                else:
                    self.stdout.write("     Set by: NOTHING - flag is never set!")
                if chain.cascade_unreachable:
                    self.stdout.write(f"     Cascade: {len(chain.cascade_unreachable)} canvases unreachable")

                if fix_suggestions:
                    if chain.set_by:
                        self.stdout.write(self.style.WARNING(
                            f"     FIX: Make '{chain.set_by}' reachable first"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"     FIX: Add a choice that sets flag '{chain.flag_key}'"
                        ))

        if not report.trait_gaps and not report.broken_chains:
            self.stdout.write("  ✅ All content is reachable")

        self.stdout.write("")

        # Clip coverage
        self.stdout.write("CLIP COVERAGE")
        cc = report.clip_coverage
        self.stdout.write(f"  Total clips: {cc.total_clips}")
        self.stdout.write(f"  In BASE content: {cc.clips_in_base}")
        self.stdout.write(f"  Reachable: {cc.clips_reachable}")
        self.stdout.write(f"  Unreachable: {cc.clips_unreachable}")

        if cc.total_clips > 0:
            pct = (cc.clips_reachable / cc.total_clips) * 100
            if pct < 50:
                self.stdout.write(self.style.WARNING(
                    f"  ⚠️  WARNING: Only {pct:.1f}% of clips will be seen!"
                ))
            elif pct == 100:
                self.stdout.write(self.style.SUCCESS(
                    f"  ✅ All clips reachable ({pct:.0f}%)"
                ))
            else:
                self.stdout.write(f"  Coverage: {pct:.1f}%")

        if verbose and cc.unreachable_clip_ids:
            self.stdout.write("")
            self.stdout.write("  Unreachable clip IDs:")
            for clip_id in cc.unreachable_clip_ids[:5]:
                self.stdout.write(f"    - {clip_id}")
            if len(cc.unreachable_clip_ids) > 5:
                self.stdout.write(f"    ... and {len(cc.unreachable_clip_ids) - 5} more")

        self.stdout.write("")

        # Schedule gaps section
        if report.schedule_gaps:
            self.stdout.write("SCHEDULE GAPS")
            for gap in report.schedule_gaps:
                start = f"{gap.start_hour:02d}:{gap.start_minute:02d}"
                end = f"{gap.end_hour:02d}:{gap.end_minute:02d}"
                hours = gap.duration_minutes // 60
                mins = gap.duration_minutes % 60
                if mins:
                    duration_str = f"{hours}h {mins}m"
                else:
                    duration_str = f"{hours} hour{'s' if hours > 1 else ''}"

                self.stdout.write(self.style.WARNING(
                    f"  ⚠️  {start} - {end} ({duration_str}): No BASE content available"
                ))

                if fix_suggestions:
                    self.stdout.write(self.style.WARNING(
                        f"     FIX: Add unconditional canvas for this time window OR "
                        "extend existing canvas schedules"
                    ))
            self.stdout.write("")
        elif template.time and template.time.enabled:
            self.stdout.write("SCHEDULE GAPS")
            self.stdout.write("  ✅ No schedule gaps detected")
            self.stdout.write("")

        # Warnings
        if report.warnings:
            self.stdout.write("WARNINGS")
            for warning in report.warnings:
                self.stdout.write(self.style.WARNING(f"  ⚠️  {warning}"))
            self.stdout.write("")

        # Canvas summary (verbose)
        if verbose:
            self.stdout.write("CANVAS SUMMARY")
            self.stdout.write(f"  Total: {len(template.canvases)}")
            self.stdout.write(f"  Reachable: {len(report.reachable_canvases)}")
            self.stdout.write(f"  Unreachable: {len(report.unreachable_canvases)}")

            if report.unreachable_canvases:
                self.stdout.write("")
                self.stdout.write("  Unreachable canvases:")
                for canvas_id in sorted(report.unreachable_canvases):
                    self.stdout.write(f"    - {canvas_id}")

            self.stdout.write("")

        # Summary
        self.stdout.write("=" * 50)
        error_count = len(report.trait_gaps) + len(report.broken_chains)
        warning_count = len(report.warnings)

        self.stdout.write(f"  Errors: {error_count}")
        self.stdout.write(f"  Warnings: {warning_count}")

        if cc.total_clips > 0:
            pct = (cc.clips_reachable / cc.total_clips) * 100
            self.stdout.write(f"  Clips playable: {cc.clips_reachable}/{cc.total_clips} ({pct:.0f}%)")

        if has_errors:
            self.stdout.write("")
            self.stdout.write(self.style.ERROR("  Status: CANNOT SHIP - Critical reachability issues"))
        else:
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("  Status: ✅ READY TO SHIP"))

        self.stdout.write("=" * 50)
        self.stdout.write("")
