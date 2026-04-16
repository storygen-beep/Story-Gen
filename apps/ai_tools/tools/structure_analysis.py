"""
Structure Analysis Tools for Elora AI Assistant

Tools for analyzing project structure, connectivity, and relationships between story elements.
"""

from collections import defaultdict, deque
from typing import Any

from django.db.models import Count, Q
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from apps.projects.models import Project
from apps.stories.models import NodeConnection, StoryNode


class StructureAnalysisInput(BaseModel):
    """Input schema for structure analysis."""
    project_id: str = Field(description="The UUID of the project to analyze")
    focus: str = Field(default="all", description="Analysis focus (all, connectivity, complexity, health, relationships, validation)")


class ProjectHealthInput(BaseModel):
    """Input schema for project health validation."""
    project_id: str = Field(description="The UUID of the project to validate")


@tool("analyze_project_structure", args_schema=StructureAnalysisInput)
def analyze_project_structure(project_id: str, focus: str = "all") -> str:
    """
    Analyze project structure, connectivity, and relationships between story elements.

    Args:
        project_id: The UUID of the project to analyze
        focus: Analysis focus (all, connectivity, complexity, health, relationships, validation)

    Returns:
        Formatted string with structural analysis results
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        if focus == "connectivity":
            return _analyze_connectivity(project)
        elif focus == "complexity":
            return _analyze_complexity(project)
        elif focus == "health":
            return _analyze_health(project)
        elif focus == "relationships":
            return _analyze_relationships(project)
        elif focus == "validation":
            return _analyze_validation(project)
        else:  # focus == "all"
            return _analyze_complete_structure(project)

    except Exception as e:
        return f"Error analyzing project structure: {str(e)}"


@tool("validate_project_health", args_schema=ProjectHealthInput)
def validate_project_health(project_id: str) -> str:
    """
    Validate project health and identify potential issues.

    Args:
        project_id: The UUID of the project to validate

    Returns:
        Formatted string with health validation results
    """
    try:
        # Validate project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return f"Project with ID {project_id} not found."

        issues = []
        warnings = []
        successes = []

        # Check for empty project
        canvases = project.story_canvases.all()
        if not canvases.exists():
            issues.append("No story canvases found")
            return _format_health_report(project.name, issues, warnings, successes)

        total_nodes = StoryNode.objects.filter(canvas__project=project).count()
        total_connections = NodeConnection.objects.filter(canvas__project=project).count()

        # Connectivity validation
        connectivity_results = _validate_connectivity(project)
        issues.extend(connectivity_results['issues'])
        warnings.extend(connectivity_results['warnings'])
        successes.extend(connectivity_results['successes'])

        # Content validation
        content_results = _validate_content(project)
        issues.extend(content_results['issues'])
        warnings.extend(content_results['warnings'])
        successes.extend(content_results['successes'])

        # Structure validation
        structure_results = _validate_structure(project)
        issues.extend(structure_results['issues'])
        warnings.extend(structure_results['warnings'])
        successes.extend(structure_results['successes'])

        return _format_health_report(project.name, issues, warnings, successes)

    except Exception as e:
        return f"Error validating project health: {str(e)}"


# Analysis helper functions

def _analyze_complete_structure(project: Project) -> str:
    """Perform complete structural analysis."""
    result = f"🏗️ **Complete Structure Analysis for '{project.name}'**\\n\\n"

    # Basic metrics
    canvases = project.story_canvases.all()
    nodes = StoryNode.objects.filter(canvas__project=project)
    connections = NodeConnection.objects.filter(canvas__project=project)

    result += "**📊 Basic Metrics:**\\n"
    result += f"  • Story Canvases: {canvases.count()}\\n"
    result += f"  • Story Nodes: {nodes.count()}\\n"
    result += f"  • Node Connections: {connections.count()}\\n"

    if nodes.count() > 0:
        avg_connections = connections.count() / nodes.count()
        result += f"  • Avg Connections per Node: {avg_connections:.2f}\\n"

    # Connectivity analysis
    connectivity = _analyze_connectivity_metrics(project)
    result += "\\n**🔗 Connectivity Analysis:**\\n"
    result += f"  • Reachable Nodes: {connectivity['reachable_percentage']:.1f}%\\n"
    result += f"  • Isolated Nodes: {connectivity['isolated_count']}\\n"
    result += f"  • Dead Ends: {connectivity['dead_ends']}\\n"
    result += f"  • Circular References: {connectivity['circular_refs']}\\n"

    # Complexity metrics
    complexity = _analyze_complexity_metrics(project)
    result += "\\n**🧩 Complexity Metrics:**\\n"
    result += f"  • Branching Factor: {complexity['avg_branching']:.2f}\\n"
    result += f"  • Max Depth: {complexity['max_depth']}\\n"
    result += f"  • Decision Points: {complexity['decision_points']}\\n"
    result += f"  • Complexity Score: {complexity['score']:.2f}\\n"

    # Health assessment
    health = _calculate_health_score(project)
    result += "\\n**💚 Health Assessment:**\\n"
    result += f"  • Overall Health Score: {health['score']:.2f}/1.0\\n"
    result += f"  • Status: {health['status']}\\n"

    if health['recommendations']:
        result += "\\n**💡 Recommendations:**\\n"
        for rec in health['recommendations'][:3]:
            result += f"  • {rec}\\n"

    return result


def _analyze_connectivity(project: Project) -> str:
    """Analyze connectivity patterns."""
    result = f"🔗 **Connectivity Analysis for '{project.name}'**\\n\\n"

    connectivity = _analyze_connectivity_metrics(project)

    result += "**Connection Statistics:**\\n"
    result += f"  • Total Connections: {connectivity['total_connections']}\\n"
    result += f"  • Reachable Nodes: {connectivity['reachable_count']}/{connectivity['total_nodes']} ({connectivity['reachable_percentage']:.1f}%)\\n"
    result += f"  • Isolated Nodes: {connectivity['isolated_count']}\\n"
    result += f"  • Dead End Nodes: {connectivity['dead_ends']}\\n"

    if connectivity['isolated_nodes']:
        result += "\\n**🔍 Isolated Nodes:**\\n"
        for node_name in connectivity['isolated_nodes'][:5]:
            result += f"  • {node_name}\\n"
        if len(connectivity['isolated_nodes']) > 5:
            result += f"  • ... and {len(connectivity['isolated_nodes']) - 5} more\\n"

    if connectivity['dead_end_nodes']:
        result += "\\n**🚫 Dead End Nodes:**\\n"
        for node_name in connectivity['dead_end_nodes'][:5]:
            result += f"  • {node_name}\\n"
        if len(connectivity['dead_end_nodes']) > 5:
            result += f"  • ... and {len(connectivity['dead_end_nodes']) - 5} more\\n"

    # Connection type analysis
    connections = NodeConnection.objects.filter(canvas__project=project)
    conn_types = connections.values('connection_type').annotate(count=Count('id'))

    if conn_types:
        result += "\\n**Connection Types:**\\n"
        for ct in conn_types:
            result += f"  • {ct['connection_type'].title()}: {ct['count']}\\n"

    return result


def _analyze_complexity(project: Project) -> str:
    """Analyze complexity patterns."""
    result = f"🧩 **Complexity Analysis for '{project.name}'**\\n\\n"

    complexity = _analyze_complexity_metrics(project)

    result += "**Complexity Metrics:**\\n"
    result += f"  • Average Branching Factor: {complexity['avg_branching']:.2f}\\n"
    result += f"  • Maximum Depth: {complexity['max_depth']}\\n"
    result += f"  • Decision Points: {complexity['decision_points']}\\n"
    result += f"  • Linear Sequences: {complexity['linear_sequences']}\\n"
    result += f"  • Overall Complexity Score: {complexity['score']:.2f}/1.0\\n"

    # Complexity assessment
    if complexity['score'] < 0.3:
        assessment = "Low complexity - story may be too linear"
    elif complexity['score'] < 0.7:
        assessment = "Moderate complexity - well-balanced structure"
    else:
        assessment = "High complexity - may be overwhelming for players"

    result += f"\\n**Assessment:** {assessment}\\n"

    # Most complex nodes
    if complexity['complex_nodes']:
        result += "\\n**Most Complex Nodes:**\\n"
        for node_name, branching in complexity['complex_nodes'][:5]:
            result += f"  • {node_name}: {branching} outgoing connections\\n"

    return result


def _analyze_health(project: Project) -> str:
    """Analyze overall project health."""
    result = f"💚 **Health Analysis for '{project.name}'**\\n\\n"

    health = _calculate_health_score(project)

    result += f"**Overall Health Score: {health['score']:.2f}/1.0**\\n"
    result += f"**Status: {health['status']}**\\n\\n"

    # Health components
    result += "**Health Components:**\\n"
    for component, score in health['components'].items():
        result += f"  • {component}: {score:.2f}\\n"

    # Issues and recommendations
    if health['issues']:
        result += "\\n**❌ Issues Found:**\\n"
        for issue in health['issues']:
            result += f"  • {issue}\\n"

    if health['warnings']:
        result += "\\n**⚠️ Warnings:**\\n"
        for warning in health['warnings']:
            result += f"  • {warning}\\n"

    if health['recommendations']:
        result += "\\n**💡 Recommendations:**\\n"
        for rec in health['recommendations']:
            result += f"  • {rec}\\n"

    return result


def _analyze_relationships(project: Project) -> str:
    """Analyze relationships between project elements."""
    result = f"🕸️ **Relationship Analysis for '{project.name}'**\\n\\n"

    # Canvas relationships
    canvases = project.story_canvases.all()
    result += "**Canvas Relationships:**\\n"

    for canvas in canvases:
        nodes = canvas.nodes.all()
        connections = canvas.connections.all()

        # Inter-canvas connections
        inter_canvas_connections = connections.filter(
            ~Q(source_node__canvas=canvas) | ~Q(target_node__canvas=canvas)
        ).count()

        result += f"  • {canvas.name}: {nodes.count()} nodes, {connections.count()} connections"
        if inter_canvas_connections > 0:
            result += f" ({inter_canvas_connections} cross-canvas)"
        result += "\\n"

    # Character-location relationships
    from apps.npcs.models import NPC
    from apps.world.models import Location

    npcs = NPC.objects.filter(project=project)
    locations = Location.objects.filter(project=project)

    result += "\\n**Character-Location Relationships:**\\n"
    result += f"  • Total NPCs: {npcs.count()}\\n"
    result += f"  • Total Locations: {locations.count()}\\n"

    # NPCs per location
    location_npc_counts = npcs.values('location__name').annotate(count=Count('id'))
    if location_npc_counts:
        result += "\\n**NPCs by Location:**\\n"
        for loc in location_npc_counts[:5]:
            location_name = loc['location__name'] or 'Unassigned'
            result += f"  • {location_name}: {loc['count']} NPCs\\n"

    return result


def _analyze_validation(project: Project) -> str:
    """Perform validation analysis."""
    result = f"✅ **Validation Analysis for '{project.name}'**\\n\\n"

    validation = _validate_connectivity(project)

    result += "**Validation Results:**\\n"

    if validation['successes']:
        result += "\\n**✅ Passed Checks:**\\n"
        for success in validation['successes']:
            result += f"  • {success}\\n"

    if validation['warnings']:
        result += "\\n**⚠️ Warnings:**\\n"
        for warning in validation['warnings']:
            result += f"  • {warning}\\n"

    if validation['issues']:
        result += "\\n**❌ Issues:**\\n"
        for issue in validation['issues']:
            result += f"  • {issue}\\n"

    return result


# Detailed analysis helper functions

def _analyze_connectivity_metrics(project: Project) -> dict[str, Any]:
    """Calculate connectivity metrics."""
    nodes = list(StoryNode.objects.filter(canvas__project=project))
    connections = list(NodeConnection.objects.filter(canvas__project=project).select_related('source_node', 'target_node'))

    if not nodes:
        return {
            'total_nodes': 0,
            'total_connections': 0,
            'reachable_count': 0,
            'reachable_percentage': 0,
            'isolated_count': 0,
            'dead_ends': 0,
            'circular_refs': 0,
            'isolated_nodes': [],
            'dead_end_nodes': [],
        }

    # Build adjacency graph
    graph = defaultdict(list)
    incoming = defaultdict(int)

    for conn in connections:
        graph[conn.source_node.id].append(conn.target_node.id)
        incoming[conn.target_node.id] += 1

    # Find reachable nodes from start nodes (nodes with no incoming connections)
    start_nodes = [node.id for node in nodes if incoming[node.id] == 0]
    if not start_nodes:
        start_nodes = [nodes[0].id]  # Use first node as start if no clear start

    reachable = set()
    for start in start_nodes:
        visited = set()
        queue = deque([start])
        while queue:
            node_id = queue.popleft()
            if node_id not in visited:
                visited.add(node_id)
                reachable.add(node_id)
                queue.extend(graph[node_id])

    # Find isolated and dead end nodes
    node_ids = set(node.id for node in nodes)
    isolated_ids = node_ids - reachable
    dead_end_ids = [node_id for node_id in node_ids if not graph[node_id] and incoming[node_id] > 0]

    # Get node names for reporting
    id_to_name = {node.id: node.name for node in nodes}
    isolated_names = [id_to_name[nid] for nid in isolated_ids]
    dead_end_names = [id_to_name[nid] for nid in dead_end_ids]

    return {
        'total_nodes': len(nodes),
        'total_connections': len(connections),
        'reachable_count': len(reachable),
        'reachable_percentage': (len(reachable) / len(nodes)) * 100,
        'isolated_count': len(isolated_ids),
        'dead_ends': len(dead_end_ids),
        'circular_refs': 0,  # TODO: Implement circular reference detection
        'isolated_nodes': isolated_names,
        'dead_end_nodes': dead_end_names,
    }


def _analyze_complexity_metrics(project: Project) -> dict[str, Any]:
    """Calculate complexity metrics."""
    nodes = StoryNode.objects.filter(canvas__project=project)
    connections = NodeConnection.objects.filter(canvas__project=project)

    if not nodes.exists():
        return {
            'avg_branching': 0,
            'max_depth': 0,
            'decision_points': 0,
            'linear_sequences': 0,
            'score': 0,
            'complex_nodes': [],
        }

    # Calculate branching factors
    branching_factors = []
    complex_nodes = []
    decision_points = 0

    for node in nodes:
        outgoing = connections.filter(source_node=node).count()
        branching_factors.append(outgoing)

        if outgoing > 1:
            decision_points += 1
            complex_nodes.append((node.name, outgoing))

    avg_branching = sum(branching_factors) / len(branching_factors) if branching_factors else 0
    max_branching = max(branching_factors) if branching_factors else 0

    # Sort complex nodes by branching factor
    complex_nodes.sort(key=lambda x: x[1], reverse=True)

    # Calculate complexity score (0-1)
    # Based on average branching, decision points, and connection density
    connection_density = connections.count() / (nodes.count() ** 2) if nodes.count() > 1 else 0

    score = min(1.0, (avg_branching * 0.4) + (decision_points / nodes.count() * 0.4) + (connection_density * 0.2))

    return {
        'avg_branching': avg_branching,
        'max_depth': 0,  # TODO: Calculate actual depth
        'decision_points': decision_points,
        'linear_sequences': nodes.count() - decision_points,
        'score': score,
        'complex_nodes': complex_nodes,
    }


def _calculate_health_score(project: Project) -> dict[str, Any]:
    """Calculate overall health score."""
    canvases = project.story_canvases.all()

    if not canvases.exists():
        return {
            'score': 0.0,
            'status': 'Empty Project',
            'components': {},
            'issues': ['No story canvases found'],
            'warnings': [],
            'recommendations': ['Create your first story canvas'],
        }

    # Calculate component scores
    connectivity = _analyze_connectivity_metrics(project)
    complexity = _analyze_complexity_metrics(project)

    # Component scores (0-1)
    connectivity_score = connectivity['reachable_percentage'] / 100
    complexity_score = min(1.0, max(0.0, 1.0 - abs(complexity['score'] - 0.5) * 2))  # Optimal around 0.5
    completeness_score = min(1.0, canvases.count() / 5)  # Assume 5+ canvases is good

    components = {
        'Connectivity': connectivity_score,
        'Complexity': complexity_score,
        'Completeness': completeness_score,
    }

    # Overall score
    overall_score = sum(components.values()) / len(components)

    # Determine status
    if overall_score >= 0.8:
        status = 'Excellent'
    elif overall_score >= 0.6:
        status = 'Good'
    elif overall_score >= 0.4:
        status = 'Fair'
    else:
        status = 'Needs Improvement'

    # Generate issues and recommendations
    issues = []
    warnings = []
    recommendations = []

    if connectivity_score < 0.7:
        issues.append(f"Only {connectivity['reachable_percentage']:.1f}% of nodes are reachable")
        recommendations.append("Connect isolated nodes to main story flow")

    if connectivity['dead_ends'] > connectivity['total_nodes'] * 0.2:
        warnings.append(f"{connectivity['dead_ends']} dead end nodes found")
        recommendations.append("Add alternative paths or endings to dead end nodes")

    if complexity_score < 0.5:
        if complexity['score'] < 0.3:
            warnings.append("Story may be too linear")
            recommendations.append("Add more choice points and branching paths")
        else:
            warnings.append("Story may be too complex")
            recommendations.append("Consider simplifying some complex sections")

    return {
        'score': overall_score,
        'status': status,
        'components': components,
        'issues': issues,
        'warnings': warnings,
        'recommendations': recommendations,
    }


# Validation helper functions

def _validate_connectivity(project: Project) -> dict[str, list[str]]:
    """Validate connectivity and return categorized results."""
    issues = []
    warnings = []
    successes = []

    connectivity = _analyze_connectivity_metrics(project)

    # Check basic connectivity
    if connectivity['total_nodes'] == 0:
        issues.append("No story nodes found")
    elif connectivity['total_connections'] == 0:
        issues.append("No connections between story nodes")
    else:
        successes.append(f"Found {connectivity['total_connections']} connections between {connectivity['total_nodes']} nodes")

    # Check reachability
    if connectivity['reachable_percentage'] < 70:
        issues.append(f"Only {connectivity['reachable_percentage']:.1f}% of nodes are reachable")
    elif connectivity['reachable_percentage'] < 90:
        warnings.append(f"{connectivity['reachable_percentage']:.1f}% of nodes are reachable")
    else:
        successes.append(f"Excellent connectivity: {connectivity['reachable_percentage']:.1f}% of nodes reachable")

    # Check for dead ends
    if connectivity['dead_ends'] > 0:
        if connectivity['dead_ends'] > connectivity['total_nodes'] * 0.2:
            issues.append(f"{connectivity['dead_ends']} dead end nodes (too many)")
        else:
            warnings.append(f"{connectivity['dead_ends']} dead end nodes")
    else:
        successes.append("No dead end nodes found")

    return {
        'issues': issues,
        'warnings': warnings,
        'successes': successes,
    }


def _validate_content(project: Project) -> dict[str, list[str]]:
    """Validate content completeness."""
    issues = []
    warnings = []
    successes = []

    canvases = project.story_canvases.all()

    # Check for empty canvases
    empty_canvases = canvases.filter(node_count=0)
    if empty_canvases.exists():
        warnings.append(f"{empty_canvases.count()} empty story canvases")

    # Check for content in nodes
    nodes_with_content = StoryNode.objects.filter(
        canvas__project=project,
        node_data__isnull=False
    ).exclude(node_data__exact={})

    total_nodes = StoryNode.objects.filter(canvas__project=project).count()

    if total_nodes > 0:
        content_percentage = (nodes_with_content.count() / total_nodes) * 100
        if content_percentage < 50:
            issues.append(f"Only {content_percentage:.1f}% of nodes have content")
        elif content_percentage < 80:
            warnings.append(f"{content_percentage:.1f}% of nodes have content")
        else:
            successes.append(f"{content_percentage:.1f}% of nodes have content")

    return {
        'issues': issues,
        'warnings': warnings,
        'successes': successes,
    }


def _validate_structure(project: Project) -> dict[str, list[str]]:
    """Validate structural integrity."""
    issues = []
    warnings = []
    successes = []

    canvases = project.story_canvases.all()

    # Check for balanced structure
    if canvases.count() == 1:
        warnings.append("Only one story canvas - consider organizing into multiple canvases")
    elif canvases.count() > 10:
        warnings.append("Many story canvases - ensure they're well organized")
    else:
        successes.append(f"Well-organized structure with {canvases.count()} canvases")

    return {
        'issues': issues,
        'warnings': warnings,
        'successes': successes,
    }


def _format_health_report(project_name: str, issues: list[str], warnings: list[str], successes: list[str]) -> str:
    """Format health validation report."""
    result = f"🏥 **Health Validation for '{project_name}'**\\n\\n"

    # Overall status
    if issues:
        result += "**Status: ❌ Issues Found**\\n"
    elif warnings:
        result += "**Status: ⚠️ Warnings Present**\\n"
    else:
        result += "**Status: ✅ Healthy**\\n"

    # Detailed results
    if successes:
        result += f"\\n**✅ Passed Checks ({len(successes)}):**\\n"
        for success in successes:
            result += f"  • {success}\\n"

    if warnings:
        result += f"\\n**⚠️ Warnings ({len(warnings)}):**\\n"
        for warning in warnings:
            result += f"  • {warning}\\n"

    if issues:
        result += f"\\n**❌ Issues ({len(issues)}):**\\n"
        for issue in issues:
            result += f"  • {issue}\\n"

    return result
