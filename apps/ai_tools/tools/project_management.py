"""
Project Management Tools for Elora AI Assistant

Tools for listing and managing projects without requiring project IDs upfront.
"""


from django.db.models import Count
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field

from apps.projects.models import Project


class ProjectNameInput(BaseModel):
    """Input schema for project name search."""
    project_name: str = Field(description="Full or partial project name to search for")


class ListProjectsInput(BaseModel):
    """Input schema for listing projects (no parameters needed)."""
    dummy: str = Field(default="", description="Dummy parameter for agent compatibility")


def _get_all_projects_helper() -> str:
    """Helper function to get all projects - can be called directly."""
    try:
        # Get all projects with canvas counts
        projects = Project.objects.annotate(
            canvas_count=Count('story_canvases'),
        ).values(
            'id', 'name', 'canvas_count', 'created_at'
        ).order_by('-created_at')

        if not projects:
            return "No projects found. You can create your first project to get started!"

        result = f"📚 **All Projects** ({len(projects)} total)\\n\\n"

        for i, project in enumerate(projects, 1):
            canvas_info = f"({project['canvas_count']} canvases)" if project['canvas_count'] else "(no canvases)"
            created_date = project['created_at'].strftime('%Y-%m-%d')
            result += f"{i}. **{project['name']}** {canvas_info}\\n"
            result += f"   📅 Created: {created_date} | 🆔 ID: `{project['id']}`\\n\\n"

        result += "💡 To analyze a specific project, ask: *\"Tell me about [project name]\"* or *\"Analyze project [project name]\"*"

        return result

    except Exception as e:
        return f"Error retrieving projects: {str(e)}"


@tool("list_all_projects", args_schema=ListProjectsInput)
def list_all_projects(dummy: str = "") -> str:
    """
    List all available projects in the system.

    Args:
        dummy: Dummy parameter for agent compatibility (not used)

    Returns:
        Formatted string with all projects and their basic information
    """
    return _get_all_projects_helper()


@tool("get_project_by_name", args_schema=ProjectNameInput)
def get_project_by_name(project_name: str) -> str:
    """
    Find a project by name (supports partial matching).

    Args:
        project_name: Full or partial project name to search for

    Returns:
        Formatted string with project details or search results
    """
    try:
        if not project_name.strip():
            return "Please provide a project name to search for."

        # Search for projects with name containing the search term
        projects = Project.objects.filter(
            name__icontains=project_name.strip()
        ).annotate(
            canvas_count=Count('story_canvases'),
        ).values(
            'id', 'name', 'canvas_count', 'created_at'
        ).order_by('-created_at')

        if not projects:
            return f"No projects found with name containing '{project_name}'. Use **list_all_projects** to see all available projects."

        if len(projects) == 1:
            # Single match - return detailed info
            project = projects[0]
            result = f"📂 **Found Project: {project['name']}**\\n\\n"
            result += f"🆔 **Project ID:** `{project['id']}`\\n"
            result += f"📊 **Story Canvases:** {project['canvas_count']}\\n"
            result += f"📅 **Created:** {project['created_at'].strftime('%Y-%m-%d %H:%M')}\\n\\n"

            result += "💡 To get detailed analysis, ask: *\"Analyze this project\"* or use the project ID with other tools."

            return result
        else:
            # Multiple matches - show list
            result = f"🔍 **Found {len(projects)} projects matching '{project_name}':**\\n\\n"

            for i, project in enumerate(projects, 1):
                canvas_info = f"({project['canvas_count']} canvases)" if project['canvas_count'] else "(no canvases)"
                result += f"{i}. **{project['name']}** {canvas_info}\\n"
                result += f"   🆔 ID: `{project['id']}`\\n\\n"

            result += "💡 To analyze a specific project, use its exact name or project ID."

            return result

    except Exception as e:
        return f"Error searching for project '{project_name}': {str(e)}"


class ProjectSummaryStatsInput(BaseModel):
    """Input schema for project summary stats (no parameters needed)."""
    dummy: str = Field(default="", description="Dummy parameter for agent compatibility")


def _get_project_summary_stats_helper() -> str:
    """Helper function to get project summary stats - can be called directly."""
    try:
        # Get project statistics
        total_projects = Project.objects.count()

        if total_projects == 0:
            return "No projects found in the system."

        # Get projects with detailed stats
        projects_with_stats = Project.objects.annotate(
            canvas_count=Count('story_canvases'),
        ).values('canvas_count', 'created_at')

        # Calculate statistics
        total_canvases = sum(p['canvas_count'] for p in projects_with_stats)
        projects_with_content = sum(1 for p in projects_with_stats if p['canvas_count'] > 0)
        empty_projects = total_projects - projects_with_content

        # Average canvases per project
        avg_canvases = total_canvases / total_projects if total_projects > 0 else 0

        # Most recent project
        recent_project = Project.objects.order_by('-created_at').first()

        # Build result
        result = "📊 **Project Summary Statistics**\\n\\n"

        result += "**📚 Overall Stats:**\\n"
        result += f"  • Total Projects: {total_projects}\\n"
        result += f"  • Projects with Content: {projects_with_content}\\n"
        result += f"  • Empty Projects: {empty_projects}\\n"
        result += f"  • Total Story Canvases: {total_canvases}\\n"
        result += f"  • Average Canvases per Project: {avg_canvases:.1f}\\n\\n"

        if recent_project:
            result += "**📅 Most Recent:**\\n"
            result += f"  • {recent_project.name}\\n"
            result += f"  • Created: {recent_project.created_at.strftime('%Y-%m-%d %H:%M')}\\n\\n"

        # Project activity insights
        result += "**💡 Insights:**\\n"
        if empty_projects > total_projects * 0.5:
            result += "  • Many empty projects - consider adding content or cleaning up\\n"
        elif projects_with_content == total_projects:
            result += "  • All projects have content - excellent activity!\\n"

        if avg_canvases < 1:
            result += "  • Low average content per project - consider expanding stories\\n"
        elif avg_canvases > 5:
            result += "  • Rich content with high canvas count per project\\n"

        result += "\\n💡 Use **list_all_projects** to see individual project details."

        return result

    except Exception as e:
        return f"Error getting project statistics: {str(e)}"


@tool("get_project_summary_stats", args_schema=ProjectSummaryStatsInput)
def get_project_summary_stats(dummy: str = "") -> str:
    """
    Get summary statistics for all projects in the system.

    Args:
        dummy: Dummy parameter for agent compatibility (not used)

    Returns:
        Formatted string with project statistics and insights
    """
    return _get_project_summary_stats_helper()
