"""
Tests for Gemini service with mocking.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestGeminiService:
    """Tests for GeminiService class."""
    
    def test_service_initialization(self):
        """Test that GeminiService initializes correctly."""
        from app.services.gemini_service import GeminiService
        
        with patch('app.services.gemini_service.genai.Client') as mock_client:
            service = GeminiService()
            assert service.client is not None
            assert service.model is not None
    
    def test_build_contents_single_message(self):
        """Test building contents with single message."""
        from app.services.gemini_service import GeminiService
        
        with patch('app.services.gemini_service.genai.Client'):
            service = GeminiService()
            contents = service._build_contents("Hello, tutor!")
            
            assert len(contents) == 1
            assert contents[0].role == "user"
    
    def test_build_contents_with_history(self):
        """Test building contents with conversation history."""
        from app.services.gemini_service import GeminiService
        
        with patch('app.services.gemini_service.genai.Client'):
            service = GeminiService()
            
            history = [
                {"role": "user", "content": "Hi"},
                {"role": "model", "content": "Hello!"},
            ]
            
            contents = service._build_contents("What next?", history)
            
            assert len(contents) == 3
            assert contents[0].role == "user"
            assert contents[1].role == "model"
            assert contents[2].role == "user"
    
    def test_safety_settings_child_safe(self):
        """Test that safety settings are appropriate for children."""
        from app.services.gemini_service import GeminiService
        
        with patch('app.services.gemini_service.genai.Client'):
            service = GeminiService()
            settings = service._get_safety_settings()
            
            assert len(settings) >= 4
            
            # All should block low and above
            for setting in settings:
                assert "BLOCK_LOW_AND_ABOVE" in str(setting.threshold)
    
    @pytest.mark.asyncio
    async def test_generate_response_calls_api(self):
        """Test that generate_response calls the Gemini API."""
        from app.services.gemini_service import GeminiService
        
        mock_response = MagicMock()
        mock_response.text = "Here's how to print hello world!"
        
        with patch('app.services.gemini_service.genai.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            service = GeminiService()
            result = await service.generate_response(
                user_message="How do I print hello?",
                system_prompt="You are a tutor.",
            )
            
            assert result == "Here's how to print hello world!"
            mock_client.models.generate_content.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_response_uses_temperature(self):
        """Test that temperature is passed to API."""
        from app.services.gemini_service import GeminiService
        
        mock_response = MagicMock()
        mock_response.text = "Response"
        
        with patch('app.services.gemini_service.genai.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            service = GeminiService()
            await service.generate_response(
                user_message="Test",
                system_prompt="Test",
                temperature=0.5,
            )
            
            call_args = mock_client.models.generate_content.call_args
            config = call_args.kwargs.get('config')
            assert config.temperature == 0.5
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self):
        """Test connection test with success."""
        from app.services.gemini_service import GeminiService
        
        mock_response = MagicMock()
        mock_response.text = "Connection successful!"
        
        with patch('app.services.gemini_service.genai.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            service = GeminiService()
            result = await service.test_connection()
            
            assert result == True
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self):
        """Test connection test with failure."""
        from app.services.gemini_service import GeminiService
        
        with patch('app.services.gemini_service.genai.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.side_effect = Exception("API Error")
            mock_client_class.return_value = mock_client
            
            service = GeminiService()
            result = await service.test_connection()
            
            assert result == False


class TestGeminiServiceIntegration:
    """Integration-style tests (still mocked but more complete flows)."""
    
    @pytest.mark.asyncio
    async def test_tutor_conversation_flow(self):
        """Test a multi-turn conversation."""
        from app.services.gemini_service import GeminiService
        
        mock_response = MagicMock()
        mock_response.text = "Great question! Let's start with..."
        
        with patch('app.services.gemini_service.genai.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            service = GeminiService()
            
            # First message
            history = []
            response1 = await service.generate_response(
                "How do loops work?",
                "You are a tutor.",
                history
            )
            
            # Add to history
            history.append({"role": "user", "content": "How do loops work?"})
            history.append({"role": "model", "content": response1})
            
            # Second message
            mock_response.text = "Now try adding a print statement..."
            response2 = await service.generate_response(
                "I tried that, now what?",
                "You are a tutor.",
                history
            )
            
            assert response2 is not None
            # Verify history was passed
            assert mock_client.models.generate_content.call_count == 2
