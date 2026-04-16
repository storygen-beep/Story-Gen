"""
Content Search Tools for Elora AI Assistant

Tools for searching text content across all project entities and story elements.
"""

from typing import Any

from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from apps.npcs.models import NPC
from apps.projects.models import Project
from apps.stories.models import NodeConnection, StoryNode
from apps.world.models import Location


class ContentSearchInput(BaseModel):
    """Input schema for content search."""
    project_id: str = Field(description="The UUID of the project to search within")
    search_query: str = Field(description="Text to search for (supports partial matches)")
    content_types: str = Field(default="all", description="Filter by content type (all, story, characters, world, metadata)")


class ContentReferenceInput(BaseModel):
    """Input schema for content reference search."""
    project_id: str = Field(description="The UUID of the project to search")
    reference_term: str = Field(description="Specific term to find references for")
    context_length: int = Field(default=100, description="Number of characters to show around each match")


@tool("search_project_content", args_schema=ContentSearchInput)
def search_project_content(project_id: str, search_query: str, content_types: str = "all") -> str:
    """
    Search for text content across all project entities.

    Args:
        project_id: The UUID of the project to search within
        search_query: Text to search for (supports partial matches)
        content_types: Filter by content type (all, story, characters, world, metadata)

    Returns:
        Formatted string with search results and context
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        if not search_query.strip():
            return "Please provide a search query."

        # Perform search across different content types
        results = {
            'story_nodes': [],
            'story_canvases': [],
            'node_connections': [],
            'story_flags': [],
            'characters': [],
            'npcs': [],
            'locations': [],
        }

        search_term = search_query.strip().lower()

        # Search story content
        if content_types in ["all", "story"]:
            results['story_nodes'] = _search_story_nodes(project, search_term)
            results['story_canvases'] = _search_story_canvases(project, search_term)
            results['node_connections'] = _search_node_connections(project, search_term)
            results['story_flags'] = []

        # Search character content
        if content_types in ["all", "characters"]:
            results['characters'] = _search_characters(project, search_term)
            results['npcs'] = _search_npcs(project, search_term)

        # Search world content
        if content_types in ["all", "world"]:
            results['locations'] = _search_locations(project, search_term)

        return _format_search_results(project.name, search_query, results)

    except Exception as e:
        return f"Error searching project content: {str(e)}"


@tool("find_content_references", args_schema=ContentReferenceInput)
def find_content_references(project_id: str, reference_term: str, context_length: int = 100) -> str:
    """
    Find references to a specific term and show surrounding context.

    Args:
        project_id: The UUID of the project to search
        reference_term: Specific term to find references for
        context_length: Number of characters to show around each match

    Returns:
        Formatted string with detailed references and context
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        if not reference_term.strip():
            return "Please provide a reference term to search for."

        search_term = reference_term.strip()
        references = []

        # Search with context extraction
        references.extend(_find_references_in_story_nodes(project, search_term, context_length))
        references.extend(_find_references_in_canvases(project, search_term, context_length))
        references.extend(_find_references_in_characters(project, search_term, context_length))
        references.extend(_find_references_in_npcs(project, search_term, context_length))
        references.extend(_find_references_in_locations(project, search_term, context_length))
        references.extend(_find_references_in_connections(project, search_term, context_length))
        references.extend(_find_references_in_flags(project, search_term, context_length))

        return _format_reference_results(project.name, reference_term, references)

    except Exception as e:
        return f"Error finding content references: {str(e)}"


# Search helper functions for different content types

def _search_story_nodes(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """Search story nodes for content matches."""
    results = []
    nodes = StoryNode.objects.filter(canvas__project=project)

    for node in nodes:
        matches = []

        # Search node name
        if search_term in node.name.lower():
            matches.append(f"name: '{node.name}'")

        # Search node content
        if node.node_data:
            content_text = _extract_searchable_text(node.node_data)
            if content_text and search_term in content_text.lower():
                matches.append("content")

        # Search tags
        if node.tags and any(search_term in tag.lower() for tag in node.tags):
            matching_tags = [tag for tag in node.tags if search_term in tag.lower()]
            matches.append(f"tags: {', '.join(matching_tags)}")

        if matches:
            canvas_name = node.canvas.name if node.canvas else "Unknown Canvas"
            results.append((f"Story Node: {node.name}", canvas_name, "; ".join(matches)))

    return results


def _search_story_canvases(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """Search story canvases for content matches."""
    results = []
    canvases = project.story_canvases.all()

    for canvas in canvases:
        matches = []

        # Search canvas name
        if search_term in canvas.name.lower():
            matches.append(f"name: '{canvas.name}'")

        # Search canvas description
        if canvas.description and search_term in canvas.description.lower():
            matches.append("description")

        # Search tags
        if canvas.tags and any(search_term in tag.lower() for tag in canvas.tags):
            matching_tags = [tag for tag in canvas.tags if search_term in tag.lower()]
            matches.append(f"tags: {', '.join(matching_tags)}")

        # Search metadata
        if canvas.metadata:
            metadata_text = str(canvas.metadata).lower()
            if search_term in metadata_text:
                matches.append("metadata")

        if matches:
            results.append((f"Story Canvas: {canvas.name}", canvas.canvas_type, "; ".join(matches)))

    return results


def _search_node_connections(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """Search node connections for content matches."""
    results = []
    connections = NodeConnection.objects.filter(canvas__project=project)

    for conn in connections:
        matches = []

        # Search connection label
        if conn.label and search_term in conn.label.lower():
            matches.append(f"label: '{conn.label}'")

        # Search connection metadata
        if conn.metadata:
            metadata_text = str(conn.metadata).lower()
            if search_term in metadata_text:
                matches.append("metadata")

        if matches:
            connection_desc = f"{conn.source_node.name} → {conn.target_node.name}"
            canvas_name = conn.canvas.name if conn.canvas else "Unknown Canvas"
            results.append((f"Connection: {connection_desc}", canvas_name, "; ".join(matches)))

    return results


def _search_story_flags(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """StoryFlag removed: return empty list."""
    return []


def _search_characters(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """Search player character for content matches."""
    results = []

    if hasattr(project, 'player_character') and project.player_character:
        character = project.player_character
        matches = []

        # Search character name
        if search_term in character.name.lower():
            matches.append(f"name: '{character.name}'")

        # Search character description
        if character.description and search_term in character.description.lower():
            matches.append("description")

        # Search character metadata
        if character.metadata:
            metadata_text = str(character.metadata).lower()
            if search_term in metadata_text:
                matches.append("metadata")

        if matches:
            results.append((f"Player Character: {character.name}", "Character", "; ".join(matches)))

    return results


def _search_npcs(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """Search NPCs for content matches."""
    results = []
    npcs = NPC.objects.filter(project=project)

    for npc in npcs:
        matches = []

        # Search NPC name
        if search_term in npc.name.lower():
            matches.append(f"name: '{npc.name}'")

        # Search NPC description
        if npc.description and search_term in npc.description.lower():
            matches.append("description")

        # Search NPC metadata
        if npc.metadata:
            metadata_text = str(npc.metadata).lower()
            if search_term in metadata_text:
                matches.append("metadata")

        if matches:
            location_name = npc.location.name if npc.location else "No Location"
            results.append((f"NPC: {npc.name}", location_name, "; ".join(matches)))

    return results


def _search_locations(project: Project, search_term: str) -> list[tuple[str, str, str]]:
    """Search locations for content matches."""
    results = []
    locations = Location.objects.filter(project=project)

    for location in locations:
        matches = []

        # Search location name
        if search_term in location.name.lower():
            matches.append(f"name: '{location.name}'")

        # Search location description
        if location.description and search_term in location.description.lower():
            matches.append("description")

        # Search location metadata
        if location.metadata:
            metadata_text = str(location.metadata).lower()
            if search_term in metadata_text:
                matches.append("metadata")

        if matches:
            npc_count = NPC.objects.filter(location=location).count()
            context = f"{npc_count} NPCs" if npc_count > 0 else "No NPCs"
            results.append((f"Location: {location.name}", context, "; ".join(matches)))

    return results


# Reference finding functions with context

def _find_references_in_story_nodes(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """Find references in story nodes with context."""
    references = []
    nodes = StoryNode.objects.filter(canvas__project=project)

    for node in nodes:
        # Search in node content
        if node.node_data:
            content_text = _extract_searchable_text(node.node_data)
            if content_text:
                contexts = _extract_contexts(content_text, search_term, context_length)
                for context in contexts:
                    references.append({
                        'type': 'Story Node',
                        'name': node.name,
                        'location': node.canvas.name if node.canvas else 'Unknown Canvas',
                        'context': context,
                    })

    return references


def _find_references_in_canvases(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """Find references in canvas descriptions with context."""
    references = []
    canvases = project.story_canvases.all()

    for canvas in canvases:
        if canvas.description:
            contexts = _extract_contexts(canvas.description, search_term, context_length)
            for context in contexts:
                references.append({
                    'type': 'Story Canvas',
                    'name': canvas.name,
                    'location': canvas.canvas_type,
                    'context': context,
                })

    return references


def _find_references_in_characters(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """Find references in character descriptions with context."""
    references = []

    if hasattr(project, 'player_character') and project.player_character:
        character = project.player_character
        if character.description:
            contexts = _extract_contexts(character.description, search_term, context_length)
            for context in contexts:
                references.append({
                    'type': 'Player Character',
                    'name': character.name,
                    'location': 'Character',
                    'context': context,
                })

    return references


def _find_references_in_npcs(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """Find references in NPC descriptions with context."""
    references = []
    npcs = NPC.objects.filter(project=project)

    for npc in npcs:
        if npc.description:
            contexts = _extract_contexts(npc.description, search_term, context_length)
            for context in contexts:
                references.append({
                    'type': 'NPC',
                    'name': npc.name,
                    'location': npc.location.name if npc.location else 'No Location',
                    'context': context,
                })

    return references


def _find_references_in_locations(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """Find references in location descriptions with context."""
    references = []
    locations = Location.objects.filter(project=project)

    for location in locations:
        if location.description:
            contexts = _extract_contexts(location.description, search_term, context_length)
            for context in contexts:
                references.append({
                    'type': 'Location',
                    'name': location.name,
                    'location': 'World',
                    'context': context,
                })

    return references


def _find_references_in_connections(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """Find references in connection labels with context."""
    references = []
    connections = NodeConnection.objects.filter(canvas__project=project)

    for conn in connections:
        if conn.label and search_term.lower() in conn.label.lower():
            references.append({
                'type': 'Connection',
                'name': f"{conn.source_node.name} → {conn.target_node.name}",
                'location': conn.canvas.name if conn.canvas else 'Unknown Canvas',
                'context': f"Label: '{conn.label}'",
            })

    return references


def _find_references_in_flags(project: Project, search_term: str, context_length: int) -> list[dict[str, Any]]:
    """StoryFlag removed: return empty list."""
    return []


# Utility functions

def _extract_searchable_text(content: Any) -> str:
    """Extract plain text from various content formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        # Handle BlockNote or similar rich text format
        if 'blocks' in content:
            text_parts = []
            for block in content['blocks']:
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
        else:
            # Fallback: stringify the entire dict
            return str(content)
    elif isinstance(content, list):
        # Handle array of content blocks
        text_parts = []
        for item in content:
            if isinstance(item, dict) and 'text' in item:
                text_parts.append(item['text'])
            elif isinstance(item, str):
                text_parts.append(item)
        return ' '.join(text_parts)

    return str(content) if content else ""


def _extract_contexts(text: str, search_term: str, context_length: int) -> list[str]:
    """Extract context around search term matches."""
    contexts = []
    text_lower = text.lower()
    search_lower = search_term.lower()

    # Find all occurrences
    start = 0
    while True:
        pos = text_lower.find(search_lower, start)
        if pos == -1:
            break

        # Extract context around the match
        context_start = max(0, pos - context_length // 2)
        context_end = min(len(text), pos + len(search_term) + context_length // 2)

        context = text[context_start:context_end]

        # Add ellipsis if context is truncated
        if context_start > 0:
            context = "..." + context
        if context_end < len(text):
            context = context + "..."

        contexts.append(context)
        start = pos + 1

    return contexts


def _format_search_results(project_name: str, search_query: str, results: dict[str, list]) -> str:
    """Format search results into readable output."""
    total_matches = sum(len(matches) for matches in results.values())

    if total_matches == 0:
        return f"🔍 **No matches found for '{search_query}' in '{project_name}'**\\n\\nTry using different keywords or checking spelling."

    result = f"🔍 **Search Results for '{search_query}' in '{project_name}'** ({total_matches} matches)\\n\\n"

    # Story content results
    story_matches = len(results['story_nodes']) + len(results['story_canvases']) + len(results['node_connections']) + len(results['story_flags'])
    if story_matches > 0:
        result += f"**📖 Story Content ({story_matches} matches):**\\n"

        for item_name, location, matches in results['story_nodes']:
            result += f"  • {item_name} (in {location}) - {matches}\\n"

        for item_name, location, matches in results['story_canvases']:
            result += f"  • {item_name} ({location}) - {matches}\\n"

        for item_name, location, matches in results['node_connections']:
            result += f"  • {item_name} (in {location}) - {matches}\\n"

        for item_name, location, matches in results['story_flags']:
            result += f"  • {item_name} (in {location}) - {matches}\\n"

        result += "\\n"

    # Character results
    character_matches = len(results['characters']) + len(results['npcs'])
    if character_matches > 0:
        result += f"**👥 Characters ({character_matches} matches):**\\n"

        for item_name, location, matches in results['characters']:
            result += f"  • {item_name} - {matches}\\n"

        for item_name, location, matches in results['npcs']:
            result += f"  • {item_name} (at {location}) - {matches}\\n"

        result += "\\n"

    # World content results
    world_matches = len(results['locations'])
    if world_matches > 0:
        result += f"**🌍 World Content ({world_matches} matches):**\\n"

        for item_name, location, matches in results['locations']:
            result += f"  • {item_name} ({location}) - {matches}\\n"

        result += "\\n"

    return result


def _format_reference_results(project_name: str, reference_term: str, references: list[dict[str, Any]]) -> str:
    """Format reference results with context."""
    if not references:
        return f"🔍 **No references found for '{reference_term}' in '{project_name}'**\\n\\nTry using different keywords or checking spelling."

    result = f"🔍 **References to '{reference_term}' in '{project_name}'** ({len(references)} found)\\n\\n"

    for i, ref in enumerate(references, 1):
        result += f"**{i}. {ref['type']}: {ref['name']}**\\n"
        result += f"   📍 Location: {ref['location']}\\n"
        result += f"   📝 Context: {ref['context']}\\n\\n"

    return result
