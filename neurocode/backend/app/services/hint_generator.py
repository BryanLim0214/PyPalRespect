"""
Hint generator service with escalating specificity.
"""
import logging
from typing import Optional

from app.services.gemini_service import gemini_service
from app.prompts.system_prompts import get_hint_prompt, get_tutor_system_prompt
from app.schemas.tutor import HintResponse

logger = logging.getLogger(__name__)


class HintGeneratorService:
    """
    Service for generating adaptive hints for students.
    
    Uses a 4-level escalation system:
    1. Gentle nudge (question to prompt thinking)
    2. Direction (point to the problem area)
    3. Specific (tell them what to fix)
    4. Show (give the solution with explanation)
    """
    
    MAX_HINT_LEVEL = 4
    
    async def generate_hint(
        self,
        code: str,
        error_message: Optional[str] = None,
        hint_level: int = 1,
    ) -> HintResponse:
        """
        Generate a hint at the specified level.
        
        Args:
            code: The student's current code
            error_message: Any error message from running the code
            hint_level: 1-4, with 4 being most specific
            
        Returns:
            HintResponse with the hint and level info
        """
        # Clamp hint level
        level = max(1, min(hint_level, self.MAX_HINT_LEVEL))
        
        # Handle empty code
        if not code or not code.strip():
            return HintResponse(
                hint="Try typing some code first! Start with something simple like: print(\"Hello!\")",
                hint_level=level,
                next_level_available=True
            )
        
        prompt = get_hint_prompt(code, error_message, level)
        
        try:
            response = await gemini_service.generate_response(
                user_message=prompt,
                system_prompt=get_tutor_system_prompt(),
                temperature=0.6,
                max_tokens=300,
            )
            
            return HintResponse(
                hint=response.strip(),
                hint_level=level,
                next_level_available=level < self.MAX_HINT_LEVEL
            )
            
        except Exception as e:
            logger.error(f"Hint generation failed: {e}")
            return self._get_fallback_hint(level, error_message)
    
    def _get_fallback_hint(
        self,
        level: int,
        error_message: Optional[str] = None
    ) -> HintResponse:
        """Return a fallback hint if AI fails."""
        fallback_hints = {
            1: "Take a look at your code line by line. Does anything look different from what you expected?",
            2: "Check the beginning of each line - make sure you don't have any typos in your keywords.",
            3: "Look at your parentheses and quotes - make sure they all have matching pairs!",
            4: "Try breaking your code into smaller pieces and testing each part separately."
        }
        
        if error_message:
            if "SyntaxError" in error_message:
                fallback_hints[1] = "There's a small typo somewhere. Check your parentheses and quotes!"
            elif "NameError" in error_message:
                fallback_hints[1] = "Python doesn't recognize a word. Check your spelling and capitalization!"
            elif "IndentationError" in error_message:
                fallback_hints[1] = "Check your spacing at the beginning of lines. Python is picky about indentation!"
        
        return HintResponse(
            hint=fallback_hints.get(level, fallback_hints[1]),
            hint_level=level,
            next_level_available=level < self.MAX_HINT_LEVEL
        )
    
    def should_escalate(
        self,
        consecutive_errors: int,
        time_stuck_seconds: int,
        frustration_expressed: bool
    ) -> bool:
        """
        Determine if hint level should automatically escalate.
        
        Based on research: ADHD learners benefit from proactive support
        to prevent frustration spirals.
        """
        if frustration_expressed:
            return True
        if consecutive_errors >= 3:
            return True
        if time_stuck_seconds > 180:  # 3 minutes
            return True
        return False


# Singleton instance
hint_generator = HintGeneratorService()
