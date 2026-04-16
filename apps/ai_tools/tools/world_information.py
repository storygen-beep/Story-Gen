"""
World Information Tools for Elora AI Assistant

Tools for getting information about characters, NPCs, locations, and world-building elements.
"""

from typing import Any

from django.db.models import Count
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from apps.npcs.models import NPC
from apps.projects.models import Project
from apps.world.models import Location


class WorldInformationInput(BaseModel):
    """Input schema for world information queries."""
    project_id: str = Field(description="The UUID of the project")
    info_type: str = Field(default="overview", description="Type of information (overview, locations, characters, npcs, relationships)")


@tool("get_world_information", args_schema=WorldInformationInput)
def get_world_information(project_id: str, info_type: str = "overview") -> str:
    """
    Get comprehensive world-building information for a project.

    Args:
        project_id: The UUID of the project
        info_type: Type of information (overview, locations, characters, npcs, relationships)

    Returns:
        Formatted string with world information
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        if info_type == "overview":
            return _get_world_overview(project)
        elif info_type == "locations":
            return _get_locations_info(project)
        elif info_type == "characters":
            return _get_characters_info(project)
        elif info_type == "npcs":
            return _get_npcs_info(project)
        elif info_type == "relationships":
            return _get_relationships_info(project)
        else:
            return f"Unknown info type: {info_type}. Available types: overview, locations, characters, npcs, relationships"

    except Exception as e:
        return f"Error getting world information: {str(e)}"


class CharacterDetailsInput(BaseModel):
    """Input schema for character details queries."""
    project_id: str = Field(description="The UUID of the project")
    character_name: str = Field(default="", description="Optional character name to search for (partial match)")
    location_name: str = Field(default="", description="Optional location name to filter characters by")


@tool("get_character_details", args_schema=CharacterDetailsInput)
def get_character_details(project_id: str, character_name: str = "", location_name: str = "") -> str:
    """
    Get detailed character information, optionally filtered by name or location.

    Args:
        project_id: The UUID of the project
        character_name: Optional character name to search for (partial match)
        location_name: Optional location name to filter characters by

    Returns:
        Formatted string with character details
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        # Start with NPCs (more likely to have multiple characters)
        npcs = NPC.objects.filter(project=project)

        # Apply filters
        if character_name:
            npcs = npcs.filter(name__icontains=character_name)

        if location_name:
            npcs = npcs.filter(location__name__icontains=location_name)

        result = f"👥 **Character Details for '{project.name}'**"

        # Add filter info
        filters = []
        if character_name:
            filters.append(f"name containing '{character_name}'")
        if location_name:
            filters.append(f"in location '{location_name}'")

        if filters:
            result += f" (filtered by {' and '.join(filters)})"

        result += "\\n\\n"

        # Player character
        if hasattr(project, 'player_character') and project.player_character:
            pc = project.player_character
            if not character_name or character_name.lower() in pc.name.lower():
                result += "**🎭 Player Character:**\\n"
                result += _format_character_details(pc, is_player=True)
                result += "\\n"

        # NPCs
        if npcs.exists():
            result += f"**👥 NPCs ({npcs.count()} found):**\\n\\n"

            for npc in npcs:
                result += _format_character_details(npc, is_player=False)
                result += "\\n"
        else:
            filter_text = " matching your criteria" if (character_name or location_name) else ""
            result += f"No NPCs found{filter_text}.\\n"

        return result

    except Exception as e:
        return f"Error getting character details: {str(e)}"


# World information helper functions

def _get_world_overview(project: Project) -> str:
    """Get comprehensive world overview."""
    result = f"🌍 **World Overview for '{project.name}'**\\n\\n"

    # Basic statistics
    locations = Location.objects.filter(project=project)
    npcs = NPC.objects.filter(project=project)
    has_player = hasattr(project, 'player_character') and project.player_character

    result += "**📊 World Statistics:**\\n"
    result += f"  • Locations: {locations.count()}\\n"
    result += f"  • NPCs: {npcs.count()}\\n"
    result += f"  • Player Character: {'Yes' if has_player else 'No'}\\n"

    # Location breakdown
    if locations.exists():
        result += "\\n**🏰 Location Overview:**\\n"

        # Locations with most NPCs
        locations_with_npcs = locations.annotate(
            npc_count=Count('npc')
        ).order_by('-npc_count')

        result += "  **Most Populated Locations:**\\n"
        for loc in locations_with_npcs[:5]:
            if loc.npc_count > 0:
                result += f"    • {loc.name}: {loc.npc_count} NPCs\\n"
            else:
                result += f"    • {loc.name}: No NPCs\\n"

    # NPC summary
    if npcs.exists():
        result += "\\n**👥 NPC Overview:**\\n"

        # NPCs by location
        located_npcs = npcs.filter(location__isnull=False).count()
        unlocated_npcs = npcs.filter(location__isnull=True).count()

        result += f"  • Located NPCs: {located_npcs}\\n"
        result += f"  • Unlocated NPCs: {unlocated_npcs}\\n"

    # World building suggestions
    result += "\\n**💡 World Building Insights:**\\n"

    if locations.count() == 0:
        result += "  • Consider adding locations to establish your world setting\\n"
    elif locations.count() < 3:
        result += "  • Your world could benefit from additional locations\\n"
    else:
        result += f"  • Good location variety with {locations.count()} different places\\n"

    if npcs.count() == 0:
        result += "  • Add NPCs to bring your world to life\\n"
    elif npcs.count() < 5:
        result += "  • Consider adding more NPCs to populate your world\\n"
    else:
        result += f"  • Well-populated world with {npcs.count()} NPCs\\n"

    # Character distribution analysis
    if npcs.exists() and locations.exists():
        avg_npcs_per_location = npcs.count() / locations.count()
        if avg_npcs_per_location < 1:
            result += "  • Some locations might feel empty - consider distributing NPCs more evenly\\n"
        elif avg_npcs_per_location > 5:
            result += "  • Very crowded world - consider if this fits your story tone\\n"
        else:
            result += f"  • Good NPC distribution with average {avg_npcs_per_location:.1f} NPCs per location\\n"

    return result


def _get_locations_info(project: Project) -> str:
    """Get detailed location information."""
    locations = Location.objects.filter(project=project).annotate(
        npc_count=Count('npc')
    ).order_by('name')

    if not locations.exists():
        return f"🏰 **Locations in '{project.name}'**\\n\\nNo locations found. Consider adding locations to establish your world setting."

    result = f"🏰 **Locations in '{project.name}'** ({locations.count()} total)\\n\\n"

    for location in locations:
        result += f"**{location.name}**\\n"

        if location.description:
            desc_preview = location.description[:150] + "..." if len(location.description) > 150 else location.description
            result += f"  📝 Description: {desc_preview}\\n"

        result += f"  👥 NPCs: {location.npc_count}\\n"

        # List NPCs in this location
        if location.npc_count > 0:
            location_npcs = NPC.objects.filter(location=location)[:5]  # First 5 NPCs
            npc_names = [npc.name for npc in location_npcs]
            result += f"     • {', '.join(npc_names)}"
            if location.npc_count > 5:
                result += f" (+{location.npc_count - 5} more)"
            result += "\\n"

        if location.metadata:
            result += f"  ⚙️ Additional Info: {len(location.metadata)} custom fields\\n"

        result += "\\n"

    return result


def _get_characters_info(project: Project) -> str:
    """Get character information overview."""
    result = f"👤 **Characters in '{project.name}'**\\n\\n"

    # Player character
    if hasattr(project, 'player_character') and project.player_character:
        pc = project.player_character
        result += "**🎭 Player Character:**\\n"
        result += f"  • **{pc.name}**\\n"

        if pc.description:
            desc_preview = pc.description[:100] + "..." if len(pc.description) > 100 else pc.description
            result += f"    Description: {desc_preview}\\n"

        if pc.metadata:
            result += f"    Custom Fields: {len(pc.metadata)} defined\\n"

        result += "\\n"
    else:
        result += "**🎭 Player Character:** Not defined\\n\\n"

    # NPCs summary
    npcs = NPC.objects.filter(project=project)

    if npcs.exists():
        result += f"**👥 NPCs ({npcs.count()} total):**\\n"

        # Group NPCs by location
        located_npcs = npcs.filter(location__isnull=False)
        unlocated_npcs = npcs.filter(location__isnull=True)

        if located_npcs.exists():
            # Group by location
            locations_with_npcs = {}
            for npc in located_npcs:
                loc_name = npc.location.name if npc.location else "Unknown Location"
                if loc_name not in locations_with_npcs:
                    locations_with_npcs[loc_name] = []
                locations_with_npcs[loc_name].append(npc.name)

            for location, npc_names in locations_with_npcs.items():
                result += f"\\n  **{location}:**\\n"
                for name in npc_names:
                    result += f"    • {name}\\n"

        if unlocated_npcs.exists():
            result += "\\n  **Unlocated NPCs:**\\n"
            for npc in unlocated_npcs[:10]:  # Limit to first 10
                result += f"    • {npc.name}\\n"

            if unlocated_npcs.count() > 10:
                result += f"    • ... and {unlocated_npcs.count() - 10} more\\n"
    else:
        result += "**👥 NPCs:** None defined\\n"

    return result


def _get_npcs_info(project: Project) -> str:
    """Get detailed NPC information."""
    npcs = NPC.objects.filter(project=project).select_related('location')

    if not npcs.exists():
        return f"👥 **NPCs in '{project.name}'**\\n\\nNo NPCs found. Consider adding NPCs to populate your world."

    result = f"👥 **NPCs in '{project.name}'** ({npcs.count()} total)\\n\\n"

    for npc in npcs[:15]:  # Limit to first 15 for readability
        result += _format_character_details(npc, is_player=False)
        result += "\\n"

    if npcs.count() > 15:
        result += f"... and {npcs.count() - 15} more NPCs\\n"

    return result


def _get_relationships_info(project: Project) -> str:
    """Get character relationship information."""
    result = f"🕸️ **Character Relationships in '{project.name}'**\\n\\n"

    locations = Location.objects.filter(project=project).annotate(
        npc_count=Count('npc')
    ).filter(npc_count__gt=0)

    if not locations.exists():
        return result + "No character relationships found. NPCs need to be assigned to locations to establish relationships."

    result += "**🏰 Location-based Relationships:**\\n\\n"

    for location in locations:
        npcs_in_location = NPC.objects.filter(location=location)

        result += f"**{location.name}** ({npcs_in_location.count()} characters):\\n"

        for npc in npcs_in_location:
            result += f"  • {npc.name}"
            if npc.description:
                # Extract relationship keywords from description
                desc_lower = npc.description.lower()
                relationship_words = []

                if 'friend' in desc_lower or 'ally' in desc_lower:
                    relationship_words.append('friendly')
                if 'enemy' in desc_lower or 'hostile' in desc_lower:
                    relationship_words.append('hostile')
                if 'merchant' in desc_lower or 'trader' in desc_lower:
                    relationship_words.append('merchant')
                if 'guard' in desc_lower or 'soldier' in desc_lower:
                    relationship_words.append('guard')
                if 'leader' in desc_lower or 'chief' in desc_lower or 'boss' in desc_lower:
                    relationship_words.append('leader')

                if relationship_words:
                    result += f" ({', '.join(relationship_words)})"

            result += "\\n"

        result += "\\n"

    # Player character relationships
    if hasattr(project, 'player_character') and project.player_character:
        pc = project.player_character
        result += "**🎭 Player Character Connections:**\\n"
        result += f"**{pc.name}** can interact with {NPC.objects.filter(project=project).count()} NPCs"
        result += f" across {locations.count()} locations.\\n\\n"

    # Relationship analysis
    total_npcs = NPC.objects.filter(project=project).count()
    if total_npcs > 0:
        located_npcs = NPC.objects.filter(project=project, location__isnull=False).count()
        relationship_density = located_npcs / total_npcs if total_npcs > 0 else 0

        result += "**📊 Relationship Analysis:**\\n"
        result += f"  • Located Characters: {located_npcs}/{total_npcs} ({relationship_density:.1%})\\n"
        result += f"  • Average NPCs per Location: {total_npcs / locations.count():.1f}\\n"

        if relationship_density < 0.5:
            result += "  • Consider assigning more NPCs to locations for better relationships\\n"
        elif relationship_density > 0.9:
            result += "  • Excellent character placement for relationship building\\n"

    return result


def _format_character_details(character: Any, is_player: bool = False) -> str:
    """Format character details consistently."""
    char_type = "🎭" if is_player else "👤"
    result = f"**{char_type} {character.name}**\\n"

    # Description
    if character.description:
        desc_preview = character.description[:200] + "..." if len(character.description) > 200 else character.description
        result += f"  📝 {desc_preview}\\n"

    # Location (for NPCs)
    if not is_player and hasattr(character, 'location') and character.location:
        result += f"  📍 Location: {character.location.name}\\n"

    # Additional NPC-specific info
    if not is_player and hasattr(character, 'metadata') and character.metadata:
        result += f"  ⚙️ Additional Info: {len(character.metadata)} custom fields\\n"

    # Player character specific info
    if is_player and hasattr(character, 'metadata') and character.metadata:
        result += f"  ⚙️ Character Data: {len(character.metadata)} fields\\n"

    return result
