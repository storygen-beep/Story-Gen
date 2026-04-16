"""
Agent tool definitions for LangGraph integration.

These are the tools the agent can call during conversations.
They wrap the services and provide a clean interface for LangGraph.

Phase 1 Enhancement: Integrates Phase 1 ReAct tool adapters for trigger-aware
canonical tool implementations while maintaining backward compatibility.
"""

import logging
from typing import Any

from ..services.memory_service import MemoryService
from ..services.phase1_tool_adapters import get_phase1_tool_adapters
from ..services.tool_manifest_registry import get_tool_manifest_registry
from ..tools import StoryTools, WorldTools

logger = logging.getLogger(__name__)


class AgentToolKit:
    """
    Collection of tools available to the Elora agent.

    This wraps the services and provides a unified interface for tool calls.

    Phase 1 Enhancement: Integrates Phase 1 ReAct tool adapters for canonical
    tool implementations while maintaining backward compatibility.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.memory_service = MemoryService(project_id)
        self.story_tools = StoryTools(project_id)
        self.world_tools = WorldTools(project_id)

        # Phase 1 Enhancement: Initialize canonical tool adapters
        self.phase1_adapters = get_phase1_tool_adapters(project_id)
        self.tool_registry = get_tool_manifest_registry()
        logger.info(f"AgentToolKit initialized with Phase 1 adapters for project: {project_id}")

    # ========== MEMORY TOOLS ==========

    def memory_put(self, kind: str, topic: str, text: str,
                  tags: list[str] = None, refs: dict[str, Any] = None) -> dict[str, Any]:
        """
        Store a memory.

        Args:
            kind: Memory type (episodic, semantic, feedback, artifacts)
            topic: Memory topic
            text: Memory content
            tags: Optional tags
            refs: Optional references to IDs

        Returns:
            Stored memory info
        """
        try:
            result = self.memory_service.store_memory(
                kind=kind,
                topic=topic,
                text=text,
                tags=tags or [],
                refs=refs or {},
            )
            logger.info(f"Agent stored {kind} memory: {topic}")
            return {"success": True, "memory": result}

        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return {"success": False, "error": str(e)}

    def memory_search(self, query: str = None, kind: str = None,
                     topic: str = None, limit: int = 5) -> dict[str, Any]:
        """
        Search memories.

        Args:
            query: Text query
            kind: Memory kind filter
            topic: Topic filter
            limit: Max results

        Returns:
            Search results
        """
        try:
            memories = self.memory_service.search_memories(
                query=query,
                kind=kind,
                topic=topic,
                limit=limit
            )
            logger.info(f"Agent searched memories: {len(memories)} results")
            return {"success": True, "memories": memories, "count": len(memories)}

        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return {"success": False, "error": str(e)}

    # ========== FEEDBACK TOOLS ==========

    def feedback_store(self, feedback_text: str, topic: str = "general",
                      refs: dict[str, Any] = None) -> dict[str, Any]:
        """
        Store user feedback.

        Args:
            feedback_text: The feedback content
            topic: Feedback topic/category
            refs: References to canvas/nodes

        Returns:
            Stored feedback info
        """
        return self.memory_put(
            kind="feedback",
            topic=topic,
            text=feedback_text,
            tags=["user_feedback"],
            refs=refs
        )

    def feedback_retrieve(self, topic: str = None, limit: int = 5) -> dict[str, Any]:
        """
        Retrieve recent feedback.

        Args:
            topic: Optional topic filter
            limit: Max results

        Returns:
            Retrieved feedback
        """
        return self.memory_search(
            kind="feedback",
            topic=topic,
            limit=limit
        )

    # ========== CAPABILITY TOOLS ==========

    def capability_list(self) -> dict[str, Any]:
        """
        List available capabilities.

        Returns:
            Available capabilities
        """
        capabilities = {
            "memory": ["put", "search"],
            "feedback": ["store", "retrieve"],
            "story": ["read_canvas", "patch_canvas", "create_canvas"],
            "world": ["read_locations", "read_location_detail"],
            "writer": ["outline", "expand", "edit_lint"],  # TODO: Implement
            "preview": ["generate_twee"],  # TODO: Implement
        }

        return {"success": True, "capabilities": capabilities}

    def capability_check(self, operation: str) -> dict[str, Any]:
        """
        Check if an operation is available.

        Args:
            operation: Operation to check (e.g. "story.read_canvas")

        Returns:
            Capability check result
        """
        # Simple capability checking - could be more sophisticated
        parts = operation.split('.')
        if len(parts) != 2:
            return {"success": False, "available": False, "reason": "Invalid operation format"}

        category, action = parts
        capabilities = self.capability_list()["capabilities"]

        if category not in capabilities:
            return {"success": False, "available": False, "reason": f"Category '{category}' not found"}

        if action not in capabilities[category]:
            return {"success": False, "available": False, "reason": f"Action '{action}' not available in '{category}'"}

        return {"success": True, "available": True}

    # ========== PHASE 1 CANONICAL TOOLS ==========

    def describe_canvas(self, canvas_id: str = None) -> dict[str, Any]:
        """
        Phase 1 canonical describe_canvas tool.

        Summarize project canvases or a specific canvas, including trigger metadata
        with enhanced weekday/time_range information from TriggerSchedule.

        Args:
            canvas_id: Optional specific canvas ID, otherwise return project summary

        Returns:
            Canvas data with enhanced trigger metadata
        """
        return self.phase1_adapters.describe_canvas(canvas_id)

    def search_nodes(self, canvas_id: str, query: str) -> dict[str, Any]:
        """
        Phase 1 canonical search_nodes tool.

        Search nodes within a specific canvas by keyword using canvas-scoped
        hybrid search as specified in Phase 1.

        Args:
            canvas_id: Target canvas ID to search within
            query: Search query text

        Returns:
            Search results filtered to specified canvas nodes
        """
        return self.phase1_adapters.search_nodes(canvas_id, query)

    def create_node(self, canvas_id: str, title: str, content: str, overwrite_confirmed: bool = False) -> dict[str, Any]:
        """
        Phase 1 canonical create_node tool.

        Create a new story node in a canvas with Phase-1 one-node-per-canvas
        rule enforcement and ASK → DRY-RUN → CONFIRM overwrite flow.

        Args:
            canvas_id: Target canvas ID
            title: Node title
            content: Node content
            overwrite_confirmed: Whether user confirmed overwrite (internal parameter)

        Returns:
            Created node info or error if one-node rule violated
        """
        return self.phase1_adapters.create_node(canvas_id, title, content, overwrite_confirmed)

    def delete_canvas(self, canvas_id: str, dry_run: bool = False) -> dict[str, Any]:
        """
        Phase 1 canonical delete_canvas tool.

        Delete a canvas and contained nodes/links (also removes its 1:1 trigger)
        with structured dry-run previews for high-destructiveness operations.

        Args:
            canvas_id: Canvas to delete
            dry_run: If True, return impact preview without executing

        Returns:
            Deletion result or structured impact preview
        """
        return self.phase1_adapters.delete_canvas(canvas_id, dry_run)

    # ========== STORY TOOLS (Legacy - Backward Compatibility) ==========

    def story_read_canvas(self, canvas_id: str = None) -> dict[str, Any]:
        """
        Legacy story canvas reading (backward compatibility).

        DEPRECATED: Use describe_canvas() for Phase 1 compliance with enhanced
        trigger metadata. This method maintains compatibility for existing code.

        Args:
            canvas_id: Optional specific canvas ID, otherwise summary

        Returns:
            Canvas data (legacy format without enhanced trigger metadata)
        """
        logger.warning("story_read_canvas is deprecated - use describe_canvas for Phase 1 compliance")

        try:
            if canvas_id:
                result = self.story_tools.read_canvas_detail(canvas_id)
                logger.info(f"Agent read canvas detail (legacy): {canvas_id}")
                return {"success": True, "type": "detail", "canvas": result}
            else:
                result = self.story_tools.read_canvas_summary()
                logger.info(f"Agent read canvas summary (legacy): {result['canvas_count']} canvases")
                return {"success": True, "type": "summary", "data": result}

        except Exception as e:
            logger.error(f"Error reading canvas (legacy): {e}")
            return {"success": False, "error": str(e)}

    def story_patch_canvas(self, canvas_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        """
        Update/patch a story canvas.

        Args:
            canvas_id: Canvas to update
            updates: Fields to update

        Returns:
            Update result
        """
        try:
            result = self.story_tools.update_canvas_content(canvas_id, updates)
            logger.info(f"Agent patched canvas: {canvas_id}")
            return {"success": True, "updated": result}

        except Exception as e:
            logger.error(f"Error patching canvas: {e}")
            return {"success": False, "error": str(e)}

    def story_create_canvas(self, name: str, description: str = "",
                           location_id: str = None) -> dict[str, Any]:
        """
        Create a new story canvas.

        Args:
            name: Canvas name
            description: Canvas description
            location_id: Optional trigger location

        Returns:
            Created canvas info
        """
        try:
            result = self.story_tools.create_canvas(
                name=name,
                description=description,
                location_id=location_id
            )
            logger.info(f"Agent created canvas: {name}")
            return {"success": True, "created": result}

        except Exception as e:
            logger.error(f"Error creating canvas: {e}")
            return {"success": False, "error": str(e)}

    def story_find_canvas(self, query: str) -> dict[str, Any]:
        """
        Find canvas using entity-aware search with disambiguation support.

        This method uses the entity search system to find canvases by name,
        enabling fuzzy matching and conversational disambiguation.

        Args:
            query: Canvas name or description to search for

        Returns:
            Canvas search result with disambiguation if needed
        """
        try:
            result = self.story_tools.find_canvas(query)

            # Log based on result type
            if result.get("type") == "disambiguation":
                logger.info(f"Agent found multiple canvases for '{query}': {len(result['choices'])} matches")
            elif "nodes" in result:
                logger.info(f"Agent found canvas '{result['name']}' via entity search")
            else:
                logger.info(f"Agent canvas search for '{query}': {result.get('type', 'unknown')}")

            return {"success": True, **result}

        except Exception as e:
            logger.error(f"Error in entity canvas search: {e}")
            return {"success": False, "error": str(e)}

    # ========== WORLD TOOLS ==========

    def world_read_locations(self) -> dict[str, Any]:
        """
        Read world locations summary.

        Returns:
            Locations data
        """
        try:
            result = self.world_tools.read_locations_summary()
            logger.info(f"Agent read locations: {result['location_count']} locations")
            return {"success": True, "data": result}

        except Exception as e:
            logger.error(f"Error reading locations: {e}")
            return {"success": False, "error": str(e)}

    def world_read_location_detail(self, location_id: str) -> dict[str, Any]:
        """
        Read specific location details.

        Args:
            location_id: Location UUID

        Returns:
            Location detail data
        """
        try:
            result = self.world_tools.read_location_detail(location_id)
            logger.info(f"Agent read location detail: {location_id}")
            return {"success": True, "location": result}

        except Exception as e:
            logger.error(f"Error reading location detail: {e}")
            return {"success": False, "error": str(e)}

    # ========== WRITER TOOLS (MOCKED) ==========

    def writer_outline(self, topic: str, context: str = "") -> dict[str, Any]:
        """
        Create a story outline using AI.

        Args:
            topic: Topic to outline
            context: Additional context

        Returns:
            Generated outline
        """
        try:
            from ..services.ai_service import AIService
            ai_service = AIService()

            outline = ai_service.generate_outline(topic, context)

            logger.info(f"Agent created AI outline for: {topic}")
            return {"success": True, "outline": outline}

        except Exception as e:
            logger.error(f"AI outline generation failed: {e}")
            return {"success": False, "error": f"Failed to generate outline: {str(e)}"}

    def writer_expand(self, outline: str, section: str = "") -> dict[str, Any]:
        """
        Expand an outline into detailed content using AI.

        Args:
            outline: The outline to expand
            section: Specific section to expand

        Returns:
            Expanded content
        """
        try:
            from ..services.ai_service import AIService
            ai_service = AIService()

            expanded_content = ai_service.expand_content(outline, section)

            logger.info(f"Agent expanded AI content for: {section or 'full story'}")
            return {"success": True, "expanded": expanded_content}

        except Exception as e:
            logger.error(f"AI content expansion failed: {e}")
            return {"success": False, "error": f"Failed to expand content: {str(e)}"}

    def writer_edit_lint(self, content: str) -> dict[str, Any]:
        """
        Edit and lint story content (MOCK implementation).

        Args:
            content: Content to edit

        Returns:
            Edited content with suggestions
        """
        # TODO: Implement with actual editing logic
        suggestions = [
            "Consider adding more sensory details",
            "Check for consistent character voice",
            "Ensure clear narrative flow",
        ]

        # Mock edit - just return original for now
        edited_content = content

        logger.info("Agent performed editing/linting")
        return {
            "success": True,
            "edited": edited_content,
            "suggestions": suggestions
        }

    # ========== SEARCH TOOLS ==========

    def hybrid_search(self, query: str, entity_types: list[str] = None,
                     limit: int = 10, filters: dict[str, Any] = None) -> dict[str, Any]:
        """
        Perform hybrid search across all project entities.

        Args:
            query: Search query text
            entity_types: Filter by entity types (canvas, location, character, etc.)
            limit: Maximum number of results
            filters: Additional filters

        Returns:
            Hybrid search results with ranking and score breakdown
        """
        try:
            from ..services.hybrid_search_service import get_hybrid_search_service

            search_service = get_hybrid_search_service(self.project_id)
            results = search_service.hybrid_search(
                query=query,
                entity_types=entity_types,
                limit=limit,
                filters=filters or {}
            )

            # Format results for agent consumption
            formatted_results = []
            for result in results:
                entity = result["entity"]
                score_info = result["score_breakdown"]

                formatted_results.append({
                    "entity_id": entity["entity_id"],
                    "name": entity.get("name", "Unnamed"),
                    "entity_type": entity["entity_type"],
                    "summary": entity.get("summary", "No summary")[:200],
                    "score": result["score"],
                    "score_breakdown": {
                        "bm25": score_info.get("bm25_score", 0.0),
                        "vector": score_info.get("vector_score", 0.0),
                        "recency": score_info.get("recency_score", 0.0),
                        "final": score_info.get("final_score", 0.0)
                    }
                })

            logger.info(f"Agent hybrid search: '{query}' found {len(results)} results")

            return {
                "success": True,
                "query": query,
                "results": formatted_results,
                "total_count": len(results),
                "search_explanation": search_service.explain_search_results(results) if results else "No results found"
            }

        except Exception as e:
            logger.error(f"Hybrid search error: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
