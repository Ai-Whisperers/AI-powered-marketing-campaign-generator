import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Add current directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock google.generativeai before importing ai_client
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["google.api_core"] = MagicMock()
sys.modules["google.api_core.exceptions"] = MagicMock()

from api.graphs.campaign_graph import CampaignGraphRunner


async def test_campaign_graph_execution():
    """Test the full execution of the campaign graph."""
    print("Starting test_campaign_graph_execution...")

    # Mock dependencies
    with patch("api.graphs.campaign_graph.get_ai_manager") as mock_get_ai, \
         patch("api.graphs.campaign_graph.get_research_service") as mock_get_research, \
         patch("api.graphs.campaign_graph.get_campaign_memory_lazy") as mock_get_memory:

        # Setup Memory Mock
        mock_memory = AsyncMock()
        mock_get_memory.return_value = mock_memory

        # Setup AI Mock
        mock_ai = AsyncMock()
        mock_get_ai.return_value = mock_ai

        # Mock synthesis response
        mock_ai.generate.return_value = "Insight 1: People love free stuff.\nInsight 2: Mobile first."

        # Mock ideation response
        mock_ai.generate_json.side_effect = [
            # Ideation response
            {
                "ideas": [
                    {"title": "Idea 1", "description": "Desc 1", "rationale": "Rat 1"},
                    {"title": "Idea 2", "description": "Desc 2", "rationale": "Rat 2"}
                ]
            },
            # Critique response 1
            {
                "critique": "Good idea",
                "scores": {"relevance": 8, "creativity": 9}
            },
            # Critique response 2
            {
                "critique": "Okay idea",
                "scores": {"relevance": 6, "creativity": 7}
            }
        ]

        # Setup Research Mock
        mock_research = AsyncMock()
        mock_get_research.return_value = mock_research
        mock_research.get_all_research.return_value = "Mock research content"

        # Run graph
        print("Initializing runner...")
        runner = CampaignGraphRunner()
        print("Running campaign...")
        result = await runner.run_campaign("test-project", num_ideas=2)

        # Assertions
        print("Verifying results...")
        assert result["project_id"] == "test-project"
        assert len(result["concepts"]) == 2
        assert len(result["scored_ideas"]) == 2
        assert result["scored_ideas"][0]["scores"]["relevance"] == 8
        assert result["research_summary"] == "Insight 1: People love free stuff.\nInsight 2: Mobile first."

        # Verify calls
        mock_research.get_all_research.assert_called_once_with("test-project")
        assert mock_ai.generate.called
        assert mock_ai.generate_json.call_count == 3  # 1 ideation + 2 critiques

        print("Test passed successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(test_campaign_graph_execution())
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
