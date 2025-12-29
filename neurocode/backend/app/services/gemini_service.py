"""
Gemini API integration using the NEW google-genai SDK.

IMPORTANT: This uses the new SDK (google-genai), NOT the deprecated
google-generativeai package.
"""
from google import genai
from google.genai import types
from typing import AsyncGenerator, Optional, List, Dict
import logging

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service for interacting with Google's Gemini API.
    Uses gemini-2.0-flash for cost-effective educational interactions.
    """
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL
    
    def _build_contents(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> List[types.Content]:
        """Build conversation contents for the API."""
        contents = []
        
        if conversation_history:
            for msg in conversation_history:
                contents.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part(text=msg["content"])]
                    )
                )
        
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
        )
        
        return contents
    
    def _get_safety_settings(self) -> List[types.SafetySetting]:
        """Get child-safe content settings."""
        return [
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_LOW_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_LOW_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_LOW_AND_ABOVE"
            ),
        ]
    
    async def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        conversation_history: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate a response from Gemini.
        
        Args:
            user_message: The student's message
            system_prompt: System instructions for ADHD-aware tutoring
            conversation_history: Previous messages for context
            temperature: Creativity level (0.7 is good for education)
            max_tokens: Maximum response length
            
        Returns:
            The tutor's response text
        """
        contents = self._build_contents(user_message, conversation_history)
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    safety_settings=self._get_safety_settings(),
                ),
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    async def generate_response_stream(
        self,
        user_message: str,
        system_prompt: str,
        conversation_history: Optional[List[Dict]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response from Gemini for real-time display.
        Useful for longer explanations where showing text as it
        generates keeps ADHD learners engaged.
        """
        contents = self._build_contents(user_message, conversation_history)
        
        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                    max_output_tokens=1024,
                ),
            ):
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Gemini streaming error: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Test API connectivity."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents="Say 'Connection successful!' in exactly those words.",
                config=types.GenerateContentConfig(
                    max_output_tokens=50,
                ),
            )
            return "successful" in response.text.lower()
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False


# Singleton instance
gemini_service = GeminiService()
