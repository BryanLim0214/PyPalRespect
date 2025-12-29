"""
Tests for task decomposer service.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json


class TestTaskDecomposerService:
    """Tests for TaskDecomposerService."""
    
    @pytest.mark.asyncio
    async def test_decompose_task_returns_response(self):
        """Test that decompose_task returns a proper response."""
        from app.services.task_decomposer import TaskDecomposerService
        
        mock_json_response = json.dumps({
            "steps": [
                {
                    "number": 1,
                    "title": "Step 1",
                    "instruction": "First instruction",
                    "code_hint": "print('hi')",
                    "checkpoint": False
                },
                {
                    "number": 2,
                    "title": "Step 2",
                    "instruction": "Second instruction",
                    "checkpoint": True
                }
            ],
            "estimated_time_minutes": 10,
            "celebration_message": "Great job!"
        })
        
        service = TaskDecomposerService()
        
        with patch('app.services.task_decomposer.gemini_service') as mock_gemini:
            mock_gemini.generate_response = AsyncMock(return_value=mock_json_response)
            
            result = await service.decompose_task("Create a hello world program")
            
            assert len(result.steps) == 2
            assert result.steps[0].number == 1
            assert result.steps[1].checkpoint == True
            assert result.estimated_time_minutes == 10
    
    @pytest.mark.asyncio
    async def test_decompose_task_with_interests(self):
        """Test task decomposition uses student interests."""
        from app.services.task_decomposer import TaskDecomposerService
        
        mock_json = json.dumps({
            "steps": [{"number": 1, "title": "t", "instruction": "i"}],
            "estimated_time_minutes": 5,
            "celebration_message": "Done!"
        })
        
        service = TaskDecomposerService()
        
        with patch('app.services.task_decomposer.gemini_service') as mock_gemini:
            mock_gemini.generate_response = AsyncMock(return_value=mock_json)
            
            await service.decompose_task(
                "Create a game",
                student_interests=["minecraft", "space"]
            )
            
            call_args = mock_gemini.generate_response.call_args
            prompt = call_args.kwargs.get('user_message', call_args.args[0] if call_args.args else '')
            assert "minecraft" in prompt or "space" in prompt
    
    @pytest.mark.asyncio
    async def test_decompose_task_fallback_on_error(self):
        """Test fallback when API fails."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        
        with patch('app.services.task_decomposer.gemini_service') as mock_gemini:
            mock_gemini.generate_response = AsyncMock(side_effect=Exception("API Error"))
            
            result = await service.decompose_task("Create a program")
            
            # Should return fallback
            assert len(result.steps) >= 2
            assert result.estimated_time_minutes > 0
    
    @pytest.mark.asyncio
    async def test_decompose_task_fallback_on_bad_json(self):
        """Test fallback when API returns invalid JSON."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        
        with patch('app.services.task_decomposer.gemini_service') as mock_gemini:
            mock_gemini.generate_response = AsyncMock(return_value="Not valid JSON")
            
            result = await service.decompose_task("Create a program")
            
            # Should return fallback
            assert len(result.steps) >= 2
    
    def test_extract_json_from_response(self):
        """Test JSON extraction from response with extra text."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        
        response = 'Here is the decomposition:\n{"steps": []}'
        extracted = service._extract_json(response)
        
        assert extracted == '{"steps": []}'
    
    def test_extract_json_clean_response(self):
        """Test JSON extraction from clean response."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        
        response = '{"steps": [{"number": 1}]}'
        extracted = service._extract_json(response)
        
        assert extracted == response
    
    def test_validate_steps_warns_too_many(self):
        """Test validation warns on too many steps."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        steps = [
            Step(number=i, title=f"Step {i}", instruction="Do something")
            for i in range(1, 10)  # 9 steps - too many
        ]
        
        warnings = service.validate_steps(steps)
        
        assert any("Too many" in w for w in warnings)
    
    def test_validate_steps_warns_long_instruction(self):
        """Test validation warns on long instructions."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        steps = [
            Step(number=1, title="Long step", instruction="x" * 250)
        ]
        
        warnings = service.validate_steps(steps)
        
        assert any("too long" in w for w in warnings)
    
    def test_validate_steps_warns_no_checkpoints(self):
        """Test validation warns when no checkpoints."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        steps = [
            Step(number=i, title=f"Step {i}", instruction="Do something", checkpoint=False)
            for i in range(1, 5)
        ]
        
        warnings = service.validate_steps(steps)
        
        assert any("checkpoint" in w.lower() for w in warnings)
    
    def test_validate_steps_good_structure(self):
        """Test validation passes on well-structured steps."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        steps = [
            Step(number=1, title="Step 1", instruction="Do first thing", checkpoint=False),
            Step(number=2, title="Step 2", instruction="Do second thing", checkpoint=True),
            Step(number=3, title="Step 3", instruction="Do third thing", checkpoint=True),
        ]
        
        warnings = service.validate_steps(steps)
        
        # May still have some minor warnings, but not critical ones
        assert not any("Too many" in w for w in warnings)


class TestFallbackDecomposition:
    """Tests for fallback decomposition behavior."""
    
    def test_fallback_has_minimum_steps(self):
        """Test fallback decomposition has required structure."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        result = service._get_fallback_decomposition("Some task here")
        
        assert len(result.steps) >= 2
        assert result.estimated_time_minutes > 0
        assert len(result.celebration_message) > 0
    
    def test_fallback_includes_task_context(self):
        """Test fallback includes task in first step."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        result = service._get_fallback_decomposition("Create a calculator")
        
        # First step should reference the task
        assert "Create" in result.steps[0].instruction or "calculator" in result.steps[0].instruction
    
    def test_fallback_has_checkpoints(self):
        """Test fallback includes checkpoints."""
        from app.services.task_decomposer import TaskDecomposerService
        
        service = TaskDecomposerService()
        result = service._get_fallback_decomposition("Any task")
        
        has_checkpoint = any(s.checkpoint for s in result.steps)
        assert has_checkpoint
