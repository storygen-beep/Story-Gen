"""
ReAct Workflow for Elora Agent.

True ReAct (Reasoning and Acting) pattern implementation with:
- Single-step micro-planning
- Safety gates (ASK/Confirm/Dry-run)
- Reflection and learning
- Conversational flow management

Phase 1 Enhancement: Integrates Phase 1 Policy Engine with TAU thresholds,
canonical tool routing, and VALIDATE/SYNTHESIZE_RESPONSE phases for
deterministic goal completion and loop prevention.
"""

import logging
import time
import traceback
from typing import Any

from ..services.ai_service import AIService
from ..services.phase1_policy_engine import get_phase1_policy_engine
from ..services.planner import Planner
from ..services.workflow_logger import ReActWorkflowLogger
from .react_state import (
    ReActPhase,
    ReActState,
    SafetyVerdict,
    StepPlan,
    ValidationResult,
)
from .tools import AgentToolKit

logger = logging.getLogger(__name__)


class ReActWorkflow:
    """
    True ReAct pattern workflow orchestrator.

    Implements the ReAct loop:
    1. Ground Context → 2. Plan Single Step → 3. Safety Gate → 4. Execute → 5. Reflect → Repeat

    Key differences from batch workflow:
    - Single step planning instead of batch planning
    - Safety policy gates before execution
    - Reflection after each step with learning
    - ASK/Confirm flows for ambiguous/destructive operations
    """

    def __init__(
        self,
        project_id: str,
        model_name: str = None,
        session_logger: ReActWorkflowLogger = None,
    ):
        self.project_id = project_id
        self.tools = AgentToolKit(project_id)
        self.session_logger = session_logger
        self.ai_service = AIService(model_name, session_logger)

        # Phase 1 Enhancement: Initialize Planner and Policy Engine
        self.planner = Planner(project_id)
        self.policy_engine = get_phase1_policy_engine(project_id)

        # Workflow phase handlers (Phase 1 enhanced)
        self.phase_handlers = {
            ReActPhase.GROUND_CONTEXT: self._ground_context,
            ReActPhase.PLAN_STEP: self._plan_single_step,
            ReActPhase.SAFETY_GATE: self._safety_gate,
            ReActPhase.EXECUTE_STEP: self._execute_step,
            ReActPhase.VALIDATE: self._validate_step_result,  # Phase 1 addition
            ReActPhase.SYNTHESIZE_RESPONSE: self._synthesize_response,  # Phase 1 addition
            ReActPhase.REFLECT: self._reflect_on_step,
            ReActPhase.ASK_USER: self._handle_ask_mode,
            ReActPhase.AWAIT_CONFIRMATION: self._handle_confirmation,
        }

        logger.info(
            f"ReAct Workflow initialized with AI model: {self.ai_service.model_name}"
        )
        logger.info(
            f"Phase 1 Policy Engine initialized with TAU thresholds: {self.policy_engine.TAU_LOW}/{self.policy_engine.TAU_HIGH}"
        )
        if self.session_logger:
            self.session_logger.log_session_start(
                user_goal="Starting ReAct workflow", ai_model=self.ai_service.model_name
            )

    def run_react_loop(self, state: ReActState, user_input: str = None) -> ReActState:
        """
        Run the ReAct loop until completion or user input required.

        Args:
            state: Current ReAct state
            user_input: New user input (for initial request or responses to ASK/Confirm)

        Returns:
            Updated state (may be awaiting user response)
        """
        # Handle new user input
        if user_input:
            state.add_message("user", user_input)

            # Log user interaction
            if self.session_logger:
                interaction_type = (
                    "new_goal" if not state.user_goal else "user_response"
                )
                self.session_logger.log_user_interaction(
                    interaction_type=interaction_type,
                    content=user_input,
                    context={"awaiting_response": state.awaiting_user_response},
                )

            # If this is a new conversation OR a different goal, reset the workflow
            if not state.user_goal or user_input.strip() != state.user_goal.strip():
                # New goal - reset workflow state for fresh processing
                state.user_goal = user_input
                state.current_phase = ReActPhase.GROUND_CONTEXT
                state.step_count = 0
                state.user_goal_achieved = False
                state.reason_for_completion = ""
                state.current_plan = None
                state.safety_decision = None
                state.step_result = None
                state.validation_result = None
                state.policy_decision = None
                state.final_response = None
                # Keep conversation history and context but reset workflow state
                logger.info(
                    f"New goal detected: '{user_input}' (previous: '{state.user_goal if state.user_goal != user_input else 'None'}')"
                )

                if self.session_logger:
                    self.session_logger.log_session_start(
                        user_goal=user_input, ai_model=self.ai_service.model_name
                    )
            # If we were waiting for user response, add it
            elif state.awaiting_user_response:
                state.add_user_response(user_input)

        try:
            # Run ReAct loop until completion or user input needed
            while state.should_continue_react_loop():
                step_start_time = time.time()
                current_step = state.step_count + 1
                current_phase = state.current_phase.value

                logger.info(f"ReAct Step {current_step}: {current_phase}")

                # Log phase start
                if self.session_logger:
                    self.session_logger.log_phase_start(current_phase, current_step)

                # Execute current phase
                if state.current_phase in self.phase_handlers:
                    phase_handler = self.phase_handlers[state.current_phase]
                    state = phase_handler(state)

                    # Log phase completion
                    if self.session_logger:
                        duration_ms = (time.time() - step_start_time) * 1000
                        self.session_logger.log_phase_complete(
                            current_phase, current_step, duration_ms
                        )

                    # Increment step counter after each phase
                    if (
                        state.current_phase != ReActPhase.ASK_USER
                        and state.current_phase != ReActPhase.AWAIT_CONFIRMATION
                    ):
                        state.step_count += 1

                else:
                    error_msg = f"Unknown phase: {state.current_phase}"
                    state.error_message = error_msg
                    if self.session_logger:
                        self.session_logger.log_error(
                            error_type="UNKNOWN_PHASE",
                            error_message=error_msg,
                            context={"phase": state.current_phase},
                        )
                    break

                # Check if we need to wait for user input
                if state.awaiting_user_response:
                    if self.session_logger:
                        self.session_logger.log_loop_control(
                            action="pause_for_user",
                            reason="Awaiting user response",
                            step_count=state.step_count,
                            max_steps=state.max_steps,
                            should_continue=False,
                        )
                    break

                # Safety check to prevent infinite loops
                if state.step_count >= state.max_steps:
                    state.reason_for_completion = (
                        f"Reached maximum steps ({state.max_steps})"
                    )
                    state.user_goal_achieved = False
                    if self.session_logger:
                        self.session_logger.log_loop_control(
                            action="max_steps_reached",
                            reason=state.reason_for_completion,
                            step_count=state.step_count,
                            max_steps=state.max_steps,
                            should_continue=False,
                        )
                    break

            # Add final summary if conversation is complete
            if (
                not state.awaiting_user_response
                and not state.user_goal_achieved
                and not state.final_response
            ):
                state.add_message("assistant", self._generate_completion_summary(state))

        except Exception as e:
            error_msg = str(e)
            stack_trace = traceback.format_exc()
            logger.error(f"ReAct workflow error: {e}")
            state.error_message = error_msg
            state.add_message("assistant", f"I encountered an error: {error_msg}")

            # Log detailed error information
            if self.session_logger:
                self.session_logger.log_error(
                    error_type="WORKFLOW_ERROR",
                    error_message=error_msg,
                    context={
                        "current_phase": state.current_phase.value,
                        "step_count": state.step_count,
                        "user_goal": state.user_goal,
                    },
                    stack_trace=stack_trace,
                )

        # Log session end if workflow is complete
        if self.session_logger and (
            not state.should_continue_react_loop() or state.error_message
        ):
            # Log AI service usage summary before ending session
            ai_usage_summary = self.ai_service.get_session_usage_summary()
            self.session_logger.log_ai_decision(
                decision_type="SESSION_USAGE_SUMMARY",
                reasoning="AI service usage for complete ReAct session",
                confidence=1.0,
                tool="ai_service",
                arguments=ai_usage_summary,
            )

            self.session_logger.log_session_end(
                reason=state.reason_for_completion
                or state.error_message
                or "User interaction required",
                total_steps=state.step_count,
                user_goal_achieved=state.user_goal_achieved,
            )

        return state

    def _ground_context(self, state: ReActState) -> ReActState:
        """
        Ground context by retrieving relevant information.

        This is the 'Reasoning' part where we gather context before planning.
        """
        logger.debug("Grounding context for ReAct step")

        context_parts = []

        try:
            # Search for relevant memories if we have a user goal
            if state.user_goal:
                memory_result = self.tools.memory_search(query=state.user_goal, limit=5)

                # Log memory search operation
                if self.session_logger:
                    self.session_logger.log_memory_operation(
                        operation="search",
                        query=state.user_goal,
                        result_count=len(memory_result.get("memories", [])),
                        context={"success": memory_result.get("success", False)},
                    )

                if memory_result.get("success") and memory_result.get("memories"):
                    state.retrieved_memories = memory_result["memories"]
                    context_parts.append(
                        f"Retrieved {len(state.retrieved_memories)} relevant memories"
                    )

                    # Extract topics for tracking
                    state.feedback_topics = [
                        mem["topic"]
                        for mem in state.retrieved_memories
                        if mem["kind"] == "feedback"
                    ]

            # Get canvas summary for context using canonical tool
            canvas_result = self.tools.describe_canvas()
            if canvas_result.get("success"):
                if canvas_result.get("type") == "summary":
                    canvas_data = canvas_result["project"]
                    canvas_count = canvas_data.get("canvas_count", 0)
                    context_parts.append(f"Project has {canvas_count} story canvases")

                    # Store enhanced context for policy engine
                    state.conversation_context["canvas_summary"] = canvas_data

                    # Extract canvas names for better context matching
                    canvas_names = [
                        c.get("name", "") for c in canvas_data.get("canvases", [])
                    ]
                    state.conversation_context["canvas_names"] = canvas_names

                    # Log canvas context retrieval
                    if self.session_logger:
                        self.session_logger.log_memory_operation(
                            operation="canvas_summary",
                            result_count=canvas_count,
                            context={"canvases": canvas_names},
                        )

            # Update conversation context
            grounding_summary = (
                "; ".join(context_parts)
                if context_parts
                else "No specific context found"
            )
            state.conversation_context["latest_grounding"] = grounding_summary

            state.add_message("system", f"Context: {grounding_summary}")
            logger.debug(f"Context grounded: {grounding_summary}")

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error grounding context: {e}")
            state.add_message("system", f"Context grounding error: {error_msg}")

            # Log grounding error
            if self.session_logger:
                self.session_logger.log_error(
                    error_type="GROUNDING_ERROR",
                    error_message=error_msg,
                    context={"user_goal": state.user_goal},
                )

        # Move to planning phase
        state.current_phase = ReActPhase.PLAN_STEP

        return state

    def _plan_single_step(self, state: ReActState) -> ReActState:
        """
        Plan a single step using Phase 1 Planner.

        Phase 1 Enhancement: Uses Planner for tool selection and argument formation,
        separated from Policy (safety decisions).
        """
        logger.info("📋 WORKFLOW TRACE: Entering PLAN_STEP phase")
        logger.debug("Planning single ReAct step using Phase 1 Planner")

        # Build context for planner
        current_context = state.conversation_context.copy()
        current_context.update(
            {
                "project_id": self.project_id,
                "step_count": state.step_count,
                "messages": state.messages[-3:],  # Recent context
                "retrieved_memories": len(state.retrieved_memories),
                "tool_results": state.tool_results[-2:] if state.tool_results else [],
                "failed_attempts": state.failed_attempts,
            }
        )

        # GPT-5 Fix: Use Planner (no fallback, no tool changes after this point)
        # Planner now handles all errors internally and returns low-confidence plans for ASK flow
        state.current_plan = self.planner.plan_single_step(
            user_goal=state.user_goal,
            context=current_context,
            tool_candidates=[],  # No heuristic hints for now
        )

        logger.info(
            f"📋 WORKFLOW TRACE: Planner returned {state.current_plan.tool} (confidence: {state.current_plan.confidence:.2f})"
        )
        logger.debug(f"Planner rationale: {state.current_plan.rationale}")

        state.add_message("system", f"Planned step: {state.current_plan.rationale}")
        state.current_phase = ReActPhase.SAFETY_GATE

        return state

    def _safety_gate(self, state: ReActState) -> ReActState:
        """
        Apply safety policy to determine if step can proceed.

        Phase 1 Enhancement: Uses Phase 1 Policy Engine for deterministic safety decisions.
        """
        logger.debug("Applying safety gate using Phase 1 Policy Engine")

        if not state.current_plan:
            state.error_message = "No plan available for safety evaluation"
            return state

        try:
            # Use Phase 1 Policy Engine for safety decision
            policy_decision = self.policy_engine.decide(
                step_plan=state.current_plan,
                tau_low=self.policy_engine.TAU_LOW,
                tau_high=self.policy_engine.TAU_HIGH,
                asks_so_far=len(state.pending_questions),
            )

            verdict = policy_decision.verdict
            logger.info(f"Safety verdict: {verdict} - {policy_decision.reasoning}")

            # Route to appropriate next phase based on Phase 1 verdict
            if verdict == "proceed":
                state.current_phase = ReActPhase.EXECUTE_STEP

            elif verdict == "ask":
                state.set_pending_questions(policy_decision.questions)
                state.current_phase = ReActPhase.ASK_USER

            elif verdict in ["confirm", "dry_run"]:
                # Create SafetyDecision for confirmation flow
                from ..agent.react_state import SafetyDecision

                safety_verdict = (
                    SafetyVerdict.DRY_RUN
                    if verdict == "dry_run"
                    else SafetyVerdict.CONFIRM
                )
                state.safety_decision = SafetyDecision(
                    verdict=safety_verdict,
                    confidence=policy_decision.confidence,
                    reasoning=policy_decision.reasoning,
                    required_confirmations=[
                        f"Confirm: {state.current_plan.expected_effect}"
                    ],
                    dry_run_preview=(
                        f"Preview: {state.current_plan.tool} with args {state.current_plan.args}"
                        if verdict == "dry_run"
                        else ""
                    ),
                )

                # Show a pre-execution preview to the user (prevents “execute-then-ask”)
                try:
                    preview_msg = self._generate_dry_run_preview(
                        state.current_plan, state
                    )
                    if preview_msg:
                        state.add_message("assistant", preview_msg)
                except Exception as _e:
                    logger.warning(f"Failed to build dry-run preview: {_e}")
                state.current_phase = ReActPhase.AWAIT_CONFIRMATION

            elif verdict == "deny":
                state.error_message = (
                    f"Policy denied action: {policy_decision.reasoning}"
                )
                logger.warning(f"Action denied by policy: {policy_decision.reasoning}")

            else:
                state.error_message = f"Unknown safety verdict: {verdict}"
                logger.error(f"Unknown safety verdict from policy: {verdict}")

        except Exception as e:
            logger.error(f"Safety gate error: {e}")
            state.error_message = f"Safety evaluation failed: {str(e)}"

        return state

    def _execute_step(self, state: ReActState) -> ReActState:
        """
        Execute the planned step.

        This is the 'Acting' part of ReAct.
        """
        logger.debug("Executing planned step")

        if not state.current_plan:
            state.error_message = "No plan available for execution"
            return state

        try:
            # Execute the tool with planned arguments
            result = self._execute_tool(
                state.current_plan.tool, state.current_plan.args, state
            )

            # Store step result
            state.step_result = result
            state.add_tool_result(
                state.current_plan.tool, result, result.get("success", False)
            )

            if result.get("success", False):
                logger.info(f"Step executed successfully: {state.current_plan.tool}")
                state.reset_failures()
            else:
                logger.warning(
                    f"Step execution failed: {result.get('error', 'Unknown error')}"
                )
                state.increment_failures()

            # Store step in history
            state.add_step_to_history(result)

        except Exception as e:
            logger.error(f"Step execution error: {e}")
            error_result = {"success": False, "error": str(e)}
            state.step_result = error_result
            state.add_tool_result(state.current_plan.tool, error_result, False)
            state.increment_failures()

        # Phase 1 Enhancement: Move to validation instead of reflection
        state.current_phase = ReActPhase.VALIDATE

        return state

    def _validate_step_result(self, state: ReActState) -> ReActState:
        """
        Phase 1 VALIDATE phase - validate tool execution result.

        Validates tool results and determines next action based on validation outcome.
        This phase prevents invalid results from propagating and enables retry logic.
        """
        logger.debug("Validating step result")

        if not state.step_result:
            state.validation_result = ValidationResult(
                is_valid=False,
                confidence=0.0,
                error_reasons=["No step result to validate"],
                should_retry=False,
            )
            state.current_phase = ReActPhase.SYNTHESIZE_RESPONSE
            return state

        try:
            # Basic validation checks
            is_success = state.step_result.get("success", False)
            has_error = "error" in state.step_result

            # Validation logic
            if is_success and not has_error:
                # Phase 1 Enhancement: Add trigger consistency validation after writes
                validation_warnings = []
                validation_errors = []

                if self._is_canvas_write_operation(state.current_plan):
                    trigger_validation = self._validate_trigger_consistency(
                        state.current_plan, state.step_result
                    )
                    validation_warnings.extend(trigger_validation.get("warnings", []))
                    validation_errors.extend(trigger_validation.get("errors", []))

                # Get policy engine evaluation of result
                policy_decision = self.policy_engine.evaluate_tool_result(
                    tool_name=(
                        state.current_plan.tool if state.current_plan else "unknown"
                    ),
                    tool_result=state.step_result,
                    original_goal=state.user_goal,
                )

                # Create validation result based on policy decision
                # Include trigger validation warnings in the result
                has_validation_errors = len(validation_errors) > 0

                if policy_decision.verdict == "synthesize_response":
                    state.validation_result = ValidationResult(
                        is_valid=not has_validation_errors,  # Only invalid if there are trigger errors
                        confidence=policy_decision.confidence,
                        should_retry=False,
                        error_reasons=validation_errors,
                        warnings=validation_warnings,
                    )

                    # Log trigger validation results
                    if validation_warnings or validation_errors:
                        logger.info(
                            f"Trigger validation: {len(validation_errors)} errors, {len(validation_warnings)} warnings"
                        )
                        if validation_errors:
                            logger.warning(
                                f"Trigger validation errors: {validation_errors}"
                            )

                    state.current_phase = ReActPhase.SYNTHESIZE_RESPONSE

                elif policy_decision.verdict == "ask":
                    state.validation_result = ValidationResult(
                        is_valid=False,
                        confidence=policy_decision.confidence,
                        should_retry=False,
                        retry_suggestion="Need clarification from user",
                        error_reasons=validation_errors,
                        warnings=validation_warnings,
                    )
                    state.set_pending_questions(policy_decision.questions)
                    state.current_phase = ReActPhase.ASK_USER

                elif policy_decision.verdict in ["dry_run", "confirm"]:
                    # These are handled by SAFETY_GATE phase, not VALIDATE
                    state.validation_result = ValidationResult(
                        is_valid=not has_validation_errors,
                        confidence=policy_decision.confidence,
                        should_retry=False,
                        error_reasons=validation_errors,
                        warnings=validation_warnings,
                    )
                    # This shouldn't normally happen in Phase 1, but handle gracefully
                    logger.warning(
                        f"Policy returned {policy_decision.verdict} during VALIDATE phase"
                    )
                    state.current_phase = ReActPhase.SYNTHESIZE_RESPONSE

                else:
                    # Default case - proceed with current result
                    state.validation_result = ValidationResult(
                        is_valid=not has_validation_errors,
                        confidence=policy_decision.confidence,
                        should_retry=False,
                        error_reasons=validation_errors,
                        warnings=validation_warnings,
                    )
                    state.current_phase = ReActPhase.SYNTHESIZE_RESPONSE

            else:
                # Failed result - check if we should retry
                error_msg = state.step_result.get("error", "Unknown error")
                should_retry = (
                    state.failed_attempts < 2
                    and "not found" not in error_msg.lower()
                    and "permission" not in error_msg.lower()
                )

                state.validation_result = ValidationResult(
                    is_valid=False,
                    confidence=0.2,
                    error_reasons=[error_msg],
                    should_retry=should_retry,
                    retry_suggestion=(
                        "Retry with different approach" if should_retry else None
                    ),
                )

                if should_retry:
                    logger.info(f"Validation failed, retrying: {error_msg}")
                    state.current_phase = ReActPhase.PLAN_STEP  # Retry with new plan
                else:
                    logger.info(f"Validation failed, no retry: {error_msg}")
                    state.current_phase = (
                        ReActPhase.SYNTHESIZE_RESPONSE
                    )  # Give up and respond

            logger.info(
                f"Validation result: valid={state.validation_result.is_valid}, confidence={state.validation_result.confidence:.2f}"
            )

        except Exception as e:
            logger.error(f"Validation error: {e}")
            state.validation_result = ValidationResult(
                is_valid=False,
                confidence=0.0,
                error_reasons=[f"Validation failed: {str(e)}"],
                should_retry=False,
            )
            state.current_phase = ReActPhase.SYNTHESIZE_RESPONSE

        return state

    def _synthesize_response(self, state: ReActState) -> ReActState:
        """
        Phase 1 SYNTHESIZE_RESPONSE phase - generate final response to user.

        This phase ensures the user always gets a meaningful response and prevents
        infinite loops by providing goal completion or explanation of what was accomplished.
        """
        logger.debug("Synthesizing final response")

        try:
            # Gather information for response synthesis
            response_context = {
                "user_goal": state.user_goal,
                "tool_results": state.tool_results,
                "step_count": state.step_count,
                "validation_result": (
                    state.validation_result.to_dict()
                    if state.validation_result
                    else None
                ),
                "policy_stats": self.policy_engine.get_session_stats(),
            }

            # Determine if goal was achieved based on validation and policy
            goal_achieved = False
            if state.validation_result and state.validation_result.is_valid:
                if state.validation_result.confidence >= self.policy_engine.TAU_HIGH:
                    goal_achieved = True

            # Generate response using AI service
            if goal_achieved:
                final_response = self.ai_service.summarize_results(
                    user_goal=state.user_goal,
                    tool_results=state.tool_results,
                    mode="react_success",
                )
                state.user_goal_achieved = True
                state.reason_for_completion = "Goal successfully completed"

            else:
                # Generate helpful response even for partial success
                final_response = self.ai_service.summarize_results(
                    user_goal=state.user_goal,
                    tool_results=state.tool_results,
                    mode="react_partial",
                )
                state.user_goal_achieved = False
                state.reason_for_completion = "Provided available information"

            # Phase 1: No caching in Phase 1 implementation

            state.final_response = final_response
            state.add_message("assistant", final_response)

            logger.info(
                f"Response synthesized: goal_achieved={goal_achieved}, length={len(final_response)}"
            )

        except Exception as e:
            logger.error(f"Response synthesis error: {e}")
            # Fallback response
            fallback_response = f"I encountered an issue while processing your request. I completed {state.step_count} steps but couldn't provide a complete response. Error: {str(e)}"
            state.final_response = fallback_response
            state.add_message("assistant", fallback_response)
            state.user_goal_achieved = False
            state.reason_for_completion = f"Synthesis error: {str(e)}"

        # End the conversation - this phase always completes the workflow
        return state

    def _reflect_on_step(self, state: ReActState) -> ReActState:
        """
        Reflect on the completed step and learn.

        This is the key ReAct component - analyzing results and planning next steps.
        """
        logger.debug("Reflecting on completed step")

        try:
            # Use AI to reflect on the step outcome
            reflection_data = self.ai_service.reflect_on_step_result(
                step_plan=state.current_plan.to_dict() if state.current_plan else {},
                step_result=state.step_result or {},
                user_goal=state.user_goal,
                conversation_context=state.conversation_context,
            )

            # Create reflection object
            from .react_state import ReflectionResult

            state.reflection = ReflectionResult.from_dict(reflection_data)

            # Check if goal is achieved
            if state.reflection.success and reflection_data.get("goal_achieved", False):
                state.user_goal_achieved = True
                state.reason_for_completion = "User goal achieved successfully"

                # Generate final response
                final_response = self.ai_service.summarize_results(
                    user_goal=state.user_goal,
                    tool_results=state.tool_results,
                    mode="react",
                )
                state.add_message("assistant", final_response)

                logger.info("ReAct loop completed: Goal achieved")
                return state

            # If not complete, plan next step
            if state.reflection.next_step_suggestion:
                logger.info(
                    f"Reflection suggests: {state.reflection.next_step_suggestion}"
                )

            # Continue with next iteration
            state.current_phase = ReActPhase.GROUND_CONTEXT

        except Exception as e:
            logger.error(f"Reflection error: {e}")
            # Continue anyway with basic reflection
            from .react_state import ReflectionResult

            state.reflection = ReflectionResult(
                success=(
                    state.step_result.get("success", False)
                    if state.step_result
                    else False
                ),
                outcome_matches_expectation=False,
                error_analysis=f"Reflection failed: {str(e)}",
            )

            # Continue to next step
            state.current_phase = ReActPhase.GROUND_CONTEXT

        return state

    def _handle_ask_mode(self, state: ReActState) -> ReActState:
        logger.debug("Handling ASK mode")

        # FIX: use pending_questions, not safety_decision.questions
        questions = getattr(state, "pending_questions", None)

        if not questions:
            state.error_message = "ASK mode triggered but no questions available"
            return state

        if not state.user_responses:
            questions_text = "\n".join([f"❓ {q}" for q in questions])
            state.add_message("assistant", f"I need clarification:\n\n{questions_text}")
            state.awaiting_user_response = True
            logger.info(f"Presented {len(questions)} questions to user")
        else:
            response_text = " ".join(state.user_responses)
            enhanced_goal = f"{state.user_goal}. Additional context: {response_text}"
            state.user_goal = enhanced_goal
            state.user_responses.clear()
            state.pending_questions.clear()
            state.awaiting_user_response = False
            state.current_phase = ReActPhase.PLAN_STEP

        return state

    def _handle_confirmation(self, state: ReActState) -> ReActState:
        """
        Handle confirmation mode - show preview and process approval.
        """
        logger.debug("Handling confirmation mode")

        if not state.safety_decision:
            state.error_message = (
                "Confirmation mode triggered but no safety decision available"
            )
            return state

        # If we don't have user response yet, show preview/confirmation
        if not state.user_responses:
            if state.safety_decision.verdict == SafetyVerdict.DRY_RUN:
                # Show dry-run preview from safety engine
                preview = (
                    state.safety_decision.dry_run_preview
                    or f"**Preview**: {state.current_plan.expected_effect}\n\nProceed with this action?"
                )
                state.add_message("assistant", preview)

            elif state.safety_decision.verdict == SafetyVerdict.CONFIRM:
                # Show confirmation request
                confirmations_text = "\n".join(
                    [f"⚠️  {c}" for c in state.safety_decision.required_confirmations]
                )
                state.add_message(
                    "assistant", f"Please confirm:\n\n{confirmations_text}"
                )

            # Wait for user confirmation
            state.awaiting_user_response = True
            logger.info(
                f"Awaiting user confirmation for {state.safety_decision.verdict.value}"
            )

        else:
            # Process user confirmation response
            user_response = " ".join(state.user_responses).lower().strip()
            logger.info(f"Processing confirmation response: '{user_response}'")

            # Check if user approved
            approval_words = [
                "yes",
                "y",
                "ok",
                "okay",
                "proceed",
                "continue",
                "approve",
                "confirm",
            ]
            denial_words = ["no", "n", "cancel", "stop", "decline", "deny"]

            if any(word in user_response for word in approval_words):
                # User approved - proceed to execution
                logger.info("User approved action - proceeding to execution")

                # Phase 1 Enhancement: Handle overwrite confirmations
                if (
                    state.current_plan
                    and state.current_plan.tool == "create_node"
                    and state.step_result
                    and state.step_result.get("requires_overwrite")
                ):
                    # Store overwrite confirmation in context for tool adapter
                    state.conversation_context["create_node_overwrite_confirmed"] = True
                    state.conversation_context["overwrite_canvas_id"] = (
                        state.step_result.get("canvas_id")
                    )
                    logger.info(
                        f"Confirmed overwrite for create_node in canvas {state.step_result.get('canvas_id')}"
                    )

                state.awaiting_user_response = False
                state.user_responses.clear()
                state.current_phase = ReActPhase.EXECUTE_STEP

            elif any(word in user_response for word in denial_words):
                # User declined - go back to planning
                logger.info("User declined action - returning to planning")
                state.awaiting_user_response = False
                state.user_responses.clear()
                state.add_message(
                    "assistant", "Understood. Let me plan a different approach."
                )
                state.current_phase = ReActPhase.PLAN_STEP

            else:
                # Unclear response - ask for clarification
                state.add_message(
                    "assistant",
                    "I'm not sure if you want to proceed. Please respond with 'yes' to continue or 'no' to cancel.",
                )
                state.user_responses.clear()  # Clear and wait for clearer response

        return state

    def _get_tool_destructiveness(self, tool_name: str) -> str:
        """
        Get destructiveness level for a tool using Tool Manifest Registry.

        Args:
            tool_name: Name of the tool

        Returns:
            Destructiveness level: "read_only", "low_write", "high_write"
        """
        try:
            destructiveness = self.tools.tool_registry.get_destructiveness(tool_name)
            return destructiveness if destructiveness else "read_only"
        except Exception:
            # Fallback for unknown tools
            if "delete" in tool_name.lower():
                return "high_write"
            elif (
                "create" in tool_name.lower()
                or "patch" in tool_name.lower()
                or "put" in tool_name.lower()
            ):
                return "low_write"
            else:
                return "read_only"

    def _execute_tool(
        self, tool_name: str, args: dict[str, Any], state: ReActState
    ) -> dict[str, Any]:
        """
        Execute a tool with the given arguments.

        Routes to appropriate tool implementation in AgentToolKit with enhanced logging.
        """
        tool_start_time = time.time()

        # Enhanced logging: Log raw tool arguments before processing
        if self.session_logger:
            self.session_logger.log_tool_execution(
                tool=tool_name,
                arguments={
                    "raw_args": args,
                    "arg_types": {k: type(v).__name__ for k, v in args.items()},
                    "arg_count": len(args),
                    "state_context": {
                        "step_count": state.step_count,
                        "phase": state.current_phase.value,
                        "goal": state.user_goal[:100] if state.user_goal else None,
                    },
                },
                result={"status": "starting", "timestamp": time.time()},
                duration_ms=0,
            )

        try:
            # Process and validate arguments
            processed_args = self._process_tool_args(tool_name, args)

            # Route to appropriate tool method with processed args
            # Phase 1 Enhancement: Route to canonical tools first, then legacy for compatibility
            raw_result = None

            # Phase 1 canonical tools (priority routing)
            if tool_name == "describe_canvas":
                raw_result = self.tools.describe_canvas(**processed_args)
            elif tool_name == "search_nodes":
                raw_result = self.tools.search_nodes(**processed_args)
            elif tool_name == "create_node":
                # Phase 1 Enhancement: Check for overwrite confirmation
                if state.conversation_context.get(
                    "create_node_overwrite_confirmed"
                ) and state.conversation_context.get(
                    "overwrite_canvas_id"
                ) == processed_args.get(
                    "canvas_id"
                ):
                    # Add overwrite confirmation to args
                    processed_args["overwrite_confirmed"] = True
                    # Clear the confirmation flag
                    state.conversation_context["create_node_overwrite_confirmed"] = (
                        False
                    )
                    del state.conversation_context["overwrite_canvas_id"]
                    logger.info(
                        f"Passing overwrite confirmation for canvas {processed_args.get('canvas_id')}"
                    )

                raw_result = self.tools.create_node(**processed_args)
            elif tool_name == "delete_canvas":
                raw_result = self.tools.delete_canvas(**processed_args)

            # Legacy tools for backward compatibility
            elif tool_name == "memory_search":
                raw_result = self.tools.memory_search(**processed_args)
            elif tool_name == "memory_put":
                raw_result = self.tools.memory_put(**processed_args)
            elif tool_name == "story_read_canvas":
                raw_result = self.tools.story_read_canvas(**processed_args)
            elif tool_name == "story_create_canvas":
                raw_result = self.tools.story_create_canvas(**processed_args)
            elif tool_name == "story_patch_canvas":
                raw_result = self.tools.story_patch_canvas(**processed_args)
            elif tool_name == "story_find_canvas":
                raw_result = self.tools.story_find_canvas(**processed_args)
            elif tool_name == "world_read_locations":
                raw_result = self.tools.world_read_locations(**processed_args)
            elif tool_name == "feedback_store":
                raw_result = self.tools.feedback_store(**processed_args)
            elif tool_name == "hybrid_search":
                raw_result = self.tools.hybrid_search(**processed_args)
            else:
                # Check if it's a valid tool in the manifest registry
                if self.tools.tool_registry.is_valid_tool(tool_name):
                    raw_result = {
                        "success": False,
                        "error": f"Tool '{tool_name}' exists but routing not implemented",
                    }
                else:
                    raw_result = {
                        "success": False,
                        "error": f"Unknown tool: {tool_name}",
                    }

            # Parse and transform the response
            final_result = self._parse_tool_response(tool_name, raw_result, args)

            # Calculate execution duration
            duration_ms = (time.time() - tool_start_time) * 1000

            # Enhanced logging: Log complete tool execution with detailed results
            if self.session_logger:
                self.session_logger.log_tool_execution(
                    tool=tool_name,
                    arguments={
                        "processed_arguments": processed_args,
                        # "validation_results": self._validate_tool_args(tool_name, args),
                        # Validate the processed args (not the raw ones) for truthful logs
                        "validation_results": self._validate_tool_args(
                            tool_name, processed_args
                        ),
                        "argument_transformations": self._get_arg_transformations(
                            args, processed_args
                        ),
                    },
                    result={
                        "raw_response": raw_result,
                        "parsed_response": final_result,
                        "response_size": self._calculate_response_size(raw_result),
                        "success": final_result.get("success", False),
                        "performance_metrics": {
                            "execution_time_ms": duration_ms,
                            "response_processing_time_ms": self._get_processing_time(
                                raw_result, final_result
                            ),
                            "memory_impact": self._estimate_memory_impact(raw_result),
                        },
                    },
                    duration_ms=duration_ms,
                )

            return final_result

        except Exception as e:
            duration_ms = (time.time() - tool_start_time) * 1000
            error_details = {
                "exception_type": type(e).__name__,
                "exception_message": str(e),
                "traceback_summary": traceback.format_exc()[-500:],  # Last 500 chars
                "tool_context": {
                    "args_provided": list(args.keys()),
                    "execution_stage": "tool_routing",
                },
            }

            logger.error(f"Tool execution error: {tool_name} - {e}")
            error_result = {
                "success": False,
                "error": str(e),
                "error_details": error_details,
            }

            # Enhanced logging: Log detailed error information
            if self.session_logger:
                self.session_logger.log_tool_execution(
                    tool=tool_name,
                    arguments=args,
                    result={
                        "error_result": error_result,
                        "error_analysis": error_details,
                        "retry_suggestion": self._suggest_retry_strategy(
                            tool_name, e, args
                        ),
                    },
                    duration_ms=duration_ms,
                )

            return error_result

    def _process_tool_args(
        self, tool_name: str, args: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Process and validate tool arguments before execution.

        Args:
            tool_name: Name of the tool being called
            args: Raw arguments from AI planning

        Returns:
            Processed and validated arguments
        """
        processed_args = args.copy()

        # Tool-specific argument processing
        if tool_name in ["memory_search", "hybrid_search"]:
            # Ensure query is string and limit is integer
            if "query" in processed_args and processed_args["query"] is not None:
                processed_args["query"] = str(processed_args["query"]).strip()
            if "limit" in processed_args:
                try:
                    processed_args["limit"] = int(processed_args["limit"])
                except (ValueError, TypeError):
                    processed_args["limit"] = 5  # Default

        elif tool_name == "memory_put":
            # Ensure required string fields
            for field in ["kind", "topic", "text"]:
                if field in processed_args and processed_args[field] is not None:
                    processed_args[field] = str(processed_args[field])

        elif tool_name in ["story_create_canvas", "story_patch_canvas"]:
            # Ensure name and description are strings
            if "name" in processed_args and processed_args["name"] is not None:
                processed_args["name"] = str(processed_args["name"]).strip()
            if (
                "description" in processed_args
                and processed_args["description"] is not None
            ):
                processed_args["description"] = str(processed_args["description"])

        return processed_args

    def _parse_tool_response(
        self, tool_name: str, raw_result: dict[str, Any], original_args: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Parse and transform tool response for consistency.

        Args:
            tool_name: Name of the tool that was called
            raw_result: Raw response from the tool
            original_args: Original arguments passed to the tool

        Returns:
            Parsed and enhanced response
        """
        if not isinstance(raw_result, dict):
            return {
                "success": False,
                "error": "Tool returned non-dict response",
                "raw_response": raw_result,
            }

        parsed_result = raw_result.copy()

        # Add metadata about the tool call
        parsed_result["_tool_metadata"] = {
            "tool_name": tool_name,
            "call_timestamp": time.time(),
            "args_hash": hash(str(sorted(original_args.items()))),
            "response_type": self._classify_response_type(raw_result),
        }

        # Tool-specific response enhancements
        if tool_name == "memory_search" and parsed_result.get("success"):
            # Add search result analysis
            memories = parsed_result.get("memories", [])
            parsed_result["_analysis"] = {
                "result_count": len(memories),
                "memory_types": list(set(m.get("kind", "unknown") for m in memories)),
                "relevance_scores": [
                    m.get("score", 0) for m in memories if "score" in m
                ],
            }

        elif tool_name == "hybrid_search" and parsed_result.get("success"):
            # Add search analysis
            results = parsed_result.get("results", [])
            parsed_result["_analysis"] = {
                "result_count": len(results),
                "entity_types": list(
                    set(r.get("entity_type", "unknown") for r in results)
                ),
                "avg_score": (
                    sum(r.get("score", 0) for r in results) / len(results)
                    if results
                    else 0
                ),
                "score_range": {
                    "min": min((r.get("score", 0) for r in results), default=0),
                    "max": max((r.get("score", 0) for r in results), default=0),
                },
            }

        elif tool_name.startswith("story_") and parsed_result.get("success"):
            # Add story operation metadata
            parsed_result["_analysis"] = {
                "operation_type": tool_name.replace("story_", ""),
                "data_size": self._calculate_response_size(raw_result),
                "contains_content": self._response_contains_story_content(raw_result),
            }

        return parsed_result

    def _validate_tool_args(
        self, tool_name: str, args: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Validate tool arguments and return validation results.

        Args:
            tool_name: Name of the tool
            args: Arguments to validate

        Returns:
            Validation results with warnings and suggestions
        """
        validation_result = {
            "valid": True,
            "warnings": [],
            "suggestions": [],
            "missing_optional": [],
        }

        # Define expected arguments for each tool
        tool_schemas = {
            "memory_search": {
                "required": [],
                "optional": ["query", "kind", "topic", "limit"],
            },
            "memory_put": {
                "required": ["kind", "topic", "text"],
                "optional": ["tags", "refs"],
            },
            "story_read_canvas": {"required": [], "optional": ["canvas_id"]},
            "story_create_canvas": {
                "required": ["name"],
                "optional": ["description", "location_id"],
            },
            "story_patch_canvas": {
                "required": ["canvas_id", "updates"],
                "optional": [],
            },
            "story_find_canvas": {"required": ["query"], "optional": []},
            "hybrid_search": {
                "required": ["query"],
                "optional": ["entity_types", "limit", "filters"],
            },
            "describe_canvas": {  # Canonical Phase-1 tools (so validations are accurate)
                "required": [],
                "optional": ["canvas_id"],
            },
            "search_nodes": {"required": ["canvas_id", "query"], "optional": ["limit"]},
            "create_node": {
                "required": ["canvas_id", "title", "content"],
                "optional": ["overwrite_confirmed"],
            },
            "delete_canvas": {"required": ["canvas_id"], "optional": []},
        }

        schema = tool_schemas.get(tool_name, {"required": [], "optional": []})

        # Check for missing required arguments
        for req_arg in schema["required"]:
            if req_arg not in args or args[req_arg] is None:
                validation_result["valid"] = False
                validation_result["warnings"].append(
                    f"Missing required argument: {req_arg}"
                )

        # Check for missing helpful optional arguments
        for opt_arg in schema["optional"]:
            if opt_arg not in args:
                validation_result["missing_optional"].append(opt_arg)
                if opt_arg == "limit" and tool_name.endswith("search"):
                    validation_result["suggestions"].append(
                        "Consider adding 'limit' to control result count"
                    )

        # Tool-specific validations
        if tool_name == "memory_put" and "kind" in args:
            valid_kinds = ["episodic", "semantic", "feedback", "artifacts"]
            if args["kind"] not in valid_kinds:
                validation_result["warnings"].append(
                    f"Unusual memory kind: {args['kind']}. Expected: {valid_kinds}"
                )

        return validation_result

    def _get_arg_transformations(
        self, original_args: dict[str, Any], processed_args: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """
        Track what transformations were applied to arguments.

        Args:
            original_args: Original arguments from AI
            processed_args: Processed arguments after validation

        Returns:
            List of transformations applied
        """
        transformations = []

        for key in original_args:
            if key in processed_args:
                original_val = original_args[key]
                processed_val = processed_args[key]

                if original_val != processed_val:
                    transformations.append(
                        {
                            "field": key,
                            "original_type": type(original_val).__name__,
                            "processed_type": type(processed_val).__name__,
                            "transformation": self._describe_transformation(
                                original_val, processed_val
                            ),
                        }
                    )

        return transformations

    def _describe_transformation(self, original: Any, processed: Any) -> str:
        """Describe what transformation was applied."""
        if type(original) != type(processed):
            return f"Type conversion: {type(original).__name__} → {type(processed).__name__}"
        elif isinstance(original, str) and isinstance(processed, str):
            if original.strip() != processed:
                return "String normalization (strip whitespace)"
        elif isinstance(original, (int, float)) and isinstance(processed, (int, float)):
            return f"Numeric conversion: {original} → {processed}"
        return "Value normalization"

    def _calculate_response_size(self, response: dict[str, Any]) -> dict[str, Any]:
        """
        Calculate the size and complexity of a tool response.

        Args:
            response: Tool response to analyze

        Returns:
            Size metrics for the response
        """
        import sys

        response_str = str(response)
        return {
            "bytes": sys.getsizeof(response),
            "characters": len(response_str),
            "dict_keys": len(response) if isinstance(response, dict) else 0,
            "nested_depth": self._calculate_dict_depth(response),
            "list_items": (
                sum(len(v) for v in response.values() if isinstance(v, list))
                if isinstance(response, dict)
                else 0
            ),
        }

    def _calculate_dict_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate the maximum nesting depth of a dictionary."""
        if not isinstance(obj, dict):
            return current_depth

        if not obj:
            return current_depth + 1

        return max(
            self._calculate_dict_depth(v, current_depth + 1) for v in obj.values()
        )

    def _get_processing_time(
        self, raw_result: dict[str, Any], final_result: dict[str, Any]
    ) -> float:
        """Estimate time spent processing the response (mock implementation)."""
        # Simple heuristic based on response complexity
        raw_size = len(str(raw_result))
        final_size = len(str(final_result))
        complexity_factor = final_size / max(raw_size, 1)
        return complexity_factor * 0.1  # Mock processing time in ms

    def _estimate_memory_impact(self, response: dict[str, Any]) -> str:
        """Estimate the memory impact of storing this response."""
        size = self._calculate_response_size(response)
        bytes_size = size["bytes"]

        if bytes_size < 1024:
            return "minimal"
        elif bytes_size < 10240:
            return "low"
        elif bytes_size < 102400:
            return "moderate"
        else:
            return "high"

    def _classify_response_type(self, response: dict[str, Any]) -> str:
        """Classify the type of response received."""
        if not isinstance(response, dict):
            return "invalid"

        if not response.get("success", True):
            return "error"

        if "memories" in response or "results" in response:
            return "search_results"
        elif "created" in response or "updated" in response:
            return "modification"
        elif "data" in response or "canvas" in response or "location" in response:
            return "data_retrieval"
        else:
            return "operation_result"

    def _response_contains_story_content(self, response: dict[str, Any]) -> bool:
        """Check if response contains actual story content."""
        content_indicators = ["nodes", "content", "story", "narrative", "text"]
        return any(
            indicator in str(response).lower() for indicator in content_indicators
        )

    def _suggest_retry_strategy(
        self, tool_name: str, error: Exception, args: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Suggest retry strategy based on the error and tool.

        Args:
            tool_name: Name of the failed tool
            error: The exception that occurred
            args: Arguments that were used

        Returns:
            Retry strategy suggestions
        """
        error_type = type(error).__name__
        error_message = str(error).lower()

        suggestion = {
            "should_retry": False,
            "retry_delay_ms": 0,
            "modified_args": None,
            "alternative_tool": None,
            "reasoning": "",
        }

        # Network/connection errors
        if "connection" in error_message or "timeout" in error_message:
            suggestion.update(
                {
                    "should_retry": True,
                    "retry_delay_ms": 1000,
                    "reasoning": "Network error - retry with delay",
                }
            )

        # Argument validation errors
        elif "validation" in error_message or "required" in error_message:
            suggestion.update(
                {
                    "should_retry": True,
                    "retry_delay_ms": 0,
                    "reasoning": "Argument validation error - fix args and retry",
                }
            )

            # Suggest argument fixes based on tool
            if tool_name == "memory_put" and "kind" in error_message:
                suggestion["modified_args"] = {
                    **args,
                    "kind": "episodic",
                }  # Default kind

        # Resource not found errors
        elif "not found" in error_message or "does not exist" in error_message:
            suggestion.update(
                {
                    "should_retry": False,
                    "reasoning": "Resource not found - need different approach",
                }
            )

            # Suggest alternative tools
            if tool_name == "story_read_canvas":
                suggestion["alternative_tool"] = "story_find_canvas"

        return suggestion

    def _generate_completion_summary(self, state: ReActState) -> str:
        """Generate summary when ReAct loop completes."""
        if state.user_goal_achieved:
            return f"✅ Successfully completed your request. Took {state.step_count} steps."
        elif state.error_message:
            return f"❌ Encountered an error: {state.error_message}"
        else:
            return (
                f"🔄 Completed {state.step_count} steps. {state.reason_for_completion}"
            )

    def _is_canvas_write_operation(self, step_plan: StepPlan) -> bool:
        """
        Check if the step plan represents a canvas write operation.

        Phase 1: Only create_node and delete_canvas are write operations touching canvases.
        """
        if not step_plan:
            return False

        write_tools = ["create_node", "delete_canvas"]
        return step_plan.tool in write_tools

    def _validate_trigger_consistency(
        self, step_plan: StepPlan, tool_result: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Validate trigger consistency after canvas write operations.

        Phase 1: Read-only validation of location_id, weekdays, and time ranges.
        Does not modify triggers, only reports inconsistencies.

        Args:
            step_plan: The executed step plan
            tool_result: Result from tool execution

        Returns:
            Dictionary with warnings and errors from trigger validation
        """
        validation_result = {"warnings": [], "errors": []}

        try:
            # Import here to avoid circular imports
            from apps.stories.models import CanvasTrigger, StoryCanvas, TriggerSchedule
            from apps.world.models import Location

            # Get canvas_id from step plan args
            canvas_id = step_plan.args.get("canvas_id")
            if not canvas_id:
                return validation_result

            # Check if canvas exists and has a trigger
            try:
                canvas = StoryCanvas.objects.get(
                    id=canvas_id, project_id=self.project_id
                )
                trigger = CanvasTrigger.objects.filter(canvas=canvas).first()

                if not trigger:
                    validation_result["warnings"].append(
                        f"Canvas '{canvas.name}' has no trigger defined"
                    )
                    return validation_result

                # Validate location_id exists
                if trigger.location_id:
                    try:
                        Location.objects.get(id=trigger.location_id)
                    except Location.DoesNotExist:
                        validation_result["errors"].append(
                            f"Trigger location_id {trigger.location_id} does not exist"
                        )
                else:
                    validation_result["warnings"].append(
                        "Canvas trigger has no location_id defined"
                    )

                # Validate trigger schedules
                schedules = TriggerSchedule.objects.filter(trigger=trigger)
                for schedule in schedules:
                    # Validate weekday ∈ {0..6}
                    if not (0 <= schedule.weekday <= 6):
                        validation_result["errors"].append(
                            f"Invalid weekday {schedule.weekday} in trigger schedule (must be 0-6)"
                        )

                    # Validate start < end
                    if schedule.start_time and schedule.end_time:
                        if schedule.start_time >= schedule.end_time:
                            validation_result["errors"].append(
                                f"Invalid time range: start_time {schedule.start_time} >= end_time {schedule.end_time}"
                            )
                    else:
                        validation_result["warnings"].append(
                            "Trigger schedule has incomplete time range"
                        )

                if not schedules.exists():
                    validation_result["warnings"].append(
                        "Canvas trigger has no schedules defined"
                    )

                logger.debug(
                    f"Trigger validation for canvas {canvas_id}: {len(validation_result['errors'])} errors, {len(validation_result['warnings'])} warnings"
                )

            except StoryCanvas.DoesNotExist:
                validation_result["errors"].append(
                    f"Canvas {canvas_id} not found during trigger validation"
                )

        except Exception as e:
            validation_result["errors"].append(f"Trigger validation failed: {str(e)}")
            logger.error(f"Trigger validation error: {e}")

        return validation_result

    def _generate_dry_run_preview(self, step_plan: StepPlan, state: ReActState) -> str:
        """
        Section 5.5: Generate dry-run preview for workflow preview path.

        For delete_canvas and overwrite scenarios, shows impacted items.
        """
        if not step_plan:
            return "**Preview**: No operation planned"

        tool_name = step_plan.tool
        args = step_plan.args

        if tool_name == "delete_canvas":
            canvas_id = args.get("canvas_id")
            if canvas_id:
                # Generate delete impact preview using helper
                try:
                    from ..services.phase1_tool_adapters import (
                        delete_canvas_impact_preview,
                    )

                    impact_info = delete_canvas_impact_preview(
                        canvas_id, self.project_id
                    )

                    preview_parts = [
                        "**⚠️ DELETE CANVAS PREVIEW**",
                        "",
                        f"**Canvas**: {impact_info.get('canvas_name', 'Unknown')}",
                        "",
                        "**Items to be deleted**:",
                    ]

                    items = impact_info.get("items_to_delete", {})
                    if items.get("canvas"):
                        preview_parts.append(f"• Canvas: {items['canvas']}")
                    if items.get("nodes"):
                        preview_parts.append(f"• Story nodes: {items['nodes']}")
                    if items.get("trigger"):
                        preview_parts.append(f"• Trigger: {items['trigger']}")
                    if items.get("schedules"):
                        preview_parts.append(f"• Schedules: {items['schedules']}")

                    preview_parts.extend(
                        [
                            "",
                            "**This action cannot be undone.**",
                            "",
                            "Proceed with deletion?",
                        ]
                    )

                    return "\n".join(preview_parts)

                except Exception as e:
                    logger.error(f"Failed to generate delete preview: {e}")
                    return f"**DELETE PREVIEW**: Canvas {canvas_id} and all associated content will be permanently deleted. Proceed?"

        elif tool_name == "create_node":
            # Check if this is an overwrite scenario from step result
            if state.step_result and state.step_result.get("requires_overwrite"):
                dry_run_info = state.step_result.get("dry_run_info", {})

                preview_parts = [
                    "**📝 NODE OVERWRITE PREVIEW**",
                    "",
                    f"**Canvas**: {dry_run_info.get('canvas_name', 'Unknown')}",
                    "",
                    f"**Current node**: '{dry_run_info.get('existing_title', 'Untitled')}' ({dry_run_info.get('existing_length', 0)} chars)",
                    f"**New node**: '{dry_run_info.get('new_title', 'Untitled')}' ({dry_run_info.get('new_length', 0)} chars)",
                    "",
                ]

                if dry_run_info.get("title_changed"):
                    preview_parts.append("• Title will change")
                else:
                    preview_parts.append("• Title unchanged")

                content_diff = dry_run_info.get("content_length_diff", 0)
                if content_diff > 0:
                    preview_parts.append(
                        f"• Content will increase by {content_diff} characters"
                    )
                elif content_diff < 0:
                    preview_parts.append(
                        f"• Content will decrease by {abs(content_diff)} characters"
                    )
                else:
                    preview_parts.append("• Content length unchanged")

                preview_parts.extend(["", "Proceed with overwrite?"])

                return "\n".join(preview_parts)

        # Default preview
        return f"**Preview**: {step_plan.expected_effect}\n\nProceed with this action?"

    def _is_final_by_nature(
        self, step_plan: StepPlan, step_result: dict[str, Any]
    ) -> bool:
        """
        Section 5.4: Check if result is final by nature (delete/overwrite completed).

        Returns True for operations that represent completion regardless of confidence.
        """
        if not step_plan or not step_result:
            return False

        # Successful delete operations are final
        if step_plan.tool == "delete_canvas" and step_result.get("success"):
            return True

        # Successful create_node with overwrite is final
        if (
            step_plan.tool == "create_node"
            and step_result.get("success")
            and step_plan.args.get("overwrite_confirmed")
        ):
            return True

        # Successful create_node on empty canvas is final
        if (
            step_plan.tool == "create_node"
            and step_result.get("success")
            and step_result.get("node")
        ):
            return True

        return False
