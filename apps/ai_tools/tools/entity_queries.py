"""
Entity Query Tools for Elora AI Assistant

Tools for querying specific project entities like characters, locations, NPCs,
story nodes with flexible filtering and counting capabilities.
"""


from django.db.models import Count
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from apps.npcs.models import NPC
from apps.projects.models import Project
from apps.stories.models import NodeConnection, StoryNode
from apps.world.models import Location


class EntityQueryInput(BaseModel):
    """Input schema for entity queries."""
    project_id: str = Field(description="The UUID of the project to query")
    entity_type: str = Field(description="Type of entities to query (story_canvases, story_nodes, characters, npcs, locations, connections, flags)")
    filters: str = Field(default="none", description="Optional filters (count_only, detailed, by_status, recent)")


class ProjectStatsInput(BaseModel):
    """Input schema for project statistics."""
    project_id: str = Field(description="The UUID of the project to analyze")


@tool("query_project_entities", args_schema=EntityQueryInput)
def query_project_entities(project_id: str, entity_type: str, filters: str = "none") -> str:
    """
    Query specific project entities with flexible filtering.

    Args:
        project_id: The UUID of the project to query
        entity_type: Type of entities to query (story_canvases, story_nodes, characters, npcs, locations, connections, flags)
        filters: Optional filters (count_only, detailed, by_status, recent)

    Returns:
        Formatted string with entity information
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        # Route to appropriate entity query
        if entity_type == "story_canvases":
            return _query_story_canvases(project, filters)
        elif entity_type == "story_nodes":
            return _query_story_nodes(project, filters)
        elif entity_type == "characters":
            return _query_characters(project, filters)
        elif entity_type == "npcs":
            return _query_npcs(project, filters)
        elif entity_type == "locations":
            return _query_locations(project, filters)
        elif entity_type == "connections":
            return _query_connections(project, filters)
        elif entity_type == "flags":
            return "StoryFlag model removed; use character/NPC flag_keys instead."
        else:
            return f"Unknown entity type: {entity_type}. Available types: story_canvases, story_nodes, characters, npcs, locations, connections, flags"

    except Exception as e:
        return f"Error querying entities: {str(e)}"


@tool("get_project_statistics", args_schema=ProjectStatsInput)
def get_project_statistics(project_id: str) -> str:
    """
    Get comprehensive statistics for all project entities.

    Args:
        project_id: The UUID of the project to analyze

    Returns:
        Formatted string with complete project statistics
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        # Collect all statistics
        stats = {}

        # Story statistics
        canvases = project.story_canvases.all()
        stats['story_canvases'] = canvases.count()
        stats['story_nodes'] = StoryNode.objects.filter(canvas__project=project).count()
        stats['node_connections'] = NodeConnection.objects.filter(canvas__project=project).count()
        stats['story_flags'] = 0

        # Character statistics
        stats['characters'] = 1 if hasattr(project, 'player_character') and project.player_character else 0

        # NPC statistics
        stats['npcs'] = NPC.objects.filter(project=project).count()

        # Location statistics
        stats['locations'] = Location.objects.filter(project=project).count()

        # Canvas type breakdown
        canvas_types = canvases.values('canvas_type').annotate(count=Count('id'))
        type_breakdown = {ct['canvas_type']: ct['count'] for ct in canvas_types}

        # Connection type breakdown
        connection_types = NodeConnection.objects.filter(canvas__project=project).values('connection_type').annotate(count=Count('id'))
        conn_breakdown = {ct['connection_type']: ct['count'] for ct in connection_types}

        # Format response
        result = f"📊 **Complete Statistics for '{project.name}'**\\n\\n"

        result += "**📖 Story Elements:**\\n"
        result += f"  • Story Canvases: {stats['story_canvases']}\\n"
        result += f"  • Story Nodes: {stats['story_nodes']}\\n"
        result += f"  • Node Connections: {stats['node_connections']}\\n"
        result += f"  • Story Flags: {stats['story_flags']}\\n"

        if type_breakdown:
            result += "\\n  Canvas Types:\\n"
            for canvas_type, count in type_breakdown.items():
                result += f"    - {canvas_type.title()}: {count}\\n"

        result += "\\n**👥 Characters & NPCs:**\\n"
        result += f"  • Player Character: {stats['characters']}\\n"
        result += f"  • NPCs: {stats['npcs']}\\n"

        result += "\\n**🌍 World Building:**\\n"
        result += f"  • Locations: {stats['locations']}\\n"

        if conn_breakdown:
            result += "\\n**🔗 Connection Types:**\\n"
            for conn_type, count in conn_breakdown.items():
                result += f"  • {conn_type.title()}: {count}\\n"

        # Calculate totals
        total_content_pieces = (stats['story_canvases'] + stats['story_nodes'] +
                               stats['characters'] + stats['npcs'] + stats['locations'])

        result += "\\n**📈 Summary:**\\n"
        result += f"  • Total Content Pieces: {total_content_pieces}\\n"
        result += f"  • Connectivity Ratio: {stats['node_connections']}/{stats['story_nodes']} connections per node\\n"

        return result

    except Exception as e:
        return f"Error getting project statistics: {str(e)}"


# Helper functions for specific entity types

def _query_story_canvases(project: Project, filters: str) -> str:
    """Query story canvases with filtering."""
    canvases = project.story_canvases.all()

    if filters == "count_only":
        return f"Project '{project.name}' has {canvases.count()} story canvases."

    if not canvases.exists():
        return f"No story canvases found in project '{project.name}'."

    result = f"📖 **Story Canvases in '{project.name}'** ({canvases.count()} total)\\n\\n"

    for canvas in canvases:
        result += f"**{canvas.name}** ({canvas.canvas_type})\\n"
        if filters == "detailed":
            result += f"  • Status: {canvas.status}\\n"
            result += f"  • Nodes: {canvas.node_count}\\n"
            result += f"  • Connections: {canvas.connection_count}\\n"
            if canvas.description:
                result += f"  • Description: {canvas.description[:100]}...\\n"
        result += "\\n"

    return result


def _query_story_nodes(project: Project, filters: str) -> str:
    """Query story nodes with filtering."""
    nodes = StoryNode.objects.filter(canvas__project=project)

    if filters == "count_only":
        return f"Project '{project.name}' has {nodes.count()} story nodes."

    if not nodes.exists():
        return f"No story nodes found in project '{project.name}'."

    result = f"📝 **Story Nodes in '{project.name}'** ({nodes.count()} total)\\n\\n"

    # Group by canvas
    canvases = project.story_canvases.prefetch_related('nodes')

    for canvas in canvases:
        canvas_nodes = canvas.nodes.all()
        if canvas_nodes:
            result += f"**{canvas.name}:** {canvas_nodes.count()} nodes\\n"
            if filters == "detailed":
                for node in canvas_nodes[:5]:  # Limit to first 5 for readability
                    result += f"  • {node.name}\\n"
                if canvas_nodes.count() > 5:
                    result += f"  • ... and {canvas_nodes.count() - 5} more nodes\\n"
            result += "\\n"

    return result


def _query_characters(project: Project, filters: str) -> str:
    """Query characters with filtering."""
    has_character = hasattr(project, 'player_character') and project.player_character

    if filters == "count_only":
        count = 1 if has_character else 0
        return f"Project '{project.name}' has {count} player character."

    if not has_character:
        return f"No player character found in project '{project.name}'."

    character = project.player_character
    result = f"👤 **Player Character in '{project.name}'**\\n\\n"
    result += f"**{character.name}**\\n"

    if filters == "detailed":
        if character.description:
            result += f"  • Description: {character.description}\\n"
        if character.metadata:
            result += f"  • Additional Info: {len(character.metadata)} data fields\\n"

    return result


def _query_npcs(project: Project, filters: str) -> str:
    """Query NPCs with filtering."""
    npcs = NPC.objects.filter(project=project)

    if filters == "count_only":
        return f"Project '{project.name}' has {npcs.count()} NPCs."

    if not npcs.exists():
        return f"No NPCs found in project '{project.name}'."

    result = f"👥 **NPCs in '{project.name}'** ({npcs.count()} total)\\n\\n"

    for npc in npcs[:10]:  # Limit to first 10 for readability
        result += f"**{npc.name}**\\n"
        if filters == "detailed":
            if npc.description:
                result += f"  • Description: {npc.description[:100]}...\\n"
            if npc.location:
                result += f"  • Location: {npc.location.name}\\n"
        result += "\\n"

    if npcs.count() > 10:
        result += f"... and {npcs.count() - 10} more NPCs\\n"

    return result


def _query_locations(project: Project, filters: str) -> str:
    """Query locations with filtering."""
    locations = Location.objects.filter(project=project)

    if filters == "count_only":
        return f"Project '{project.name}' has {locations.count()} locations."

    if not locations.exists():
        return f"No locations found in project '{project.name}'."

    result = f"🏰 **Locations in '{project.name}'** ({locations.count()} total)\\n\\n"

    for location in locations[:10]:  # Limit to first 10 for readability
        result += f"**{location.name}**\\n"
        if filters == "detailed":
            if location.description:
                result += f"  • Description: {location.description[:100]}...\\n"
            # Count NPCs in this location
            npc_count = NPC.objects.filter(project=project, location=location).count()
            if npc_count > 0:
                result += f"  • NPCs: {npc_count}\\n"
        result += "\\n"

    if locations.count() > 10:
        result += f"... and {locations.count() - 10} more locations\\n"

    return result


def _query_connections(project: Project, filters: str) -> str:
    """Query node connections with filtering."""
    connections = NodeConnection.objects.filter(canvas__project=project)

    if filters == "count_only":
        return f"Project '{project.name}' has {connections.count()} node connections."

    if not connections.exists():
        return f"No node connections found in project '{project.name}'."

    result = f"🔗 **Node Connections in '{project.name}'** ({connections.count()} total)\\n\\n"

    # Group by connection type
    connection_types = connections.values('connection_type').annotate(count=Count('id'))

    for conn_type in connection_types:
        result += f"**{conn_type['connection_type'].title()}:** {conn_type['count']} connections\\n"

    if filters == "detailed":
        result += "\\n**Sample Connections:**\\n"
        for connection in connections[:5]:
            result += f"  • {connection.source_node.name} → {connection.target_node.name}"
            if connection.label:
                result += f" ({connection.label})"
            result += "\\n"

    return result


def _query_flags(project: Project, filters: str) -> str:
    """StoryFlag model removed; no query available."""
    return "StoryFlag model removed; use character/NPC flag_keys instead."
