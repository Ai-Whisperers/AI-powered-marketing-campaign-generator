import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Add code directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Mock google.generativeai before importing ai_client
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["google.api_core"] = MagicMock()
sys.modules["google.api_core.exceptions"] = MagicMock()

from api.services.ai_client import GeminiClient

async def test_gemini_client():
    print("Starting test_gemini_client...")
    
    # Test Initialization
    print("Testing initialization...")
    client = GeminiClient(api_key="test-key", model="gemini-pro")
    assert client.model_name == "gemini-pro"
    assert client.get_provider_name() == "gemini"
    
    # Test Generation
    print("Testing generation...")
    
    # Mock the model's generate_content_async method
    mock_response = MagicMock()
    mock_response.text = "Generated content"
    client.model.generate_content_async = AsyncMock(return_value=mock_response)
    
    response = await client.generate("Test prompt")
    
    assert response == "Generated content"
    client.model.generate_content_async.assert_called_once()
    
    print("Gemini Client tests passed successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(test_gemini_client())
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
