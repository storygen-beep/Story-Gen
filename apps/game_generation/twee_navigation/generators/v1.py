"""
Twee Navigation Generator v1.

Basic navigation-only game generator that creates simple world exploration games.
This is the isolated, self-contained navigation game generation system.
"""

import json
import logging
from typing import Optional

from apps.projects.models import Project
from apps.world.models import Location

logger = logging.getLogger(__name__)


class TweeNavigationGeneratorV1:
    """
    Navigation-only Twee generator.

    Creates simple 3-passage structure with GameStart -> NavigationHub -> NavigationOptions
    pattern using world locations. Completely isolated from other generation systems.
    """

    def __init__(self):
        self.project = None
        self.locations = []

    def generate(self, project: Project, options: Optional[dict] = None) -> str:
        """
        Generate navigation-only Twee content.

        Args:
            project: Django Project instance
            options: Optional generation options

        Returns:
            str: Complete Twee file content
        """
        self.project = project
        self.options = options or {}

        # Load project data
        self._load_project_data()

        # Generate navigation game
        return self._generate_navigation_game()

    def _load_project_data(self):
        """Load world locations and connections from Django models."""
        self.locations = list(Location.objects.filter(project=self.project).prefetch_related('entry_connections'))

    def _generate_navigation_game(self) -> str:
        """Generate navigation-only game content."""
        sections = []

        # Story metadata
        story_name = self.project.name or "Interactive Adventure"

        sections.append(
            f""":: Story [meta]
{{
    "name": "{story_name}",
    "ifid": "{self.project.id}",
    "format": "SugarCube",
    "format-version": "2.36.1",
    "start": "GameStart"
}}

:: StoryTitle
{story_name}

:: StoryData
{{
    "ifid": "{self.project.id}",
    "format": "SugarCube",
    "format-version": "2.36.1",
    "start": "GameStart"
}}"""
        )

        # Build entry connections data
        connections_init = []
        for location in self.locations:
            for entry_location in location.entry_connections.all():
                connection_data = {
                    "id": f"{location.id}_{entry_location.id}",
                    "from_location_id": str(location.id),
                    "to_location_id": str(entry_location.id),
                    "connection_type": "entry",
                    "navigation_text": f"Go to {entry_location.name}",
                }
                connections_init.append(f"    {self._dict_to_sugarcube(connection_data)}")

        connections_str = (
            "[\n" + ",\n".join(connections_init) + "\n]" if connections_init else "[]"
        )

        # Build locations data
        starting_location = self._get_starting_location()
        starting_location_id = (
            str(starting_location.id) if starting_location else "null"
        )

        locations_init = []
        for location in self.locations:
            location_data = {
                "name": location.name,
                "description": location.description or f"You are at {location.name}",
                "discovered": getattr(location, "is_starting_location", False),
            }
            locations_init.append(
                f'    "{location.id}": {self._dict_to_sugarcube(location_data)}'
            )

        locations_str = (
            "{\n" + ",\n".join(locations_init) + "\n}" if locations_init else "{}"
        )

        # GameStart passage
        sections.append(
            f""":: GameStart [system]
<h1>{story_name}</h1>
<p><em>Welcome to your interactive adventure.</em></p>

<<set $game_state to {{
    current_location: "{starting_location_id}",
    discovered_locations: ["{starting_location_id}"]
}}>>
<<set $locations to {locations_str}>>
<<set $world_connections to {connections_str}>>

<<link "Start Game">><<goto "NavigationHub">><</link>>"""
        )

        # NavigationHub passage
        sections.append(
            """:: NavigationHub [system]
<div class="navigation-hub">
    <div class="current-location">
        <p><<print $locations[$game_state.current_location].description>></p>
    </div>
    <<include "NavigationOptions">>
</div>"""
        )

        # NavigationOptions passage with dynamic navigation
        nav_options_lines = [
            ":: NavigationOptions [system]",
            '<div class="navigation-options">',
        ]

        # Generate navigation links using entry connections
        for location in self.locations:
            from_id = str(location.id)

            for entry_location in location.entry_connections.all():
                to_id = str(entry_location.id)
                safe_to_id = to_id.replace("-", "_")

                nav_options_lines.append(
                    f'<<if $game_state.current_location eq "{from_id}">><<set _link_text_{safe_to_id} to $locations["{to_id}"].name>><<link _link_text_{safe_to_id}>><<set $game_state.current_location to "{to_id}">><<if not $game_state.discovered_locations.includes("{to_id}")>><<run $game_state.discovered_locations.push("{to_id}")>><<set $locations["{to_id}"].discovered to true>><</if>><<goto "NavigationHub">><</link>><</if>>'
                )

        nav_options_lines.append("</div>")
        sections.append("\n".join(nav_options_lines))

        return "\n\n".join(sections)

    def _get_starting_location(self):
        """Find the starting location from the project's locations."""
        for location in self.locations:
            if getattr(location, "is_starting_location", False):
                return location
        # Return first location if no starting location is set
        return self.locations[0] if self.locations else None


    def _dict_to_sugarcube(self, data: dict) -> str:
        """Convert Python dict to SugarCube object format."""
        if not data:
            return "{}"

        items = []
        for key, value in data.items():
            if isinstance(value, str):
                # Escape quotes and use proper string format
                escaped_value = value.replace('"', '\\"').replace("'", "\\'")
                items.append(f'"{key}": "{escaped_value}"')
            elif isinstance(value, bool):
                items.append(f'"{key}": {str(value).lower()}')
            elif isinstance(value, (int, float)):
                items.append(f'"{key}": {value}')
            else:
                # Convert other types to JSON string
                value_json = json.dumps(str(value))
                items.append(f'"{key}": {value_json}')

        return "{" + ", ".join(items) + "}"

    def _convert_blocks_to_game_html(self, blocks: list[dict]) -> str:
        """
        Convert BlockNote blocks to basic HTML for SugarCube games.

        Args:
            blocks: List of BlockNote block dictionaries

        Returns:
            Basic HTML string without CSS classes
        """
        if not blocks:
            logger.warning("Empty blocks provided for HTML conversion")
            return "<p><em>No content</em></p>"

        try:
            html_parts = []

            for block in blocks:
                block_type = block.get("type")
                content = str(block.get("content", "")).strip()

                if not content:
                    continue

                if block_type == "heading":
                    level = block.get("props", {}).get("level", 1)
                    html_parts.append(f"<h{level}>{content}</h{level}>")
                elif block_type == "paragraph":
                    html_parts.append(f"<p>{content}</p>")
                else:
                    # Default to paragraph for unknown types
                    html_parts.append(f"<p>{content}</p>")

            result = "".join(html_parts)

            if not result:
                logger.warning("All blocks were empty after processing")
                return "<p><em>No content</em></p>"

            return result

        except Exception as e:
            logger.error(f"Error converting blocks to game HTML: {e}", extra={
                "blocks_count": len(blocks) if blocks else 0,
                "error": str(e)
            })
            return "<p><em>Error processing content</em></p>"
