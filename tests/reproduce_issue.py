
import os
import sys

# Add code directory to path
sys.path.append(os.path.join(os.getcwd(), "code"))

# Apply patches

print("Attempting to import gpt_researcher...")
try:
    from gpt_researcher import GPTResearcher
    print("Successfully imported GPTResearcher")
except ImportError as e:
    print(f"Failed to import GPTResearcher: {e}")
except Exception as e:
    print(f"An error occurred during import: {e}")

print("\nAttempting to run simple research...")
import asyncio


async def main():
    try:
        researcher = GPTResearcher(query="test query", report_type="research_report")
        print("Successfully initialized GPTResearcher")
        # Don't actually run it to save time/cost, just init is enough to trigger import errors usually
    except Exception as e:
        print(f"Failed to initialize/run: {e}")

if __name__ == "__main__":
    asyncio.run(main())
