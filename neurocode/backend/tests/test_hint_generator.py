"""
Tests for hint generator service.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestHintGeneratorService:
    """Tests for HintGeneratorService."""
    
    def test_max_hint_level(self):
        """Test maximum hint level constant."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        assert service.MAX_HINT_LEVEL == 4
    
    @pytest.mark.asyncio
    async def test_generate_hint_empty_code(self):
        """Test hint generation with empty code."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = await service.generate_hint("")
        
        assert result.hint_level == 1
        assert "Try typing some code" in result.hint
        assert result.next_level_available == True
    
    @pytest.mark.asyncio
    async def test_generate_hint_clamps_level(self):
        """Test that hint level is clamped to valid range."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        
        # Test level too low
        with patch.object(service, '_get_fallback_hint') as mock:
            mock.return_value = MagicMock(hint_level=1)
            await service.generate_hint("x = 5", hint_level=0)
        
        # Test level too high
        with patch.object(service, '_get_fallback_hint') as mock:
            mock.return_value = MagicMock(hint_level=4)
            await service.generate_hint("x = 5", hint_level=10)
    
    def test_fallback_hint_basic(self):
        """Test fallback hint generation."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = service._get_fallback_hint(1)
        
        assert result.hint is not None
        assert result.hint_level == 1
        assert result.next_level_available == True
    
    def test_fallback_hint_syntax_error(self):
        """Test fallback hint for syntax errors."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = service._get_fallback_hint(1, "SyntaxError: invalid syntax")
        
        assert "typo" in result.hint.lower() or "parentheses" in result.hint.lower()
    
    def test_fallback_hint_name_error(self):
        """Test fallback hint for name errors."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = service._get_fallback_hint(1, "NameError: name 'x' is not defined")
        
        assert "spelling" in result.hint.lower() or "recognize" in result.hint.lower()
    
    def test_fallback_hint_indentation_error(self):
        """Test fallback hint for indentation errors."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = service._get_fallback_hint(1, "IndentationError: expected indent")
        
        assert "spacing" in result.hint.lower() or "indentation" in result.hint.lower()
    
    def test_fallback_hint_level_4_shows_solution(self):
        """Test that level 4 fallback still available."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = service._get_fallback_hint(4)
        
        assert result.hint_level == 4
        assert result.next_level_available == False
    
    def test_should_escalate_frustration(self):
        """Test escalation on frustration."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        
        result = service.should_escalate(
            consecutive_errors=1,
            time_stuck_seconds=60,
            frustration_expressed=True
        )
        
        assert result == True
    
    def test_should_escalate_many_errors(self):
        """Test escalation after many consecutive errors."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        
        result = service.should_escalate(
            consecutive_errors=3,
            time_stuck_seconds=60,
            frustration_expressed=False
        )
        
        assert result == True
    
    def test_should_escalate_time_stuck(self):
        """Test escalation after being stuck for too long."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        
        result = service.should_escalate(
            consecutive_errors=1,
            time_stuck_seconds=200,  # More than 3 minutes
            frustration_expressed=False
        )
        
        assert result == True
    
    def test_should_not_escalate_normal(self):
        """Test no escalation under normal conditions."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        
        result = service.should_escalate(
            consecutive_errors=1,
            time_stuck_seconds=60,
            frustration_expressed=False
        )
        
        assert result == False
    
    @pytest.mark.asyncio
    async def test_hint_uses_gemini_service(self):
        """Test that hint generator uses Gemini service."""
        from app.services.hint_generator import hint_generator
        
        with patch('app.services.hint_generator.gemini_service') as mock_gemini:
            mock_gemini.generate_response = AsyncMock(return_value="Check line 2!")
            
            result = await hint_generator.generate_hint(
                code='print("hello"',
                error_message="SyntaxError",
                hint_level=2
            )
            
            mock_gemini.generate_response.assert_called_once()
            assert result.hint == "Check line 2!"


class TestHintEscalation:
    """Tests for hint level escalation behavior."""
    
    def test_all_hint_levels_have_fallbacks(self):
        """Test that all 4 levels have fallback messages."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        
        for level in range(1, 5):
            result = service._get_fallback_hint(level)
            assert result.hint is not None
            assert len(result.hint) > 10
    
    def test_hint_level_4_not_escalatable(self):
        """Test that level 4 hints indicate no more levels."""
        from app.services.hint_generator import HintGeneratorService
        
        service = HintGeneratorService()
        result = service._get_fallback_hint(4)
        
        assert result.next_level_available == False
