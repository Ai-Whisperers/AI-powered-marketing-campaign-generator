import pytest
import os
from unittest.mock import MagicMock, patch
from typing import Generator


@pytest.fixture(scope="session", autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(
        os.environ,
        {
            "ENVIRONMENT": "test",
            "API_KEY": "test-api-key",
            "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
            "REDIS_URL": "redis://localhost:6379/0",
            "OPENAI_API_KEY": "sk-test-key",
            "ANTHROPIC_API_KEY": "sk-ant-test-key",
            "GEMINI_API_KEY": "test-gemini-key",
            "TAVILY_API_KEY": "test-tavily-key",
        },
    ):
        yield


@pytest.fixture
def mock_settings():
    """Mock settings object."""
    with patch("api.config.get_settings") as mock:
        settings = MagicMock()
        settings.environment = "test"
        settings.debug = True
        settings.api_key = "test-api-key"
        settings.openai_api_key = "sk-test-key"
        settings.anthropic_api_key = "sk-ant-test-key"
        settings.gemini_api_key = "test-gemini-key"
        settings.tavily_api_key = "test-tavily-key"
        mock.return_value = settings
        yield settings


@pytest.fixture
def mock_ai_client():
    """Mock AI client manager."""
    with patch("api.services.ai_client.AIClientManager") as mock:
        manager = MagicMock()
        manager.generate.return_value = "Mocked AI response"
        manager.generate_json.return_value = {"key": "value"}
        mock.return_value = manager
        yield manager
