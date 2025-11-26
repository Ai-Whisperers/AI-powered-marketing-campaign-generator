import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()


async def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables.")
        return

    print(f"🔑 Testing OpenAI API Key: {api_key[:5]}...{api_key[-4:]}")

    client = AsyncOpenAI(api_key=api_key)

    # Test 1: Cheap model (gpt-3.5-turbo)
    print("\n🧪 Test 1: gpt-3.5-turbo (Cheap)")
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10,
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    # Test 2: Expensive model (gpt-4-turbo) - This is what config uses
    print("\n🧪 Test 2: gpt-4-turbo (Expensive)")
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10,
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_openai())
