import asyncio
import os
import sys
from dotenv import load_dotenv
import aiohttp

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)

# Add code directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from api.config import get_settings
from api.services.ai_client import OpenAIClient, AnthropicClient, GeminiClient

async def verify_keys():
    print("Verifying API Keys and Connectivity...")
    settings = get_settings()
    
    # 1. Verify OpenAI
    print("\n--- OpenAI Verification ---")
    if settings.openai_api_key:
        print("OpenAI API Key found.")
        try:
            client = OpenAIClient(api_key=settings.openai_api_key, model="gpt-4o")
            response = await client.generate("Hello, are you working?")
            print(f"OpenAI Response: Success (Length: {len(response)})")
        except Exception as e:
            print(f"OpenAI Failed: {e}")
    else:
        print("OpenAI API Key NOT found.")

    # 2. Verify Anthropic
    print("\n--- Anthropic Verification ---")
    if settings.anthropic_api_key:
        print("Anthropic API Key found.")
        try:
            # Use haiku which is cheaper and widely available
            client = AnthropicClient(api_key=settings.anthropic_api_key, model="claude-3-haiku-20240307")
            response = await client.generate("Hello")
            print(f"Anthropic Response: Success (Length: {len(response)})")
        except Exception as e:
            print(f"Anthropic Failed: {e}")
    else:
        print("Anthropic API Key NOT found.")

    # 3. Verify Gemini
    print("\n--- Gemini Verification ---")
    if settings.gemini_api_key:
        print("Gemini API Key found.")
        try:
            # Use standard gemini-pro
            client = GeminiClient(api_key=settings.gemini_api_key, model="gemini-pro")
            response = await client.generate("Hello")
            print(f"Gemini Response: Success (Length: {len(response)})")
        except Exception as e:
            print(f"Gemini Failed: {e}")
    else:
        print("Gemini API Key NOT found.")

    # 4. Verify Tavily (Direct API Check)
    print("\n--- Tavily Verification ---")
    # Tavily key is not in Settings, so we check env var
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if tavily_key:
        print("Tavily API Key found.")
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "api_key": tavily_key,
                    "query": "What is the capital of France?",
                    "search_depth": "basic",
                    "max_results": 1
                }
                async with session.post("https://api.tavily.com/search", json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"Tavily Response: Success (Results: {len(data.get('results', []))})")
                    else:
                        print(f"Tavily Failed: Status {resp.status} - {await resp.text()}")
        except Exception as e:
            print(f"Tavily Failed: {e}")
    else:
        print("Tavily API Key NOT found.")

    # 5. Verify Langfuse
    print("\n--- Langfuse Verification ---")
    if settings.langfuse_public_key and settings.langfuse_secret_key:
        print("Langfuse Keys found.")
        try:
            from langfuse import Langfuse
            langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host
            )
            if langfuse.auth_check():
                print("Langfuse Auth: Success")
            else:
                print("Langfuse Auth: Failed")
        except ImportError:
            print("Langfuse package not installed.")
        except Exception as e:
            print(f"Langfuse Verification Failed: {e}")
    else:
        print("Langfuse Keys NOT found.")

if __name__ == "__main__":
    asyncio.run(verify_keys())
