"""
Integration module for ReAct workflow.

Provides a clean interface for using the ReAct pattern workflow.
This eliminates confusion by using only the ReAct implementation.
"""

import logging
from enum import Enum
from typing import Any, Optional

from .agent.react_state import ReActState
from .agent.react_workflow import ReActWorkflow
from .services.workflow_logger import ReActWorkflowLogger

logger = logging.getLogger(__name__)


class WorkflowMode(Enum):
    """Available workflow modes."""
    REACT = "react"      # ReAct pattern workflow (default and only mode)


class EloraAgentIntegration:
    """
    Integration layer for Elora Agent workflow.

    Provides a clean interface for using the ReAct pattern workflow,
    eliminating confusion by using only one workflow implementation.
    """

    def __init__(self, project_id: str, model_name: str = None):
        self.project_id = project_id
        self.model_name = model_name
        self.workflow_mode = WorkflowMode.REACT

        # Session continuity - maintain workflow instances to prevent re-initialization
        self._react_workflow: Optional[ReActWorkflow] = None
        self._session_logger: Optional[ReActWorkflowLogger] = None
        self._current_session_id: Optional[str] = None

        logger.info("Elora Agent initialized with ReAct workflow")

    def process_user_input(self, user_input: str, session_id: str,
                          previous_state: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Process user input using the appropriate workflow.

        Args:
            user_input: User's input message
            session_id: Session identifier
            previous_state: Previous conversation state (if continuing)

        Returns:
            Updated conversation state and response
        """
        logger.info("Processing user input with ReAct workflow")

        try:
            return self._process_with_react_workflow(user_input, session_id, previous_state)

        except Exception as e:
            logger.error(f"Workflow processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f"I encountered an error: {str(e)}",
                "state": None,
                "awaiting_user_response": False
            }


    def _process_with_react_workflow(self, user_input: str, session_id: str,
                                   previous_state: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Process with ReAct pattern workflow."""
        # Initialize or reuse workflow components for session continuity
        if (not self._react_workflow or
            not self._session_logger or
            self._current_session_id != session_id):

            # Clean up existing logger if switching sessions
            if self._session_logger and self._current_session_id != session_id:
                self._session_logger.cleanup_logger()

            # Create new components for this session
            self._session_logger = ReActWorkflowLogger(session_id, self.project_id)
            self._react_workflow = ReActWorkflow(self.project_id, self.model_name, self._session_logger)
            self._current_session_id = session_id
            logger.info("Initialized ReAct workflow components for session continuity")

        # Create or restore ReAct state
        if previous_state and previous_state.get("workflow_type") == "react":
            state = ReActState.from_dict(previous_state["state"])
        else:
            state = ReActState(
                project_id=self.project_id,
                session_id=session_id,
                max_steps=10
            )

        # Run ReAct workflow with reused components
        result_state = self._react_workflow.run_react_loop(state, user_input)

        # Extract response
        response = ""
        if result_state.messages:
            # Get the last assistant message
            for message in reversed(result_state.messages):
                if message.get("role") == "assistant":
                    response = message["content"]
                    break

        return {
            "success": not bool(result_state.error_message),
            "error": result_state.error_message,
            "response": response,
            "state": {
                "workflow_type": "react",
                "state": result_state.to_dict()
            },
            "awaiting_user_response": result_state.awaiting_user_response,
            "workflow_type": "react",
            "conversation_summary": result_state.get_conversation_summary(),
            "step_count": result_state.step_count,
            "goal_achieved": result_state.user_goal_achieved,
            "tool_results": result_state.tool_results,
            "current_phase": result_state.current_phase.value if result_state.current_phase else None,
            "pending_questions": result_state.pending_questions,
            "safety_info": {
                "verdict": result_state.safety_decision.verdict.value if result_state.safety_decision else None,
                "reasoning": result_state.safety_decision.reasoning if result_state.safety_decision else None
            } if result_state.safety_decision else None
        }


    def get_workflow_info(self) -> dict[str, Any]:
        """Get information about current workflow configuration."""
        return {
            "mode": self.workflow_mode.value,
            "project_id": self.project_id,
            "model_name": self.model_name,
            "available_modes": [WorkflowMode.REACT.value],
            "react_capabilities": {
                "single_step_planning": True,
                "safety_gates": True,
                "conversational_flow": True,
                "ask_clarification": True,
                "confirmation_flow": True,
                "dry_run_preview": True,
                "proper_tool_routing": True
            }
        }


    def get_conversation_state(self, state_dict: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Extract conversation state for frontend display."""
        if not state_dict:
            return None

        # ReAct workflow state (only workflow supported)
        if state_dict.get("workflow_type") == "react":
            react_state_data = state_dict.get("state", {})
            return {
                "step_count": react_state_data.get("step_count", 0),
                "max_steps": react_state_data.get("max_steps", 10),
                "current_phase": react_state_data.get("current_phase", "ground_context"),
                "awaiting_user_response": react_state_data.get("awaiting_user_response", False),
                "pending_questions": react_state_data.get("pending_questions", []),
                "goal_achieved": react_state_data.get("user_goal_achieved", False),
                "user_goal": react_state_data.get("user_goal", ""),
                "conversation_summary": f"Step {react_state_data.get('step_count', 0)}/{react_state_data.get('max_steps', 10)} | Phase: {react_state_data.get('current_phase', 'unknown')}"
            }

        # Legacy state handling
        return {
            "workflow_type": "react",
            "completed": True,
            "tool_count": len(state_dict.get("tool_results", []))
        }

    def cleanup_session(self):
        """Clean up workflow components and resources."""
        if self._session_logger:
            self._session_logger.cleanup_logger()
            self._session_logger = None

        self._react_workflow = None
        self._current_session_id = None
        logger.info("Cleaned up ReAct workflow session")


# Convenience factory functions
def create_elora_agent(project_id: str, model_name: str = None) -> EloraAgentIntegration:
    """Create an Elora agent using ReAct workflow."""
    return EloraAgentIntegration(project_id, model_name)


def create_react_agent(project_id: str, model_name: str = None) -> EloraAgentIntegration:
    """Create an Elora agent using ReAct workflow (same as create_elora_agent)."""
    return EloraAgentIntegration(project_id, model_name)
