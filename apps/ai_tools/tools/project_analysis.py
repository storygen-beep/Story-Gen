"""
LangChain AI Tools for Story Generation Project Analysis

Provides AI agents with comprehensive project understanding capabilities.
Simplified Django integration without complex setup.
"""

import logging

from langchain_core.tools import tool

from apps.ai_tools.services.analysis_service import AnalysisService

logger = logging.getLogger(__name__)


@tool
def analyze_project(project_id: str, analysis_depth: str = "standard") -> str:
    """
    Analyze a story generation project comprehensively.

    This tool provides deep analysis of project complexity, health, and AI enhancement potential.
    Perfect for understanding project structure, content quality, and improvement opportunities.

    Args:
        project_id: UUID of the project to analyze
        analysis_depth: Level of analysis detail (minimal, standard, comprehensive, expert)

    Returns:
        Formatted analysis report with scores, insights, and recommendations
    """
    try:
        analysis_service = AnalysisService()

        # Get comprehensive analysis data
        complexity_analysis = analysis_service.analyze_project_complexity(project_id)
        health_assessment = analysis_service.assess_project_health(project_id)
        generation_potential = analysis_service.get_project_generation_potential(project_id)

        # Format results based on analysis depth
        if analysis_depth == "minimal":
            return _format_minimal_analysis(complexity_analysis, health_assessment, generation_potential)
        elif analysis_depth == "comprehensive":
            return _format_comprehensive_analysis(complexity_analysis, health_assessment, generation_potential)
        elif analysis_depth == "expert":
            return _format_expert_analysis(complexity_analysis, health_assessment, generation_potential)
        else:  # standard
            return _format_standard_analysis(complexity_analysis, health_assessment, generation_potential)

    except Exception as e:
        logger.error(f"Project analysis failed: {e}")
        return f"❌ Failed to analyze project {project_id}: {str(e)}"


@tool
def get_project_summary(project_id: str) -> str:
    """
    Get a quick summary of a story generation project.

    Provides essential project information and basic metrics without deep analysis.
    Ideal for quick project overviews and screening.

    Args:
        project_id: UUID of the project to summarize

    Returns:
        Concise project summary with key statistics
    """
    try:
        analysis_service = AnalysisService()

        # Get basic complexity analysis (contains project stats)
        complexity = analysis_service.analyze_project_complexity(project_id)

        project_name = complexity['project_name']
        stats = complexity['project_stats']
        overall_complexity = complexity['overall_complexity']

        summary = f"📋 Project Summary: {project_name}\n"
        summary += "═══════════════════════════════════════\n\n"

        summary += f"🎯 Overall Complexity: {overall_complexity['score']}/100 ({overall_complexity['level']})\n"
        summary += "📊 Content Statistics:\n"
        summary += f"   • {stats['canvas_count']} story canvases\n"
        summary += f"   • {stats['node_count']} story nodes\n"
        summary += f"   • {stats['connection_count']} connections\n"
        summary += f"   • {stats['character_count']} characters\n"
        summary += f"   • {stats['location_count']} locations\n"
        summary += f"   • {stats['total_content_length']:,} characters of content\n\n"

        # Quick assessment
        if overall_complexity['score'] >= 60:
            summary += "✨ This is a well-developed project with good complexity.\n"
        elif overall_complexity['score'] >= 30:
            summary += "🔨 This project has basic structure and room for expansion.\n"
        else:
            summary += "🌱 This is an early-stage project requiring development.\n"

        return summary

    except Exception as e:
        logger.error(f"Project summary failed: {e}")
        return f"❌ Failed to get summary for project {project_id}: {str(e)}"


@tool
def assess_project_complexity(project_id: str) -> str:
    """
    Detailed complexity assessment of a story generation project.

    Analyzes structural, content, and relationship complexity across multiple dimensions.
    Provides specific scores and detailed breakdown for each complexity component.

    Args:
        project_id: UUID of the project to assess

    Returns:
        Detailed complexity breakdown with component scores
    """
    try:
        analysis_service = AnalysisService()
        complexity = analysis_service.analyze_project_complexity(project_id)

        result = f"🧮 Complexity Assessment: {complexity['project_name']}\n"
        result += "═══════════════════════════════════════════════\n\n"

        # Overall complexity
        overall = complexity['overall_complexity']
        result += f"🎯 Overall Complexity: {overall['score']}/100 ({overall['level']})\n"
        result += f"   {overall['description']}\n\n"

        # Detailed breakdown
        result += "📊 Detailed Breakdown:\n\n"

        # Structural complexity
        structural = complexity['structural_complexity']
        result += f"🏗️  Structural Complexity: {structural['score']}/100 ({structural['level']})\n"
        if 'components' in structural:
            components = structural['components']
            result += f"   • Canvas organization: {components.get('canvas_complexity', 0)}/30\n"
            result += f"   • Node complexity: {components.get('node_complexity', 0)}/25\n"
            result += f"   • Connection patterns: {components.get('connection_complexity', 0)}/20\n"
            result += f"   • Component diversity: {components.get('diversity_score', 0)}/25\n"

        result += "\n"

        # Content complexity
        content = complexity['content_complexity']
        result += f"📝 Content Complexity: {content['score']}/100 ({content['level']})\n"
        if 'components' in content:
            components = content['components']
            result += f"   • Content density: {components.get('content_density', 0)}/30\n"
            result += f"   • Character development: {components.get('character_development', 0)}/25\n"
            result += f"   • World building: {components.get('world_building', 0)}/20\n"
            result += f"   • Narrative depth: {components.get('narrative_depth', 0)}/25\n"

        result += "\n"

        # Relationship complexity
        relationship = complexity['relationship_complexity']
        result += f"🔗 Relationship Complexity: {relationship['score']}/100 ({relationship['level']})\n"
        if 'components' in relationship:
            components = relationship['components']
            result += f"   • Connection density: {components.get('connection_density', 0)}/40\n"
            result += f"   • Interaction potential: {components.get('interaction_potential', 0)}/30\n"
            result += f"   • Story flow: {components.get('story_flow', 0)}/30\n"

        # Project statistics
        stats = complexity['project_stats']
        result += "\n📈 Project Statistics:\n"
        result += f"   • Canvases: {stats['canvas_count']}\n"
        result += f"   • Story nodes: {stats['node_count']}\n"
        result += f"   • Connections: {stats['connection_count']} (avg {stats['avg_connections_per_node']:.1f}/node)\n"
        result += f"   • Characters: {stats['character_count']}\n"
        result += f"   • Locations: {stats['location_count']}\n"
        result += f"   • Content volume: {stats['total_content_length']:,} characters\n"
        result += f"   • Component types: {', '.join(stats['component_types'])}\n"

        return result

    except Exception as e:
        logger.error(f"Complexity assessment failed: {e}")
        return f"❌ Failed to assess complexity for project {project_id}: {str(e)}"


@tool
def analyze_multiple_projects(project_ids: list[str], comparison_focus: str = "overview") -> str:
    """
    Comparative analysis of multiple story generation projects.

    Analyzes multiple projects simultaneously and provides comparative insights,
    rankings, and recommendations across the project portfolio.

    Args:
        project_ids: List of project UUIDs to analyze and compare
        comparison_focus: Focus area for comparison (overview, complexity, health, potential)

    Returns:
        Comparative analysis with rankings and insights
    """
    try:
        if len(project_ids) > 10:
            return f"❌ Too many projects requested ({len(project_ids)}). Maximum is 10 projects per comparison."

        analysis_service = AnalysisService()
        results = []

        # Analyze each project
        for project_id in project_ids:
            try:
                complexity = analysis_service.analyze_project_complexity(project_id)
                health = analysis_service.assess_project_health(project_id)
                potential = analysis_service.get_project_generation_potential(project_id)

                results.append({
                    'project_id': project_id,
                    'project_name': complexity['project_name'],
                    'complexity_score': complexity['overall_complexity']['score'],
                    'complexity_level': complexity['overall_complexity']['level'],
                    'health_score': health['overall_health']['score'],
                    'health_level': health['overall_health']['level'],
                    'ai_potential_score': potential['generation_potential']['score'],
                    'ai_potential_level': potential['generation_potential']['level'],
                    'stats': complexity['project_stats']
                })

            except Exception as e:
                logger.warning(f"Failed to analyze project {project_id}: {e}")
                continue

        if not results:
            return "❌ No projects could be analyzed successfully."

        # Format comparison results
        comparison = f"📈 Multi-Project Comparison ({len(results)} projects)\n"
        comparison += "═══════════════════════════════════════════════════\n\n"

        if comparison_focus == "complexity":
            return _format_complexity_comparison(results)
        elif comparison_focus == "health":
            return _format_health_comparison(results)
        elif comparison_focus == "potential":
            return _format_potential_comparison(results)
        else:  # overview
            return _format_overview_comparison(results)

    except Exception as e:
        logger.error(f"Multi-project analysis failed: {e}")
        return f"❌ Failed to analyze multiple projects: {str(e)}"


# Helper functions for formatting analysis results

def _format_minimal_analysis(complexity, health, potential):
    """Format minimal analysis output."""
    project_name = complexity['project_name']

    result = f"📋 {project_name} - Quick Analysis\n"
    result += "═══════════════════════════════════\n\n"
    result += f"🧮 Complexity: {complexity['overall_complexity']['score']}/100 ({complexity['overall_complexity']['level']})\n"
    result += f"🏥 Health: {health['overall_health']['score']}/100 ({health['overall_health']['level']})\n"
    result += f"🚀 AI Potential: {potential['generation_potential']['score']}/100 ({potential['generation_potential']['level']})\n"

    return result


def _format_standard_analysis(complexity, health, potential):
    """Format standard analysis output."""
    project_name = complexity['project_name']

    result = f"📊 {project_name} - Standard Analysis\n"
    result += "═══════════════════════════════════════════\n\n"

    # Complexity summary
    result += "🧮 Complexity Analysis:\n"
    result += f"   Overall: {complexity['overall_complexity']['score']}/100 ({complexity['overall_complexity']['level']})\n"
    result += f"   Structural: {complexity['structural_complexity']['score']}/100\n"
    result += f"   Content: {complexity['content_complexity']['score']}/100\n"
    result += f"   Relationships: {complexity['relationship_complexity']['score']}/100\n\n"

    # Health summary
    result += "🏥 Health Assessment:\n"
    result += f"   Overall: {health['overall_health']['score']}/100 ({health['overall_health']['level']})\n"
    result += f"   Completeness: {health['completeness']['score']}/100\n"
    result += f"   Consistency: {health['consistency']['score']}/100\n"
    result += f"   Quality: {health['quality']['score']}/100\n\n"

    # AI Potential summary
    result += "🚀 AI Generation Potential:\n"
    result += f"   Overall: {potential['generation_potential']['score']}/100 ({potential['generation_potential']['level']})\n"
    result += f"   Structure Readiness: {potential['structure_readiness']['score']}/100\n"
    result += f"   Content Readiness: {potential['content_readiness']['score']}/100\n"
    result += f"   Expansion Opportunities: {potential['expansion_opportunities']['score']}/100\n\n"

    # Key statistics
    stats = complexity['project_stats']
    result += "📈 Key Statistics:\n"
    result += f"   • {stats['canvas_count']} canvases, {stats['node_count']} nodes, {stats['connection_count']} connections\n"
    result += f"   • {stats['character_count']} characters, {stats['location_count']} locations\n"
    result += f"   • {stats['total_content_length']:,} characters of content\n\n"

    # Recommendations
    if health.get('recommendations'):
        result += "💡 Health Recommendations:\n"
        for rec in health['recommendations'][:3]:
            result += f"   • {rec}\n"

    if potential.get('ai_recommendations'):
        result += "\n🤖 AI Enhancement Recommendations:\n"
        for rec in potential['ai_recommendations'][:3]:
            result += f"   • {rec}\n"

    return result


def _format_comprehensive_analysis(complexity, health, potential):
    """Format comprehensive analysis output."""
    standard = _format_standard_analysis(complexity, health, potential)

    # Add detailed breakdowns
    result = standard + "\n"
    result += "🔍 Detailed Component Analysis:\n"
    result += "═══════════════════════════════════════\n\n"

    # Detailed complexity components
    if 'components' in complexity['structural_complexity']:
        components = complexity['structural_complexity']['components']
        result += "🏗️  Structural Components:\n"
        for key, value in components.items():
            result += f"   • {key.replace('_', ' ').title()}: {value}\n"

    # Expansion opportunities
    if potential.get('expansion_opportunities', {}).get('opportunities'):
        result += "\n📈 Expansion Opportunities:\n"
        for opp in potential['expansion_opportunities']['opportunities']:
            result += f"   • {opp}\n"

    return result


def _format_expert_analysis(complexity, health, potential):
    """Format expert-level analysis output."""
    comprehensive = _format_comprehensive_analysis(complexity, health, potential)

    # Add expert-level insights
    result = comprehensive + "\n"
    result += "🎓 Expert Analysis:\n"
    result += "═══════════════════════\n\n"

    # AI readiness factors
    if potential.get('structure_readiness', {}).get('factors'):
        result += "🚀 AI Structure Readiness Factors:\n"
        for factor in potential['structure_readiness']['factors']:
            result += f"   • {factor}\n"

    if potential.get('content_readiness', {}).get('factors'):
        result += "\n📝 AI Content Readiness Factors:\n"
        for factor in potential['content_readiness']['factors']:
            result += f"   • {factor}\n"

    # Technical metrics
    stats = complexity['project_stats']
    result += "\n📊 Technical Metrics:\n"
    result += f"   • Content density: {stats['total_content_length'] / max(stats['node_count'], 1):.1f} chars/node\n"
    result += f"   • Connection density: {stats['avg_connections_per_node']:.2f} connections/node\n"
    result += f"   • Character ratio: {stats['character_count'] / max(stats['node_count'], 1):.2f} characters/node\n"
    result += f"   • Component diversity: {stats['component_diversity']}/4 types\n"

    return result


def _format_overview_comparison(results):
    """Format overview comparison of multiple projects."""
    comparison = "📈 Project Portfolio Overview\n"
    comparison += "═══════════════════════════════════\n\n"

    # Sort by overall score (average of complexity, health, AI potential)
    for result in results:
        result['overall_score'] = (
            result['complexity_score'] +
            result['health_score'] +
            result['ai_potential_score']
        ) / 3

    sorted_results = sorted(results, key=lambda x: x['overall_score'], reverse=True)

    comparison += "🏆 Project Rankings (by overall score):\n\n"

    for i, result in enumerate(sorted_results, 1):
        comparison += f"{i}. {result['project_name']} (Overall: {result['overall_score']:.1f}/100)\n"
        comparison += f"   🧮 Complexity: {result['complexity_score']}/100 ({result['complexity_level']})\n"
        comparison += f"   🏥 Health: {result['health_score']}/100 ({result['health_level']})\n"
        comparison += f"   🚀 AI Potential: {result['ai_potential_score']}/100 ({result['ai_potential_level']})\n"
        comparison += f"   📊 Content: {result['stats']['node_count']} nodes, {result['stats']['character_count']} characters\n\n"

    # Portfolio statistics
    avg_complexity = sum(r['complexity_score'] for r in results) / len(results)
    avg_health = sum(r['health_score'] for r in results) / len(results)
    avg_potential = sum(r['ai_potential_score'] for r in results) / len(results)

    comparison += "📊 Portfolio Averages:\n"
    comparison += f"   • Complexity: {avg_complexity:.1f}/100\n"
    comparison += f"   • Health: {avg_health:.1f}/100\n"
    comparison += f"   • AI Potential: {avg_potential:.1f}/100\n\n"

    # Recommendations
    top_project = sorted_results[0]
    comparison += "💡 Portfolio Insights:\n"
    comparison += f"   • Strongest project: {top_project['project_name']} ({top_project['overall_score']:.1f}/100)\n"

    if avg_complexity < 40:
        comparison += "   • Focus on increasing complexity across projects\n"
    if avg_health < 50:
        comparison += "   • Improve content quality and completeness\n"
    if avg_potential > 60:
        comparison += "   • Portfolio is ready for AI enhancement\n"

    return comparison


def _format_complexity_comparison(results):
    """Format complexity-focused comparison."""
    sorted_results = sorted(results, key=lambda x: x['complexity_score'], reverse=True)

    comparison = "🧮 Complexity Comparison\n"
    comparison += "═══════════════════════════\n\n"

    for i, result in enumerate(sorted_results, 1):
        comparison += f"{i}. {result['project_name']}: {result['complexity_score']}/100 ({result['complexity_level']})\n"
        stats = result['stats']
        comparison += f"   📊 {stats['node_count']} nodes, {stats['connection_count']} connections, {stats['character_count']} characters\n\n"

    return comparison


def _format_health_comparison(results):
    """Format health-focused comparison."""
    sorted_results = sorted(results, key=lambda x: x['health_score'], reverse=True)

    comparison = "🏥 Health Comparison\n"
    comparison += "═══════════════════════\n\n"

    for i, result in enumerate(sorted_results, 1):
        comparison += f"{i}. {result['project_name']}: {result['health_score']}/100 ({result['health_level']})\n"
        stats = result['stats']
        content_density = stats['total_content_length'] / max(stats['node_count'], 1)
        comparison += f"   📝 Content density: {content_density:.0f} chars/node\n\n"

    return comparison


def _format_potential_comparison(results):
    """Format AI potential-focused comparison."""
    sorted_results = sorted(results, key=lambda x: x['ai_potential_score'], reverse=True)

    comparison = "🚀 AI Potential Comparison\n"
    comparison += "═══════════════════════════\n\n"

    for i, result in enumerate(sorted_results, 1):
        comparison += f"{i}. {result['project_name']}: {result['ai_potential_score']}/100 ({result['ai_potential_level']})\n"

        if result['ai_potential_score'] > 70:
            comparison += "   ✨ Ready for AI enhancement\n"
        elif result['ai_potential_score'] > 50:
            comparison += "   🔨 Good candidate with some preparation needed\n"
        else:
            comparison += "   🌱 Needs foundational work before AI enhancement\n"
        comparison += "\n"

    return comparison
