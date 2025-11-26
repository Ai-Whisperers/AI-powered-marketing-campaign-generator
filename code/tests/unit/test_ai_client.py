import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.services.ai_client import AIClientManager, AIProviderError


@pytest.mark.asyncio
async def test_ai_client_initialization(mock_settings):
    """Test that clients are initialized correctly based on settings."""
    # Ensure keys are present in the mock settings
    mock_settings.anthropic_api_key = "test-ant-key"
    mock_settings.openai_api_key = "test-oai-key"
    mock_settings.gemini_api_key = "test-gem-key"

    # Mock the client classes to avoid actual API init
    with (
        patch("api.services.ai_client.AnthropicClient") as MockAnthropic,
        patch("api.services.ai_client.OpenAIClient") as MockOpenAI,
        patch("api.services.ai_client.GeminiClient") as MockGemini,
    ):

        manager = AIClientManager()

        assert manager.primary_client is not None
        assert manager.fallback_client is not None

        # Verify Anthropic is primary by default (as per current logic)
        MockAnthropic.assert_called()


@pytest.mark.asyncio
async def test_generate_primary_success(mock_settings):
    """Test successful generation with primary client."""
    with patch("api.services.ai_client.AnthropicClient") as MockAnthropic:
        # Setup mock primary client
        mock_primary = AsyncMock()
        mock_primary.generate.return_value = "Primary response"
        MockAnthropic.return_value = mock_primary

        manager = AIClientManager()
        # Force primary client to be our mock
        manager.primary_client = mock_primary

        response = await manager.generate("Test prompt")

        assert response == "Primary response"
        mock_primary.generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_fallback_success(mock_settings):
    """Test fallback to secondary client when primary fails."""
    with (
        patch("api.services.ai_client.AnthropicClient") as MockAnthropic,
        patch("api.services.ai_client.OpenAIClient") as MockOpenAI,
    ):

        # Setup mock primary client to fail
        mock_primary = AsyncMock()
        mock_primary.generate.side_effect = AIProviderError("Primary failed", "anthropic")
        MockAnthropic.return_value = mock_primary

        # Setup mock fallback client to succeed
        mock_fallback = AsyncMock()
        mock_fallback.generate.return_value = "Fallback response"
        MockOpenAI.return_value = mock_fallback

        manager = AIClientManager()
        manager.primary_client = mock_primary
        manager.fallback_client = mock_fallback

        response = await manager.generate("Test prompt")

        assert response == "Fallback response"
        mock_primary.generate.assert_called_once()
        mock_fallback.generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_json_parsing(mock_settings):
    """Test JSON generation and parsing."""
    with patch("api.services.ai_client.AnthropicClient") as MockAnthropic:
        mock_primary = AsyncMock()
        # Return JSON wrapped in markdown code block
        mock_primary.generate.return_value = '```json\n{"key": "value"}\n```'
        MockAnthropic.return_value = mock_primary

        manager = AIClientManager()
        manager.primary_client = mock_primary

        result = await manager.generate_json("Test prompt")

        assert result == {"key": "value"}
        assert isinstance(result, dict)
