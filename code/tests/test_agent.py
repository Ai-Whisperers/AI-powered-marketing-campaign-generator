"""
Test script for Research Agent.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

import sys
from pathlib import Path
# Add 'code' directory to sys.path to import 'api' directly
sys.path.append(str(Path(__file__).parent))

from api.agents.research_agent import create_research_graph

async def test_agent():
    print("Initializing Research Agent...")
    agent = create_research_graph()
    
    initial_state = {
        "project_id": "test-project",
        "topic": "Nestlé Paraguay Market Trends",
        "subtopics": ["Coffee consumption", "Competitors"],
        "messages": [],
        "findings": [],
        "pending_queries": [],
        "iterations": 0,
        "is_complete": False
    }
    
    print(f"Starting research on: {initial_state['topic']}")
    
    async for event in agent.astream(initial_state):
        for key, value in event.items():
            print(f"\nNode: {key}")
            if "pending_queries" in value:
                print(f"Queries: {value['pending_queries']}")
            if "findings" in value:
                print(f"Findings: {len(value['findings'])} new items")
            if "is_complete" in value:
                print(f"Complete: {value['is_complete']}")

if __name__ == "__main__":
    asyncio.run(test_agent())
