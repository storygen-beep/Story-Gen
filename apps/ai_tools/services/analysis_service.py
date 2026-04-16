"""
Analysis Service for AI Tools

Provides comprehensive analysis capabilities for story generation projects.
Simplified Django service without complex setup or configuration.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Union
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import Count

from apps.projects.models import Project

User = get_user_model()
logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for advanced project and user analysis."""

    def analyze_project_complexity(self, project_id: Union[str, UUID]) -> dict[str, Any]:
        """
        Analyze project complexity across multiple dimensions.

        Args:
            project_id: Project UUID

        Returns:
            Dictionary with complexity analysis
        """
        try:
            if isinstance(project_id, str):
                project_id = UUID(project_id)

            project = Project.objects.select_related('owner').prefetch_related(
                'story_canvases__nodes__outgoing_connections',
                'story_canvases__nodes__incoming_connections',
                'locations'  # Character is OneToOne, locations is the correct relationship
            ).get(id=project_id)

            # Get project statistics
            stats = self._calculate_project_stats(project)

            # Calculate complexity scores
            structural = self._assess_structural_complexity(stats)
            content = self._assess_content_complexity(stats)
            relationship = self._assess_relationship_complexity(stats)

            # Calculate overall complexity
            overall_score = (
                structural['score'] * 0.4 +
                content['score'] * 0.3 +
                relationship['score'] * 0.3
            )

            complexity_level = self._get_complexity_level(overall_score)

            return {
                'project_id': str(project_id),
                'project_name': project.name,
                'overall_complexity': {
                    'score': round(overall_score, 1),
                    'level': complexity_level,
                    'description': self._get_complexity_description(complexity_level)
                },
                'structural_complexity': structural,
                'content_complexity': content,
                'relationship_complexity': relationship,
                'project_stats': stats,
                'analysis_timestamp': datetime.now().isoformat()
            }

        except Project.DoesNotExist:
            logger.error(f"Project not found: {project_id}")
            raise ValueError(f"Project {project_id} not found")
        except Exception as e:
            logger.error(f"Error analyzing project complexity: {e}")
            raise

    def assess_project_health(self, project_id: Union[str, UUID]) -> dict[str, Any]:
        """
        Assess project health and completeness.

        Args:
            project_id: Project UUID

        Returns:
            Dictionary with health assessment
        """
        try:
            if isinstance(project_id, str):
                project_id = UUID(project_id)

            project = Project.objects.select_related('owner').prefetch_related(
                'story_canvases__nodes',
                'locations'
            ).get(id=project_id)

            # Calculate health metrics
            completeness = self._assess_completeness(project)
            consistency = self._assess_consistency(project)
            quality = self._assess_quality(project)

            # Calculate overall health
            overall_score = (
                completeness['score'] * 0.4 +
                consistency['score'] * 0.3 +
                quality['score'] * 0.3
            )

            health_level = self._get_health_level(overall_score)

            return {
                'project_id': str(project_id),
                'project_name': project.name,
                'overall_health': {
                    'score': round(overall_score, 1),
                    'level': health_level,
                    'description': self._get_health_description(health_level)
                },
                'completeness': completeness,
                'consistency': consistency,
                'quality': quality,
                'recommendations': self._generate_health_recommendations(overall_score, completeness, consistency, quality),
                'analysis_timestamp': datetime.now().isoformat()
            }

        except Project.DoesNotExist:
            logger.error(f"Project not found: {project_id}")
            raise ValueError(f"Project {project_id} not found")
        except Exception as e:
            logger.error(f"Error assessing project health: {e}")
            raise

    def get_project_generation_potential(self, project_id: Union[str, UUID]) -> dict[str, Any]:
        """
        Assess project's potential for AI enhancement.

        Args:
            project_id: Project UUID

        Returns:
            Dictionary with generation potential analysis
        """
        try:
            if isinstance(project_id, str):
                project_id = UUID(project_id)

            # Get complexity and health data
            complexity = self.analyze_project_complexity(project_id)
            health = self.assess_project_health(project_id)

            # Calculate AI potential based on various factors
            structure_readiness = self._assess_structure_readiness(complexity)
            content_readiness = self._assess_content_readiness(complexity, health)
            expansion_opportunities = self._identify_expansion_opportunities(complexity)

            # Calculate overall potential
            potential_score = (
                structure_readiness['score'] * 0.4 +
                content_readiness['score'] * 0.35 +
                expansion_opportunities['score'] * 0.25
            )

            potential_level = self._get_potential_level(potential_score)

            return {
                'project_id': str(project_id),
                'project_name': complexity['project_name'],
                'generation_potential': {
                    'score': round(potential_score, 1),
                    'level': potential_level,
                    'description': self._get_potential_description(potential_level)
                },
                'structure_readiness': structure_readiness,
                'content_readiness': content_readiness,
                'expansion_opportunities': expansion_opportunities,
                'ai_recommendations': self._generate_ai_recommendations(potential_score, structure_readiness, content_readiness, expansion_opportunities),
                'analysis_timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error assessing generation potential: {e}")
            raise

    def generate_user_project_insights(self, user_id: Union[str, UUID], time_period_days: int = 30) -> dict[str, Any]:
        """
        Generate comprehensive insights about a user's project portfolio.

        Args:
            user_id: User UUID
            time_period_days: Analysis time period in days

        Returns:
            Dictionary with user insights
        """
        try:
            if isinstance(user_id, str):
                user_id = UUID(user_id)

            user = User.objects.get(id=user_id)
            since_date = datetime.now() - timedelta(days=time_period_days)

            # Get user's projects
            projects = Project.objects.filter(
                owner=user,
                deleted_at__isnull=True
            ).select_related('owner').prefetch_related(
                'story_canvases__nodes',
                'locations'
            )

            total_projects = projects.count()
            recent_projects = projects.filter(updated_at__gte=since_date).count()

            if total_projects == 0:
                return {
                    'user_id': str(user_id),
                    'username': user.username,
                    'total_projects': 0,
                    'analyzed_projects': 0,
                    'message': 'No projects found for analysis',
                    'analysis_timestamp': datetime.now().isoformat()
                }

            # Analyze each project
            analyzed_projects = []
            for project in projects[:20]:  # Limit to 20 projects for performance
                try:
                    complexity = self.analyze_project_complexity(project.id)
                    health = self.assess_project_health(project.id)
                    analyzed_projects.append({
                        'project_id': str(project.id),
                        'name': project.name,
                        'complexity_score': complexity['overall_complexity']['score'],
                        'health_score': health['overall_health']['score']
                    })
                except Exception as e:
                    logger.warning(f"Failed to analyze project {project.id}: {e}")
                    continue

            # Generate portfolio insights
            portfolio_overview = self._generate_portfolio_overview(analyzed_projects, projects)
            ai_opportunities = self._identify_portfolio_ai_opportunities(analyzed_projects)
            recommendations = self._generate_user_recommendations(analyzed_projects, portfolio_overview)

            return {
                'user_id': str(user_id),
                'username': user.username,
                'total_projects': total_projects,
                'analyzed_projects': len(analyzed_projects),
                'recent_activity_projects': recent_projects,
                'time_period_days': time_period_days,
                'portfolio_overview': portfolio_overview,
                'ai_opportunities': ai_opportunities,
                'personalized_recommendations': recommendations,
                'analysis_timestamp': datetime.now().isoformat()
            }

        except User.DoesNotExist:
            logger.error(f"User not found: {user_id}")
            raise ValueError(f"User {user_id} not found")
        except Exception as e:
            logger.error(f"Error generating user insights: {e}")
            raise

    def _calculate_project_stats(self, project: Project) -> dict[str, Any]:
        """Calculate comprehensive project statistics."""
        canvases = project.story_canvases.all()
        canvas_count = canvases.count()

        # Node and connection counts
        total_nodes = sum(canvas.nodes.count() for canvas in canvases)
        total_connections = sum(
            canvas.nodes.aggregate(
                total=Count('outgoing_connections')
            )['total'] or 0 for canvas in canvases
        )

        # Content metrics
        character_count = 1 if hasattr(project, 'player_character') and project.player_character else 0
        location_count = project.locations.count()

        # Calculate content length
        total_content_length = 0
        for canvas in canvases:
            for node in canvas.nodes.all():
                # StoryNode stores content in node_data['content']
                if hasattr(node, 'node_data') and node.node_data and 'content' in node.node_data:
                    content = node.node_data['content']
                    if content:
                        total_content_length += len(str(content))

        # Component diversity
        component_types = []
        if canvas_count > 0:
            component_types.append('canvases')
        if total_nodes > 0:
            component_types.append('nodes')
        if character_count > 0:
            component_types.append('characters')
        if location_count > 0:
            component_types.append('locations')

        return {
            'canvas_count': canvas_count,
            'node_count': total_nodes,
            'connection_count': total_connections,
            'character_count': character_count,
            'location_count': location_count,
            'total_content_length': total_content_length,
            'component_diversity': len(component_types),
            'component_types': component_types,
            'avg_connections_per_node': total_connections / total_nodes if total_nodes > 0 else 0
        }

    def _assess_structural_complexity(self, stats: dict[str, Any]) -> dict[str, Any]:
        """Assess structural complexity based on project organization."""
        canvas_count = stats['canvas_count']
        node_count = stats['node_count']
        connection_count = stats['connection_count']
        component_diversity = stats['component_diversity']

        # Calculate component scores (max 100 each)
        canvas_score = min(canvas_count * 15, 30)
        node_score = min(node_count * 2, 25)
        connection_score = min(connection_count * 1.5, 20)
        diversity_score = component_diversity * 8.33  # Max 4 types * 8.33 = ~33

        total_score = canvas_score + node_score + connection_score + diversity_score
        level = self._get_complexity_level(total_score)

        return {
            'score': round(total_score, 1),
            'level': level,
            'components': {
                'canvas_complexity': round(canvas_score, 1),
                'node_complexity': round(node_score, 1),
                'connection_complexity': round(connection_score, 1),
                'diversity_score': round(diversity_score, 1)
            }
        }

    def _assess_content_complexity(self, stats: dict[str, Any]) -> dict[str, Any]:
        """Assess content complexity based on writing and detail."""
        content_length = stats['total_content_length']
        character_count = stats['character_count']
        location_count = stats['location_count']
        node_count = stats['node_count']

        # Content density score
        avg_content_per_node = content_length / node_count if node_count > 0 else 0
        content_density_score = min(avg_content_per_node / 50, 30)  # 50 chars = 1 point, max 30

        # Character development score
        character_score = min(character_count * 3, 25)

        # World building score
        location_score = min(location_count * 4, 20)

        # Narrative depth (estimated)
        narrative_score = min(content_length / 1000, 25)  # 1000 chars = 1 point, max 25

        total_score = content_density_score + character_score + location_score + narrative_score
        level = self._get_complexity_level(total_score)

        return {
            'score': round(total_score, 1),
            'level': level,
            'components': {
                'content_density': round(content_density_score, 1),
                'character_development': round(character_score, 1),
                'world_building': round(location_score, 1),
                'narrative_depth': round(narrative_score, 1)
            }
        }

    def _assess_relationship_complexity(self, stats: dict[str, Any]) -> dict[str, Any]:
        """Assess relationship and interaction complexity."""
        node_count = stats['node_count']
        connection_count = stats['connection_count']
        character_count = stats['character_count']

        # Connection density
        avg_connections = stats['avg_connections_per_node']
        connection_density_score = min(avg_connections * 15, 40)

        # Character interaction potential
        interaction_potential = character_count * (character_count - 1) / 2 if character_count > 1 else 0
        interaction_score = min(interaction_potential * 2, 30)

        # Story flow complexity
        flow_score = min((connection_count / node_count * 20) if node_count > 0 else 0, 30)

        total_score = connection_density_score + interaction_score + flow_score
        level = self._get_complexity_level(total_score)

        return {
            'score': round(total_score, 1),
            'level': level,
            'components': {
                'connection_density': round(connection_density_score, 1),
                'interaction_potential': round(interaction_score, 1),
                'story_flow': round(flow_score, 1)
            }
        }

    def _assess_completeness(self, project: Project) -> dict[str, Any]:
        """Assess project completeness."""
        canvases = project.story_canvases.all()
        canvas_count = canvases.count()

        # Basic structure completeness
        structure_score = 20 if canvas_count > 0 else 0
        structure_score += min(canvas_count * 10, 30)

        # Content completeness
        content_score = 0
        total_nodes = 0
        content_nodes = 0

        for canvas in canvases:
            nodes = canvas.nodes.all()
            total_nodes += nodes.count()
            for node in nodes:
                # Check content in node_data
                if (hasattr(node, 'node_data') and node.node_data and
                    'content' in node.node_data and node.node_data['content'] and
                    len(str(node.node_data['content']).strip()) > 20):
                    content_nodes += 1

        content_ratio = content_nodes / total_nodes if total_nodes > 0 else 0
        content_score = content_ratio * 30

        # Character and world completeness
        character_count = 1 if hasattr(project, 'player_character') and project.player_character else 0
        character_score = min(character_count * 10, 20)

        total_score = structure_score + content_score + character_score

        return {
            'score': round(total_score, 1),
            'components': {
                'structure_completeness': round(structure_score, 1),
                'content_completeness': round(content_score, 1),
                'character_completeness': round(character_score, 1)
            }
        }

    def _assess_consistency(self, project: Project) -> dict[str, Any]:
        """Assess project consistency."""
        # For now, basic consistency check
        # In a real implementation, this would check for:
        # - Naming consistency
        # - Style consistency
        # - Structural consistency

        base_score = 70  # Assume basic consistency

        return {
            'score': base_score,
            'components': {
                'naming_consistency': 70,
                'style_consistency': 70,
                'structural_consistency': 70
            }
        }

    def _assess_quality(self, project: Project) -> dict[str, Any]:
        """Assess project quality."""
        # Basic quality assessment
        # In a real implementation, this would analyze:
        # - Content quality
        # - Structure quality
        # - User experience quality

        base_score = 60  # Assume decent quality

        return {
            'score': base_score,
            'components': {
                'content_quality': 60,
                'structure_quality': 60,
                'ux_quality': 60
            }
        }

    def _assess_structure_readiness(self, complexity: dict[str, Any]) -> dict[str, Any]:
        """Assess how ready the project structure is for AI enhancement."""
        structural_score = complexity['structural_complexity']['score']

        # Higher structural complexity = better readiness
        readiness_score = min(structural_score * 1.2, 100)

        return {
            'score': round(readiness_score, 1),
            'level': self._get_readiness_level(readiness_score),
            'factors': ['Node connectivity', 'Canvas organization', 'Component diversity']
        }

    def _assess_content_readiness(self, complexity: dict[str, Any], health: dict[str, Any]) -> dict[str, Any]:
        """Assess how ready the content is for AI enhancement."""
        content_score = complexity['content_complexity']['score']
        quality_score = health['quality']['score']

        readiness_score = (content_score * 0.6 + quality_score * 0.4)

        return {
            'score': round(readiness_score, 1),
            'level': self._get_readiness_level(readiness_score),
            'factors': ['Content depth', 'Character development', 'Quality metrics']
        }

    def _identify_expansion_opportunities(self, complexity: dict[str, Any]) -> dict[str, Any]:
        """Identify opportunities for AI-driven expansion."""
        stats = complexity['project_stats']

        opportunities = []
        opportunity_score = 0

        # Check for expansion opportunities
        if stats['character_count'] < 3:
            opportunities.append('Character development')
            opportunity_score += 20

        if stats['location_count'] < 2:
            opportunities.append('World building')
            opportunity_score += 20

        if stats['node_count'] < 10:
            opportunities.append('Story expansion')
            opportunity_score += 25

        if stats['total_content_length'] < 1000:
            opportunities.append('Content enrichment')
            opportunity_score += 25

        if stats['avg_connections_per_node'] < 1.5:
            opportunities.append('Choice complexity')
            opportunity_score += 10

        return {
            'score': min(opportunity_score, 100),
            'opportunities': opportunities,
            'priority_areas': opportunities[:3]  # Top 3 priorities
        }

    def _generate_portfolio_overview(self, analyzed_projects: list[dict], all_projects) -> dict[str, Any]:
        """Generate portfolio overview statistics."""
        if not analyzed_projects:
            return {}

        # Calculate averages
        avg_complexity = sum(p['complexity_score'] for p in analyzed_projects) / len(analyzed_projects)
        avg_health = sum(p['health_score'] for p in analyzed_projects) / len(analyzed_projects)

        # Get genre distribution (simplified)
        genre_dist = {}
        for project in all_projects:
            genre = getattr(project, 'genre', 'Unknown') or 'Unknown'
            genre_dist[genre] = genre_dist.get(genre, 0) + 1

        return {
            'average_complexity': round(avg_complexity, 1),
            'average_health': round(avg_health, 1),
            'genre_distribution': genre_dist,
            'portfolio_maturity': self._assess_portfolio_maturity(avg_complexity, avg_health)
        }

    def _identify_portfolio_ai_opportunities(self, analyzed_projects: list[dict]) -> dict[str, Any]:
        """Identify AI opportunities across the portfolio."""
        high_potential = [p for p in analyzed_projects if p['complexity_score'] > 60 and p['health_score'] > 50]
        improvement_candidates = [p for p in analyzed_projects if p['health_score'] < 40]

        return {
            'high_potential_projects': high_potential[:5],
            'improvement_candidates': improvement_candidates[:3],
            'expansion_ready': len([p for p in analyzed_projects if p['complexity_score'] < 40])
        }

    def _generate_user_recommendations(self, analyzed_projects: list[dict], portfolio_overview: dict) -> list[str]:
        """Generate personalized recommendations for the user."""
        recommendations = []

        avg_complexity = portfolio_overview.get('average_complexity', 0)
        avg_health = portfolio_overview.get('average_health', 0)

        if avg_complexity < 30:
            recommendations.append("Focus on creating more complex story structures with multiple paths")

        if avg_health < 50:
            recommendations.append("Improve content quality and completeness across projects")

        if len(analyzed_projects) < 3:
            recommendations.append("Develop a more diverse portfolio with different story types")

        return recommendations

    def _generate_health_recommendations(self, overall_score: float, completeness: dict, consistency: dict, quality: dict) -> list[str]:
        """Generate health improvement recommendations."""
        recommendations = []

        if completeness['score'] < 50:
            recommendations.append("Focus on completing story content and character development")

        if consistency['score'] < 60:
            recommendations.append("Improve consistency in naming, style, and structure")

        if quality['score'] < 50:
            recommendations.append("Enhance content quality and user experience")

        return recommendations

    def _generate_ai_recommendations(self, potential_score: float, structure: dict, content: dict, expansion: dict) -> list[str]:
        """Generate AI enhancement recommendations."""
        recommendations = []

        if structure['score'] > 70:
            recommendations.append("Structure is AI-ready - consider content generation")

        if content['score'] < 50:
            recommendations.append("Improve content depth before AI enhancement")

        if expansion['opportunities']:
            recommendations.append(f"Focus AI enhancement on: {', '.join(expansion['opportunities'][:2])}")

        return recommendations

    def _get_complexity_level(self, score: float) -> str:
        """Convert complexity score to level."""
        if score >= 80:
            return "Very High"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Moderate"
        elif score >= 20:
            return "Low"
        else:
            return "Very Low"

    def _get_health_level(self, score: float) -> str:
        """Convert health score to level."""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        elif score >= 20:
            return "Poor"
        else:
            return "Critical"

    def _get_potential_level(self, score: float) -> str:
        """Convert potential score to level."""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Moderate"
        elif score >= 20:
            return "Low"
        else:
            return "Limited"

    def _get_readiness_level(self, score: float) -> str:
        """Convert readiness score to level."""
        if score >= 80:
            return "Ready"
        elif score >= 60:
            return "Nearly Ready"
        elif score >= 40:
            return "Needs Work"
        else:
            return "Not Ready"

    def _get_complexity_description(self, level: str) -> str:
        """Get description for complexity level."""
        descriptions = {
            "Very High": "Highly sophisticated project with complex structures and rich content",
            "High": "Well-developed project with good complexity and depth",
            "Moderate": "Reasonably complex project with room for enhancement",
            "Low": "Simple project structure with basic elements",
            "Very Low": "Minimal project complexity requiring significant development"
        }
        return descriptions.get(level, "Unknown complexity level")

    def _get_health_description(self, level: str) -> str:
        """Get description for health level."""
        descriptions = {
            "Excellent": "Project is complete, consistent, and high quality",
            "Good": "Project is well-developed with minor areas for improvement",
            "Fair": "Project has good foundation but needs content and quality improvements",
            "Poor": "Project requires significant work on completeness and quality",
            "Critical": "Project needs major improvements across all areas"
        }
        return descriptions.get(level, "Unknown health level")

    def _get_potential_description(self, level: str) -> str:
        """Get description for AI potential level."""
        descriptions = {
            "Excellent": "Perfect candidate for AI enhancement with high success potential",
            "High": "Good structure for AI enhancement with promising opportunities",
            "Moderate": "Suitable for AI enhancement with some preparation needed",
            "Low": "Limited AI potential, requires foundational improvements first",
            "Limited": "Not ready for AI enhancement, needs significant development"
        }
        return descriptions.get(level, "Unknown potential level")

    def _assess_portfolio_maturity(self, avg_complexity: float, avg_health: float) -> str:
        """Assess overall portfolio maturity."""
        combined_score = (avg_complexity + avg_health) / 2

        if combined_score >= 70:
            return "Mature"
        elif combined_score >= 50:
            return "Developing"
        elif combined_score >= 30:
            return "Early Stage"
        else:
            return "Beginner"
