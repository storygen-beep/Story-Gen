"""
Story Details Tools for Elora AI Assistant

Tools for getting detailed information about specific story canvases and nodes.
"""

from typing import Any

from django.db.models import Count
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from apps.projects.models import Project
from apps.stories.models import NodeConnection, StoryCanvas


class StoryDetailsInput(BaseModel):
    """Input schema for story details."""
    canvas_id: str = Field(description="The UUID of the story canvas to analyze")
    depth: str = Field(default="standard", description="Detail level (basic, standard, detailed)")


class CanvasInfoInput(BaseModel):
    """Input schema for canvas information."""
    project_id: str = Field(description="The UUID of the project")
    canvas_name: str = Field(default="", description="Optional canvas name to search for (partial match)")
    canvas_type: str = Field(default="", description="Optional canvas type filter (story, intro, dialogue, tutorial)")


@tool("get_story_details", args_schema=StoryDetailsInput)
def get_story_details(canvas_id: str, depth: str = "standard") -> str:
    """
    Get detailed information about a specific story canvas.

    Args:
        canvas_id: The UUID of the story canvas to analyze
        depth: Detail level (basic, standard, detailed)

    Returns:
        Formatted string with canvas details
    """
    try:
        # Validate canvas exists
        try:
            canvas = StoryCanvas.objects.select_related('project').get(id=canvas_id)
        except StoryCanvas.DoesNotExist:
            return f"Story canvas with ID {canvas_id} not found."

        if depth == "basic":
            return _get_canvas_basic_info(canvas)
        elif depth == "detailed":
            return _get_canvas_detailed_info(canvas)
        else:  # standard
            return _get_canvas_standard_info(canvas)

    except Exception as e:
        return f"Error getting story details: {str(e)}"


@tool("get_canvas_information", args_schema=CanvasInfoInput)
def get_canvas_information(project_id: str, canvas_name: str = "", canvas_type: str = "") -> str:
    """
    Get information about story canvases by name or type within a project.

    Args:
        project_id: The UUID of the project
        canvas_name: Optional canvas name to search for (partial match)
        canvas_type: Optional canvas type filter (story, intro, dialogue, tutorial)

    Returns:
        Formatted string with canvas information
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        # Build query
        canvases = project.story_canvases.all()

        if canvas_name:
            canvases = canvases.filter(name__icontains=canvas_name)

        if canvas_type:
            canvases = canvases.filter(canvas_type=canvas_type)

        if not canvases.exists():
            filters_desc = []
            if canvas_name:
                filters_desc.append(f"name containing '{canvas_name}'")
            if canvas_type:
                filters_desc.append(f"type '{canvas_type}'")

            filter_text = " and ".join(filters_desc)
            return f"No story canvases found in project '{project.name}'" + (f" with {filter_text}" if filter_text else "") + "."

        # Format results
        result = f"📖 **Story Canvases in '{project.name}'**"
        if canvas_name or canvas_type:
            filters = []
            if canvas_name:
                filters.append(f"name: '{canvas_name}'")
            if canvas_type:
                filters.append(f"type: '{canvas_type}'")
            result += f" (filtered by {', '.join(filters)})"
        result += f" - {canvases.count()} found\\n\\n"

        for canvas in canvases:
            result += _format_canvas_summary(canvas)
            result += "\\n"

        return result

    except Exception as e:
        return f"Error getting canvas information: {str(e)}"


# Canvas detail helper functions

def _get_canvas_basic_info(canvas: StoryCanvas) -> str:
    """Get basic canvas information."""
    result = f"📖 **{canvas.name}** ({canvas.canvas_type})\\n\\n"
    result += f"**Project:** {canvas.project.name}\\n"
    result += f"**Status:** {canvas.status}\\n"
    result += f"**Nodes:** {canvas.node_count}\\n"
    result += f"**Connections:** {canvas.connection_count}\\n"

    if canvas.description:
        result += f"**Description:** {canvas.description}\\n"

    return result


def _get_canvas_standard_info(canvas: StoryCanvas) -> str:
    """Get standard canvas information."""
    result = f"📖 **{canvas.name}** ({canvas.canvas_type})\\n\\n"

    # Basic info
    result += f"**Project:** {canvas.project.name}\\n"
    result += f"**Status:** {canvas.status}\\n"
    result += f"**Type:** {canvas.canvas_type}\\n"

    if canvas.description:
        result += f"**Description:** {canvas.description}\\n"

    # Content statistics
    result += "\\n**📊 Content Statistics:**\\n"
    result += f"  • Story Nodes: {canvas.node_count}\\n"
    result += f"  • Node Connections: {canvas.connection_count}\\n"

    # Calculate additional stats
    nodes = canvas.nodes.all()
    connections = canvas.connections.all()
    # Story flags removed
    result += f"  • Story Flags: 0\\n"

    if canvas.estimated_play_time:
        result += f"  • Estimated Play Time: {canvas.estimated_play_time} minutes\\n"

    # Node summary
    if nodes.exists():
        result += "\\n**📝 Story Nodes:**\\n"
        for i, node in enumerate(nodes[:5], 1):
            result += f"  {i}. {node.name}\\n"

        if nodes.count() > 5:
            result += f"  ... and {nodes.count() - 5} more nodes\\n"

    # Connection types
    if connections.exists():
        conn_types = connections.values('connection_type').annotate(count=Count('id'))
        result += "\\n**🔗 Connection Types:**\\n"
        for ct in conn_types:
            result += f"  • {ct['connection_type'].title()}: {ct['count']}\\n"

    # Flags summary
    # Flags removed

    # Validation status
    result += "\\n**✅ Validation:**\\n"
    result += f"  • Status: {'Valid' if canvas.is_valid else 'Has Issues'}\\n"

    if not canvas.is_valid and canvas.validation_errors:
        result += f"  • Issues: {len(canvas.validation_errors)} errors\\n"

    return result


def _get_canvas_detailed_info(canvas: StoryCanvas) -> str:
    """Get detailed canvas information."""
    result = _get_canvas_standard_info(canvas)

    # Add detailed node information
    nodes = canvas.nodes.all()
    if nodes.exists():
        result += "\\n**📝 Detailed Node Information:**\\n"

        for node in nodes[:10]:  # Limit to first 10 for readability
            result += f"\\n**{node.name}**\\n"

            # Node content preview
            if node.node_data and isinstance(node.node_data, dict):
                content = node.node_data.get('content', '')
                if content:
                    # Extract text from content (handle rich text)
                    preview = _extract_text_preview(content)
                    if preview:
                        result += f"  Content: {preview[:100]}...\\n"

            # Node connections
            outgoing = NodeConnection.objects.filter(source_node=node).count()
            incoming = NodeConnection.objects.filter(target_node=node).count()
            result += f"  Connections: {incoming} incoming, {outgoing} outgoing\\n"

            # Node tags
            if node.tags:
                result += f"  Tags: {', '.join(node.tags)}\\n"

        if nodes.count() > 10:
            result += f"\\n... and {nodes.count() - 10} more nodes\\n"

    # Detailed connection information
    connections = canvas.connections.all()
    if connections.exists():
        result += "\\n**🔗 Connection Details:**\\n"

        # Connection flow analysis
        entry_points = nodes.filter(incoming_connections__isnull=True).count()
        exit_points = nodes.filter(outgoing_connections__isnull=True).count()

        result += f"  • Entry Points: {entry_points}\\n"
        result += f"  • Exit Points: {exit_points}\\n"
        result += f"  • Average Connections per Node: {connections.count() / nodes.count():.1f}\\n"

        # Sample connections
        result += "\\n  **Sample Connections:**\\n"
        for conn in connections[:5]:
            label_text = f" ({conn.label})" if conn.label else ""
            result += f"    • {conn.source_node.name} → {conn.target_node.name}{label_text}\\n"

    # Detailed flag information removed

    # Canvas metadata
    if canvas.metadata:
        result += "\\n**⚙️ Canvas Metadata:**\\n"
        for key, value in canvas.metadata.items():
            result += f"  • {key}: {value}\\n"

    return result


def _format_canvas_summary(canvas: StoryCanvas) -> str:
    """Format a brief canvas summary."""
    result = f"**{canvas.name}** ({canvas.canvas_type}, {canvas.status})\\n"
    result += f"  • Nodes: {canvas.node_count}, Connections: {canvas.connection_count}\\n"

    if canvas.description:
        desc_preview = canvas.description[:100] + "..." if len(canvas.description) > 100 else canvas.description
        result += f"  • Description: {desc_preview}\\n"

    if canvas.estimated_play_time:
        result += f"  • Est. Play Time: {canvas.estimated_play_time}min\\n"

    return result


def _extract_text_preview(content: Any) -> str:
    """Extract plain text preview from rich content."""
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        # Handle BlockNote or similar rich text format
        if 'blocks' in content:
            text_parts = []
            for block in content['blocks'][:3]:  # First 3 blocks
                if isinstance(block, dict) and 'content' in block:
                    if isinstance(block['content'], list):
                        for item in block['content']:
                            if isinstance(item, dict) and 'text' in item:
                                text_parts.append(item['text'])
                            elif isinstance(item, str):
                                text_parts.append(item)
            return ' '.join(text_parts)
        elif 'text' in content:
            return content['text']
    elif isinstance(content, list):
        # Handle array of content blocks
        text_parts = []
        for item in content[:3]:  # First 3 items
            if isinstance(item, dict) and 'text' in item:
                text_parts.append(item['text'])
            elif isinstance(item, str):
                text_parts.append(item)
        return ' '.join(text_parts)

    return ""
