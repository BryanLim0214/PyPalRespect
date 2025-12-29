"""
Tests for system prompts.
"""
import pytest


class TestSystemPrompts:
    """Tests for system_prompts.py"""
    
    def test_tutor_system_prompt_exists(self):
        """Test that get_tutor_system_prompt is defined."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        prompt = get_tutor_system_prompt()
        assert prompt is not None
        assert len(prompt) > 100
    
    def test_tutor_prompt_contains_adhd_guidelines(self):
        """Test that tutor prompt includes ADHD-specific guidance."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        
        prompt_lower = get_tutor_system_prompt().lower()
        
        # Should mention key ADHD accommodations
        assert "short" in prompt_lower
        assert "step" in prompt_lower
        assert "encouraging" in prompt_lower
        assert "one thing at a time" in prompt_lower.replace("-", " ")
    
    def test_tutor_prompt_contains_safety_rules(self):
        """Test that tutor prompt includes safety rules."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        
        prompt_lower = get_tutor_system_prompt().lower()
        
        assert "safety" in prompt_lower or "appropriate" in prompt_lower
        assert "never" in prompt_lower
    
    def test_tutor_prompt_mentions_age_group(self):
        """Test that tutor prompt references target age group."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        
        assert "middle school" in get_tutor_system_prompt().lower()
        assert "11" in get_tutor_system_prompt() or "14" in get_tutor_system_prompt()
    
    def test_task_decomposition_prompt_generation(self):
        """Test task decomposition prompt generation."""
        from app.prompts.system_prompts import get_task_decomposition_prompt
        
        prompt = get_task_decomposition_prompt(
            task="Create a number guessing game",
            student_interests=["games", "space"]
        )
        
        assert "Create a number guessing game" in prompt
        assert "games" in prompt
        assert "space" in prompt
        assert "JSON" in prompt
        assert "steps" in prompt
    
    def test_task_decomposition_prompt_default_interests(self):
        """Test task decomposition with default interests."""
        from app.prompts.system_prompts import get_task_decomposition_prompt
        
        prompt = get_task_decomposition_prompt(
            task="Print hello world",
            student_interests=[]
        )
        
        # Should use default interests
        assert "games" in prompt.lower() or "technology" in prompt.lower()
    
    def test_hint_prompt_levels(self):
        """Test hint prompt generation for different levels."""
        from app.prompts.system_prompts import get_hint_prompt
        
        code = "print('hello')"
        
        # Level 1 - Gentle
        prompt1 = get_hint_prompt(code, hint_level=1)
        assert "GENTLE" in prompt1
        assert "question" in prompt1.lower()
        
        # Level 2 - Direction
        prompt2 = get_hint_prompt(code, hint_level=2)
        assert "GENERAL AREA" in prompt2
        
        # Level 3 - Specific
        prompt3 = get_hint_prompt(code, hint_level=3)
        assert "SPECIFICALLY" in prompt3
        
        # Level 4 - Show solution
        prompt4 = get_hint_prompt(code, hint_level=4)
        assert "CORRECT CODE" in prompt4
    
    def test_hint_prompt_includes_error(self):
        """Test hint prompt includes error message when provided."""
        from app.prompts.system_prompts import get_hint_prompt
        
        prompt = get_hint_prompt(
            current_code="prin('hello')",
            error_message="NameError: name 'prin' is not defined",
            hint_level=1
        )
        
        assert "NameError" in prompt
        assert "prin" in prompt
    
    def test_hint_prompt_age_appropriate(self):
        """Test hint prompt reminds about age appropriateness."""
        from app.prompts.system_prompts import get_hint_prompt
        
        prompt = get_hint_prompt("x = 5", hint_level=1)
        
        assert "11-14" in prompt or "middle school" in prompt.lower()
        assert "SHORT" in prompt
    
    def test_celebration_prompt_generation(self):
        """Test celebration prompt generation."""
        from app.prompts.system_prompts import get_celebration_prompt
        
        prompt = get_celebration_prompt(
            achievement_type="step_complete",
            points=10
        )
        
        assert "step_complete" in prompt
        assert "10" in prompt
        assert "emoji" in prompt.lower()
        assert "SHORT" in prompt
