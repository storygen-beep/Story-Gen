"""
ReAct State definitions for true ReAct pattern implementation.

Complete ReAct state management including:
- Single-step planning tracking
- Safety policy decisions
- Reflection and learning
- Confirmation flows
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class AgentMode(Enum):
    """Agent operational modes."""
    THINK = "think"
    DO = "do"


class SafetyVerdict(Enum):
    """Safety policy verdicts for operations."""
    PROCEED = "proceed"      # Safe to execute directly
    ASK = "ask"             # Need clarification from user
    DRY_RUN = "dry_run"     # Show preview before execution
    CONFIRM = "confirm"     # Require explicit confirmation
    DENY = "deny"           # Operation not allowed


class ReActPhase(Enum):
    """Current phase in the ReAct loop."""
    GROUND_CONTEXT = "ground_context"
    PLAN_STEP = "plan_step"
    SAFETY_GATE = "safety_gate"
    EXECUTE_STEP = "execute_step"
    VALIDATE = "validate"  # Phase 1: Validate tool result
    SYNTHESIZE_RESPONSE = "synthesize_response"  # Phase 1: Generate final response
    REFLECT = "reflect"
    ASK_USER = "ask_user"
    AWAIT_CONFIRMATION = "await_confirmation"


@dataclass
class StepPlan:
    """Single step plan with safety metadata."""
    tool: str
    args: dict[str, Any]
    targets: list[str] = field(default_factory=list)
    expected_effect: str = ""
    destructiveness: str = "read_only"  # read_only, low_write, high_write
    confidence: float = 0.0
    needs: list[str] = field(default_factory=list)
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tool": self.tool,
            "args": self.args,
            "targets": self.targets,
            "expected_effect": self.expected_effect,
            "destructiveness": self.destructiveness,
            "confidence": self.confidence,
            "needs": self.needs,
            "rationale": self.rationale
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'StepPlan':
        """Create StepPlan from dictionary."""
        return cls(
            tool=data.get("tool", ""),
            args=data.get("args", {}),
            targets=data.get("targets", []),
            expected_effect=data.get("expected_effect", ""),
            destructiveness=data.get("destructiveness", "read_only"),
            confidence=data.get("confidence", 0.0),
            needs=data.get("needs", []),
            rationale=data.get("rationale", "")
        )


@dataclass
class SafetyDecision:
    """Safety policy decision for a step plan."""
    verdict: SafetyVerdict
    confidence: float
    reasoning: str
    questions: list[str] = field(default_factory=list)
    required_confirmations: list[str] = field(default_factory=list)
    dry_run_preview: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "verdict": self.verdict.value,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "questions": self.questions,
            "required_confirmations": self.required_confirmations,
            "dry_run_preview": self.dry_run_preview
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'SafetyDecision':
        """Create SafetyDecision from dictionary."""
        return cls(
            verdict=SafetyVerdict(data.get("verdict", "proceed")),
            confidence=data.get("confidence", 0.0),
            reasoning=data.get("reasoning", ""),
            questions=data.get("questions", []),
            required_confirmations=data.get("required_confirmations", []),
            dry_run_preview=data.get("dry_run_preview", "")
        )


@dataclass
class ValidationResult:
    """Result of Phase 1 VALIDATE phase."""
    is_valid: bool
    confidence: float
    error_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    should_retry: bool = False
    retry_suggestion: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "is_valid": self.is_valid,
            "confidence": self.confidence,
            "error_reasons": self.error_reasons,
            "warnings": self.warnings,
            "should_retry": self.should_retry,
            "retry_suggestion": self.retry_suggestion
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ValidationResult':
        """Create ValidationResult from dictionary."""
        return cls(
            is_valid=data.get("is_valid", False),
            confidence=data.get("confidence", 0.0),
            error_reasons=data.get("error_reasons", []),
            warnings=data.get("warnings", []),
            should_retry=data.get("should_retry", False),
            retry_suggestion=data.get("retry_suggestion")
        )


@dataclass
class PolicyDecision:
    """Phase 1 Policy Engine decision."""
    action: str  # "tool_call" | "ask_question" | "synthesize_response" | "error"
    confidence: float
    tool_name: Optional[str] = None
    tool_args: Optional[dict[str, Any]] = None
    question: Optional[str] = None
    reasoning: str = ""
    should_cache: bool = False
    cache_key: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "action": self.action,
            "confidence": self.confidence,
            "tool_name": self.tool_name,
            "tool_args": self.tool_args,
            "question": self.question,
            "reasoning": self.reasoning,
            "should_cache": self.should_cache,
            "cache_key": self.cache_key
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'PolicyDecision':
        """Create PolicyDecision from dictionary."""
        return cls(
            action=data.get("action", "error"),
            confidence=data.get("confidence", 0.0),
            tool_name=data.get("tool_name"),
            tool_args=data.get("tool_args"),
            question=data.get("question"),
            reasoning=data.get("reasoning", ""),
            should_cache=data.get("should_cache", False),
            cache_key=data.get("cache_key")
        )


@dataclass
class ReflectionResult:
    """Result of reflection on a completed step."""
    success: bool
    outcome_matches_expectation: bool
    lessons_learned: list[str] = field(default_factory=list)
    next_step_suggestion: Optional[str] = None
    error_analysis: str = ""
    improvement_suggestions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "outcome_matches_expectation": self.outcome_matches_expectation,
            "lessons_learned": self.lessons_learned,
            "next_step_suggestion": self.next_step_suggestion,
            "error_analysis": self.error_analysis,
            "improvement_suggestions": self.improvement_suggestions
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ReflectionResult':
        """Create ReflectionResult from dictionary."""
        return cls(
            success=data.get("success", True),
            outcome_matches_expectation=data.get("outcome_matches_expectation", True),
            lessons_learned=data.get("lessons_learned", []),
            next_step_suggestion=data.get("next_step_suggestion"),
            error_analysis=data.get("error_analysis", ""),
            improvement_suggestions=data.get("improvement_suggestions", [])
        )


@dataclass
class ReActState:
    """
    ReAct workflow state management.

    Manages the complete state for ReAct pattern execution including
    planning, safety decisions, execution results, and learning.
    """

    # Core identification (required fields)
    project_id: str
    session_id: str
    user_goal: str = ""

    # Agent mode and behavior
    mode: AgentMode = AgentMode.THINK

    # Context and memory
    context_snippets: list[dict[str, Any]] = field(default_factory=list)
    feedback_topics: list[str] = field(default_factory=list)
    retrieved_memories: list[dict[str, Any]] = field(default_factory=list)

    # Tool execution tracking
    last_tool: Optional[str] = None
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    failed_attempts: int = 0

    # Messages and conversation
    messages: list[dict[str, str]] = field(default_factory=list)

    # Legacy workflow compatibility
    current_step: str = ""
    next_action: str = ""
    should_continue: bool = True
    error_message: Optional[str] = None

    # ReAct loop control
    current_phase: ReActPhase = ReActPhase.GROUND_CONTEXT
    step_count: int = 0
    max_steps: int = 10

    # Current step planning and execution
    current_plan: Optional[StepPlan] = None
    safety_decision: Optional[SafetyDecision] = None
    step_result: Optional[dict[str, Any]] = None
    reflection: Optional[ReflectionResult] = None

    # Phase 1 specific state
    policy_decision: Optional[PolicyDecision] = None
    validation_result: Optional[ValidationResult] = None
    final_response: Optional[str] = None

    # Conversation flow for ASK/Confirm
    awaiting_user_response: bool = False
    pending_questions: list[str] = field(default_factory=list)
    user_responses: list[str] = field(default_factory=list)

    # Learning and adaptation
    step_history: list[dict[str, Any]] = field(default_factory=list)
    conversation_context: dict[str, Any] = field(default_factory=dict)

    # Progress tracking
    user_goal_achieved: bool = False
    reason_for_completion: str = ""

    def add_step_to_history(self, step_data: dict[str, Any]):
        """Add completed step to history for learning."""
        step_record = {
            "step_count": self.step_count,
            "phase": self.current_phase.value,
            "plan": self.current_plan.to_dict() if self.current_plan else None,
            "safety_decision": self.safety_decision.to_dict() if self.safety_decision else None,
            "result": step_data,
            "reflection": self.reflection.to_dict() if self.reflection else None,
            "timestamp": None  # Could add timestamp if needed
        }
        self.step_history.append(step_record)

    def add_user_response(self, response: str):
        """Add user response to ASK/Confirm flow."""
        self.user_responses.append(response)

        # Clear awaiting state if we got responses to all questions
        if len(self.user_responses) >= len(self.pending_questions):
            self.awaiting_user_response = False

    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        message = {
            "role": role,
            "content": content
        }
        self.messages.append(message)

    def add_tool_result(self, tool: str, result: dict[str, Any], success: bool):
        """Add tool execution result to tracking."""
        tool_result = {
            "tool": tool,
            "result": result,
            "success": success,
            "timestamp": None  # Could add timestamp if needed
        }
        self.tool_results.append(tool_result)
        self.last_tool = tool

    def reset_failures(self):
        """Reset failed attempts counter."""
        self.failed_attempts = 0

    def increment_failures(self):
        """Increment failed attempts counter."""
        self.failed_attempts += 1

    def set_pending_questions(self, questions: list[str]):
        """Set questions awaiting user response."""
        self.pending_questions = questions
        self.user_responses.clear()
        self.awaiting_user_response = len(questions) > 0

    def get_conversation_summary(self) -> str:
        """Generate summary of conversation progress."""
        completed_steps = len([s for s in self.step_history if s.get("result", {}).get("success", False)])

        return (f"Step {self.step_count}/{self.max_steps} | "
                f"Phase: {self.current_phase.value} | "
                f"Completed: {completed_steps} steps | "
                f"Goal: {'✅' if self.user_goal_achieved else '🎯'}")

    def should_continue_react_loop(self) -> bool:
        """Determine if ReAct loop should continue."""
        if self.user_goal_achieved:
            return False

        if self.step_count >= self.max_steps:
            self.reason_for_completion = f"Reached maximum steps ({self.max_steps})"
            return False

        if self.error_message:
            self.reason_for_completion = f"Error encountered: {self.error_message}"
            return False

        if self.awaiting_user_response:
            return False  # Pause until user responds

        return True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            # Core identification
            "project_id": self.project_id,
            "session_id": self.session_id,
            "user_goal": self.user_goal,
            "mode": self.mode.value,

            # Context and memory
            "context_snippets": self.context_snippets,
            "feedback_topics": self.feedback_topics,
            "retrieved_memories": self.retrieved_memories,

            # Tool execution tracking
            "last_tool": self.last_tool,
            "tool_results": self.tool_results,
            "failed_attempts": self.failed_attempts,

            # Messages and conversation
            "messages": self.messages,

            # Legacy workflow compatibility
            "current_step": self.current_step,
            "next_action": self.next_action,
            "should_continue": self.should_continue,
            "error_message": self.error_message,

            # ReAct-specific fields
            "current_phase": self.current_phase.value,
            "step_count": self.step_count,
            "max_steps": self.max_steps,
            "current_plan": self.current_plan.to_dict() if self.current_plan else None,
            "safety_decision": self.safety_decision.to_dict() if self.safety_decision else None,
            "step_result": self.step_result,
            "reflection": self.reflection.to_dict() if self.reflection else None,
            "awaiting_user_response": self.awaiting_user_response,
            "pending_questions": self.pending_questions,
            "user_responses": self.user_responses,
            "step_history": self.step_history,
            "conversation_context": self.conversation_context,
            "user_goal_achieved": self.user_goal_achieved,
            "reason_for_completion": self.reason_for_completion
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ReActState':
        """Create ReActState from dictionary."""
        # Create ReActState directly from data
        state = cls(
            project_id=data.get("project_id", ""),
            session_id=data.get("session_id", ""),
            user_goal=data.get("user_goal", ""),
            mode=AgentMode(data.get("mode", "think")),
            context_snippets=data.get("context_snippets", []),
            feedback_topics=data.get("feedback_topics", []),
            retrieved_memories=data.get("retrieved_memories", []),
            last_tool=data.get("last_tool"),
            tool_results=data.get("tool_results", []),
            failed_attempts=data.get("failed_attempts", 0),
            messages=data.get("messages", []),
            current_step=data.get("current_step", ""),
            next_action=data.get("next_action", ""),
            should_continue=data.get("should_continue", True),
            error_message=data.get("error_message")
        )

        # Set ReAct-specific fields
        state.current_phase = ReActPhase(data.get("current_phase", "ground_context"))
        state.step_count = data.get("step_count", 0)
        state.max_steps = data.get("max_steps", 10)

        if data.get("current_plan"):
            state.current_plan = StepPlan.from_dict(data["current_plan"])

        if data.get("safety_decision"):
            state.safety_decision = SafetyDecision.from_dict(data["safety_decision"])

        state.step_result = data.get("step_result")

        if data.get("reflection"):
            state.reflection = ReflectionResult.from_dict(data["reflection"])

        state.awaiting_user_response = data.get("awaiting_user_response", False)
        state.pending_questions = data.get("pending_questions", [])
        state.user_responses = data.get("user_responses", [])
        state.step_history = data.get("step_history", [])
        state.conversation_context = data.get("conversation_context", {})
        state.user_goal_achieved = data.get("user_goal_achieved", False)
        state.reason_for_completion = data.get("reason_for_completion", "")

        return state
