from unittest.mock import AsyncMock, patch

import pytest
from api.graphs.campaign_graph import CampaignGraphRunner


@pytest.mark.asyncio
async def test_campaign_graph_execution():
    """Test the full execution of the campaign graph."""

    # Mock dependencies
    with patch("api.graphs.campaign_graph.get_ai_manager") as mock_get_ai, \
         patch("api.graphs.campaign_graph.get_research_service") as mock_get_research:

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
        runner = CampaignGraphRunner()
        result = await runner.run_campaign("test-project", num_ideas=2)

        # Assertions
        assert result["project_id"] == "test-project"
        assert len(result["concepts"]) == 2
        assert len(result["scored_ideas"]) == 2
        assert result["scored_ideas"][0]["scores"]["relevance"] == 8
        assert result["research_summary"] == "Insight 1: People love free stuff.\nInsight 2: Mobile first."

        # Verify calls
        mock_research.get_all_research.assert_called_once_with("test-project")
        assert mock_ai.generate.called
        assert mock_ai.generate_json.call_count == 3  # 1 ideation + 2 critiques
