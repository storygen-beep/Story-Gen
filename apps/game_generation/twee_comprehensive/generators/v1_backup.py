"""
Twee Comprehensive Generator v1.

Comprehensive game generator that creates sophisticated interactive experiences.
This is the isolated, self-contained comprehensive game generation system.
"""

from typing import Any, Optional

from apps.characters.models import Character
from apps.npcs.models import NPC
from apps.projects.models import Project
from apps.world.models import Location


class TweeComprehensiveGeneratorV1:
    """
    Comprehensive Twee generator with four-layer architecture.

    Integrates:
    - Foundation Layer: Location, time, and flag management
    - Character Layer: Player characters, NPCs, and traits
    - Interaction Layer: Navigation, activities, and triggers
    - Narrative Layer: Scenes, dialogue, and choices

    Completely isolated from other generation systems.
    """

    def __init__(self):
        self.project = None
        self.player_character = None
        self.npcs = []
        self.locations = []
        self.game_config = {}

    def generate(self, project: Project, options: Optional[dict] = None) -> str:
        """
        Generate comprehensive Twee content.

        Args:
            project: Django Project instance
            options: Optional generation options

        Returns:
            str: Complete Twee content with all features
        """
        self.project = project
        self.options = options or {}

        # Load project data
        self._load_project_data()

        # Build game configuration
        self.game_config = self._build_game_config()

        # Generate comprehensive game
        twee_sections = []

        # Add game metadata
        twee_sections.append(self._generate_metadata())

        # Add comprehensive initialization
        twee_sections.append(self._generate_initialization())

        # Add Foundation Layer
        twee_sections.append(self._generate_foundation_layer())

        # Add Character Layer
        twee_sections.append(self._generate_character_layer())

        # Add Interaction Layer
        twee_sections.append(self._generate_interaction_layer())

        # Add Narrative Layer
        twee_sections.append(self._generate_narrative_layer())

        # Add Presentation Layer
        twee_sections.append(self._generate_presentation_layer())

        return "\n\n".join(twee_sections)

    def _load_project_data(self):
        """Load all related project data."""
        # Load player character
        try:
            self.player_character = self.project.player_character
        except Character.DoesNotExist:
            self.player_character = None

        # Load NPCs
        self.npcs = list(
            NPC.objects.filter(project=self.project, deleted_at__isnull=True)
        )

        # Load locations
        self.locations = list(Location.objects.filter(project=self.project))

    def _build_game_config(self) -> dict[str, Any]:
        """Build game configuration."""
        return {
            "project_name": self.project.name,
            "project_id": str(self.project.id),
            "enable_character_progression": True,
            "enable_npc_interactions": len(self.npcs) > 0,
            "enable_location_discovery": len(self.locations) > 0,
            "enable_time_management": True,
            "enable_relationship_tracking": True,
            "character_count": 1 if self.player_character else 0,
            "npc_count": len(self.npcs),
            "location_count": len(self.locations),
        }

    def _generate_metadata(self) -> str:
        """Generate game metadata."""
        story_name = self.project.name or "Comprehensive Interactive Game"

        return f""":: Story [meta]
{{
    "name": "{story_name}",
    "ifid": "{self.project.id}",
    "format": "SugarCube",
    "format-version": "2.36.1",
    "start": "Start"
}}

:: StoryTitle
{story_name}

:: StoryData
{{
    "ifid": "{self.project.id}",
    "format": "SugarCube",
    "format-version": "2.36.1",
    "start": "Start"
}}"""

    def _generate_initialization(self) -> str:
        """Generate comprehensive initialization."""
        return f""":: Start
<!-- Comprehensive Game Initialization -->
<<set $player = {{
    name: "Player",
    stats: {{
        intelligence: 5,
        charisma: 5,
        stamina: 100,
        experience: 0,
        level: 1
    }},
    current_location: "",
    visited_locations: [],
    discovered_locations: [],
    relationships: {{}},
    inventory: [],
    progression: {{
        quests_completed: 0,
        scenes_experienced: 0,
        npcs_met: []
    }}
}}>>

<<set $flags = {{
    game_started: true,
    tutorial_completed: false,
    day_count: 1,
    current_time: {{
        hour: 9,
        day: "Monday",
        week: 1,
        period: "morning"
    }}
}}>>

<<set $game_state = {{
    current_canvas: "",
    visited_nodes: [],
    choices_made: {{}},
    active_scenes: [],
    available_activities: [],
    world_state: "active"
}}>>

<<set $world = {{
    locations: {{}},
    npcs: {{}},
    activities: {{}},
    time_events: []
}}>>

<h1>{self.game_config.get('project_name', 'Interactive Game')}</h1>
<p>Welcome to your comprehensive interactive experience!</p>

[[Begin Your Journey->GameHub]]"""

    def _generate_foundation_layer(self) -> str:
        """Generate Foundation Layer."""
        content = "<!-- FOUNDATION LAYER -->\n"

        # Location system
        content += self._generate_location_system()

        # Time system
        content += self._generate_time_system()

        # Flag system
        content += self._generate_flag_system()

        return content

    def _generate_location_system(self) -> str:
        """Generate location discovery and management system."""
        if not self.locations:
            return "<!-- No locations available -->\n"

        content = """
:: LocationSystemInit [startup]
<!-- Initialize location discovery system -->
<<set $world.locations = {}>>
<<set $player.discovered_locations = []>>

"""

        # Add each location
        for location in self.locations:
            location_id = str(location.id)
            content += f"""<<set $world.locations["{location_id}"] = {{
    name: "{location.name}",
    description: `{location.description or "A mysterious location."}`,
    type: "{location.location_type}",
    discovered: false,
    accessible: {str(location.is_accessible).lower()},
    requires_unlock: {str(location.requires_unlock).lower()}
}}>>

"""

        return content

    def _generate_time_system(self) -> str:
        """Generate time management system."""
        return """
:: TimeSystemInit [startup]
<!-- Initialize time management -->
<<set $time = {
    current_hour: 9,
    current_day: "Monday",
    current_week: 1,
    time_period: "morning",
    day_count: 1
}>>

:: TimeWidget [widget]
<!-- Time advancement widget -->
<<widget "advanceTime">>
    <<set _hours = $args[0] || 1>>
    <<set $time.current_hour += _hours>>

    <<if $time.current_hour >= 24>>
        <<set $time.current_hour = $time.current_hour - 24>>
        <<set $time.day_count += 1>>
    <</if>>

    <!-- Update time period -->
    <<if $time.current_hour >= 6 and $time.current_hour < 12>>
        <<set $time.time_period = "morning">>
    <<elseif $time.current_hour >= 12 and $time.current_hour < 18>>
        <<set $time.time_period = "afternoon">>
    <<elseif $time.current_hour >= 18 and $time.current_hour < 22>>
        <<set $time.time_period = "evening">>
    <<else>>
        <<set $time.time_period = "night">>
    <</if>>
<</widget>>

"""

    def _generate_flag_system(self) -> str:
        """Generate flag management system."""
        return """
:: FlagSystemInit [startup]
<!-- Initialize flag system -->
<<set $flags.character_flags = {}>>
<<set $flags.location_flags = {}>>
<<set $flags.story_flags = {}>>

"""

    def _generate_character_layer(self) -> str:
        """Generate Character Layer."""
        content = "<!-- CHARACTER LAYER -->\n"

        # Character system
        if self.player_character:
            content += self._generate_character_system()

        # NPC system
        if self.npcs:
            content += self._generate_npc_system()

        return content

    def _generate_character_system(self) -> str:
        """Generate player character system."""
        if not self.player_character:
            return "<!-- No player character available -->\n"

        character = self.player_character

        return f"""
:: CharacterSystemInit [startup]
<!-- Initialize character system -->
<<set $player.name = "{character.name}">>
<<set $player.description = `{character.description or ""}`>>
<<set $player.age = {character.age or 18}>>
<<set $player.personality_archetype = "{character.personality_archetype or 'regular'}">>
<<set $player.experience_points = {character.experience_points}>>
<<set $player.character_level = {character.character_level}>>

"""

    def _generate_npc_system(self) -> str:
        """Generate NPC interaction system."""
        if not self.npcs:
            return "<!-- No NPCs available -->\n"

        content = """
:: NPCSystemInit [startup]
<!-- Initialize NPC system -->
<<set $world.npcs = {}>>

"""

        # Add each NPC
        for npc in self.npcs:
            npc_id = str(npc.id)
            content += f"""<<set $world.npcs["{npc_id}"] = {{
    name: "{npc.name}",
    description: `{npc.description or ""}`,
    role: "{npc.role}",
    age: {npc.age or 25},
    interaction_style: "{npc.interaction_style}",
    personality_archetype: "{npc.personality_archetype or 'regular'}",
    quest_giver: {str(npc.quest_giver).lower()},
    romance_option: {str(npc.romance_option).lower()},
    interaction_frequency: {npc.interaction_frequency},
    interactions_count: 0,
    trust_level: 0
}}>>

"""

        return content

    def _generate_interaction_layer(self) -> str:
        """Generate Interaction Layer."""
        content = "<!-- INTERACTION LAYER -->\n"

        # Navigation system
        content += self._generate_navigation_system()

        # Activity system
        content += self._generate_activity_system()

        return content

    def _generate_navigation_system(self) -> str:
        """Generate navigation system."""
        return """
:: NavigationWidget [widget]
<!-- Enhanced navigation with stamina -->
<<widget "moveToLocation">>
    <<set _destination_id = $args[0]>>

    <<if $player.stats.stamina >= 5>>
        <<set $player.stats.stamina -= 5>>
        <<set $player.current_location = _destination_id>>
        <<set $player.visited_locations.push(_destination_id)>>

        <<if not $player.discovered_locations.includes(_destination_id)>>
            <<set $player.discovered_locations.push(_destination_id)>>
            <<set $world.locations[_destination_id].discovered = true>>
        <</if>>
    <</if>>
<</widget>>

"""

    def _generate_activity_system(self) -> str:
        """Generate activity system."""
        return """
:: ActivitySystemInit [startup]
<!-- Initialize activity system -->
<<set $world.activities = {
    "study": {
        name: "Study",
        description: "Increase intelligence",
        duration: 2,
        stamina_cost: 10
    },
    "socialize": {
        name: "Socialize",
        description: "Improve charisma",
        duration: 1,
        stamina_cost: 5
    },
    "rest": {
        name: "Rest",
        description: "Restore stamina",
        duration: 2,
        stamina_cost: -30
    }
}>>

"""

    def _generate_narrative_layer(self) -> str:
        """Generate Narrative Layer."""
        content = "<!-- NARRATIVE LAYER -->\n"

        # Dialogue system
        content += self._generate_dialogue_system()

        # Choice system
        content += self._generate_choice_system()

        return content

    def _generate_dialogue_system(self) -> str:
        """Generate dialogue system."""
        return """
:: DialogueWidget [widget]
<!-- Dialogue system -->
<<widget "generateNPCDialogue">>
    <<set _npc_id = $args[0]>>
    <<set _dialogue_type = $args[1] || "greeting">>
    <<set _npc = $world.npcs[_npc_id]>>

    <<if _npc>>
        <<switch _dialogue_type>>
            <<case "greeting">>
                <<set $temp_npc_dialogue = "Hello there!">>
            <<case "farewell">>
                <<set $temp_npc_dialogue = "Goodbye!">>
            <<default>>
                <<set $temp_npc_dialogue = "...">>
        <</switch>>
    <</if>>
<</widget>>

"""

    def _generate_choice_system(self) -> str:
        """Generate choice system."""
        return """
:: ChoiceWidget [widget]
<!-- Choice system with consequences -->
<<widget "makeChoice">>
    <<set _choice_id = $args[0]>>
    <<set _effects = $args[1] || {}>>

    <<set $game_state.choices_made[_choice_id] = {
        timestamp: $time.current_hour,
        day: $time.current_day
    }>>

    <<if _effects.experience>>
        <<set $player.stats.experience += _effects.experience>>
    <</if>>
<</widget>>

"""

    def _generate_presentation_layer(self) -> str:
        """Generate Presentation Layer."""
        return """
<!-- PRESENTATION LAYER -->

:: GameHub
<h2>Game Hub</h2>

<div class="character-status">
    <h3>$player.name</h3>
    <strong>Level:</strong> $player.character_level
    <br><strong>Stamina:</strong> $player.stats.stamina/100
    <br><strong>Time:</strong> $time.current_hour:00 - $time.time_period
</div>

<div class="action-menu">
    <h3>What would you like to do?</h3>

    <!-- Activities -->
    <h4>Activities</h4>
    <<for _activity_id, _activity range $world.activities>>
        [[_activity.name->PerformActivity][$temp_activity = _activity_id]]
    <</for>>

    <!-- NPCs -->
    <<if Object.keys($world.npcs).length > 0>>
        <h4>Talk to Someone</h4>
        <<for _npc_id, _npc range $world.npcs>>
            [[Talk to _npc.name->NPCInteraction][$temp_npc_target = _npc_id]]
        <</for>>
    <</if>>
</div>

:: PerformActivity
<<set _activity = $world.activities[$temp_activity]>>
<h2>_activity.name</h2>
<p>_activity.description</p>

<<if $player.stats.stamina >= _activity.stamina_cost>>
    <<set $player.stats.stamina -= _activity.stamina_cost>>
    <<advanceTime _activity.duration>>
    <p>Activity completed!</p>
<<else>>
    <p>Not enough stamina!</p>
<</if>>

[[Continue->GameHub]]

:: NPCInteraction
<<set _npc = $world.npcs[$temp_npc_target]>>
<h2>Talking with _npc.name</h2>

<<generateNPCDialogue $temp_npc_target "greeting">>
<p>"<<print $temp_npc_dialogue>>"</p>

<p><em>_npc.name is a _npc.role with a _npc.interaction_style personality.</em></p>

[[Say Goodbye->GameHub]]
"""
