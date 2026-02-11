"""
Shared LLM Service for all CAISOGAMES agents.
Zero-dependency HTTP client using urllib for Gemini API.

Each agent subclasses this and overrides _generate_mock() for agent-specific
mock responses. The API logic is shared and never duplicated.
"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

from .constants import GEMINI_TEXT_MODEL, GEMINI_API_BASE


class LLMService:
    """
    Zero-dependency LLM client using Gemini API via urllib.
    Subclass and override _generate_mock() for agent-specific mock responses.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = GEMINI_TEXT_MODEL,
        temperature: float = 0.7,
        max_output_tokens: int = 4000,
    ):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found. Using Mock LLM mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate text response from Gemini API (or mock fallback)."""
        if self.mock_mode:
            return self._generate_mock(prompt)

        url = f"{GEMINI_API_BASE}/{self.model}:generateContent?key={self.api_key}"

        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_output_tokens,
            },
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))

                candidates = result.get("candidates", [])
                if not candidates:
                    return "Error: No candidates returned from API."

                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if not parts:
                    return "Error: Empty response parts."

                return parts[0].get("text", "")

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            return f"API Error {e.code}: {e.reason}\nDetails: {error_body}"
        except Exception as e:
            return f"Network Error: {str(e)}"

    def _generate_mock(self, prompt: str) -> str:
        """Override in subclass for agent-specific mock responses."""
        return "Mock LLM Response"
