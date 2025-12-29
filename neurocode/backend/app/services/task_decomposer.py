"""
Task decomposition service for breaking problems into ADHD-friendly steps.
"""
import json
import logging
from typing import List, Optional

from app.services.gemini_service import gemini_service
from app.prompts.system_prompts import get_task_decomposition_prompt
from app.schemas.tutor import Step, TaskDecompositionResponse

logger = logging.getLogger(__name__)


class TaskDecomposerService:
    """
    Service for breaking coding tasks into micro-steps.
    Research basis: Barkley (2021) shows ADHD learners benefit from
    external scaffolding of executive functions like task planning.
    """
    
    async def decompose_task(
        self,
        task: str,
        student_interests: List[str] = None,
    ) -> TaskDecompositionResponse:
        """
        Break a coding task into small, achievable steps.
        
        Args:
            task: Description of the coding task
            student_interests: Student's interests for personalization
            
        Returns:
            TaskDecompositionResponse with steps and estimated time
        """
        interests = student_interests or ["games", "technology"]
        prompt = get_task_decomposition_prompt(task, interests)
        
        try:
            response = await gemini_service.generate_response(
                user_message=prompt,
                system_prompt="You are a task decomposition expert for ADHD learners. Return ONLY valid JSON.",
                temperature=0.5,
                max_tokens=1500,
            )
            
            # Parse JSON response
            json_str = self._extract_json(response)
            data = json.loads(json_str)
            
            steps = [
                Step(
                    number=s["number"],
                    title=s["title"],
                    instruction=s["instruction"],
                    code_hint=s.get("code_hint"),
                    checkpoint=s.get("checkpoint", False)
                )
                for s in data["steps"]
            ]
            
            return TaskDecompositionResponse(
                steps=steps,
                estimated_time_minutes=data.get("estimated_time_minutes", 15),
                celebration_message=data.get("celebration_message", "Great job! You did it! 🎉")
            )
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse task decomposition JSON: {e}")
            return self._get_fallback_decomposition(task)
        except Exception as e:
            logger.error(f"Task decomposition failed: {e}")
            return self._get_fallback_decomposition(task)
    
    def _extract_json(self, response: str) -> str:
        """Extract JSON from response that might have extra text."""
        # Find JSON object in response
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end > start:
            return response[start:end]
        return response
    
    def _get_fallback_decomposition(self, task: str) -> TaskDecompositionResponse:
        """Return a basic fallback decomposition if AI fails."""
        return TaskDecompositionResponse(
            steps=[
                Step(
                    number=1,
                    title="Understand the goal",
                    instruction=f"Let's break this down: {task[:50]}... What's the first small thing we need to do?",
                    checkpoint=False
                ),
                Step(
                    number=2,
                    title="Start coding",
                    instruction="Write a simple first line of code to get started.",
                    checkpoint=True
                ),
                Step(
                    number=3,
                    title="Test it",
                    instruction="Run your code and see what happens!",
                    checkpoint=True
                ),
            ],
            estimated_time_minutes=10,
            celebration_message="You completed the exercise! Great work! 🎉"
        )
    
    def validate_steps(self, steps: List[Step]) -> List[str]:
        """
        Validate that steps are ADHD-friendly.
        Returns list of warnings if any.
        """
        warnings = []
        
        if len(steps) > 7:
            warnings.append("Too many steps (>7) may be overwhelming")
        
        for step in steps:
            if len(step.instruction) > 200:
                warnings.append(f"Step {step.number} instruction is too long")
        
        # Check for checkpoints
        checkpoint_count = sum(1 for s in steps if s.checkpoint)
        if checkpoint_count == 0 and len(steps) > 2:
            warnings.append("No checkpoints - add points where students can run code")
        
        return warnings


# Singleton instance
task_decomposer = TaskDecomposerService()
