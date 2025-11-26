import os
import sys
from unittest.mock import AsyncMock, MagicMock

import pytest

# Add code directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Mock google.generativeai before importing ai_client
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["google.api_core"] = MagicMock()
sys.modules["google.api_core.exceptions"] = MagicMock()

from api.services.ai_client import GeminiClient


@pytest.mark.asyncio
async def test_gemini_client_initialization():
    """Test GeminiClient initialization."""
    client = GeminiClient(api_key="test-key", model="gemini-pro")
    assert client.model_name == "gemini-pro"
    assert client.get_provider_name() == "gemini"

@pytest.mark.asyncio
async def test_gemini_client_generate():
    """Test GeminiClient generation."""
    client = GeminiClient(api_key="test-key")

    # Mock the model's generate_content_async method
    mock_response = MagicMock()
    mock_response.text = "Generated content"
    client.model.generate_content_async = AsyncMock(return_value=mock_response)

    response = await client.generate("Test prompt")

    assert response == "Generated content"
    client.model.generate_content_async.assert_called_once()
