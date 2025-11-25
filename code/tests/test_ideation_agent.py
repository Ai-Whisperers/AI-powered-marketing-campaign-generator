import asyncio
import os
from api.agents.ideation_agent import create_ideation_graph
from api.models import Idea

async def test_ideation_agent():
    print("Initializing Ideation Agent Graph...")
    try:
        graph = create_ideation_graph()
        print("Graph compiled successfully.")
    except Exception as e:
        print(f"Failed to compile graph: {e}")
        return

    # Mock state
    initial_state = {
        "project_id": "test-project",
        "brief_text": "Challenge: Sell more coffee to Gen Z. Target: Gen Z.",
        "research_summary": "Gen Z likes authentic brands.",
        "ideas": [],
        "critique": "",
        "iteration_count": 0,
        "max_iterations": 1
    }

    print("\nRunning Agent (Dry Run)...")
    # We expect this to fail due to API credits, but we want to see it start.
    try:
        # We can't easily mock the internal AI calls without extensive mocking.
        # So we'll just run it and catch the expected API error.
        await graph.ainvoke(initial_state)
        print("Agent finished successfully (Unexpected without credits).")
    except Exception as e:
        print(f"\nAgent execution stopped as expected (or failed): {e}")
        if "credit balance is too low" in str(e) or "400" in str(e):
             print("SUCCESS: Agent attempted to call API.")
        else:
             print("WARNING: Stopped due to other error.")

if __name__ == "__main__":
    asyncio.run(test_ideation_agent())
