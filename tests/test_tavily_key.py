import os

from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()


def test_tavily():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("❌ TAVILY_API_KEY not found in environment variables.")
        return

    print(f"🔑 Testing Tavily API Key: {api_key[:5]}...{api_key[-4:]}")

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search("Nestlé Paraguay market trends", search_depth="basic")

        if response and "results" in response and len(response["results"]) > 0:
            print(f"✅ Success! Found {len(response['results'])} results.")
            print(f"   First result: {response['results'][0]['title']}")
        else:
            print("⚠️ API call worked but returned no results.")

    except Exception as e:
        print(f"❌ Failed: {e}")


if __name__ == "__main__":
    test_tavily()
