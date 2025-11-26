import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.services.gpt_research_service import GPTResearchService


@pytest.mark.asyncio
async def test_research_service_initialization(mock_settings):
    """Test service initialization."""
    with patch("api.services.gpt_research_service.get_ai_manager") as mock_get_manager:
        service = GPTResearchService()
        assert service.ai_manager is not None
        mock_get_manager.assert_called_once()


@pytest.mark.asyncio
async def test_conduct_research_success(mock_settings):
    """Test successful research execution."""
    with patch("api.services.gpt_research_service.get_ai_manager") as mock_get_manager:
        # Setup mock AI manager
        mock_manager = MagicMock()
        mock_manager.generate_json = AsyncMock(
            return_value={
                "summary": "Test summary",
                "key_points": ["Point 1", "Point 2"],
                "statistics": [{"text": "Stat 1", "source": "Source 1"}],
                "relevance_score": 90,
                "source_type": "web",
            }
        )
        mock_get_manager.return_value = mock_manager

        service = GPTResearchService()

        result = await service.conduct_research(query="Test query", category="market_analysis")

        assert result["summary"] == "Test summary"
        assert len(result["key_points"]) == 2
        assert result["relevance_score"] == 90

        # Verify AI call
        mock_manager.generate_json.assert_called_once()
        call_args = mock_manager.generate_json.call_args
        assert "Test query" in call_args[1]["prompt"]


@pytest.mark.asyncio
async def test_analyze_content_success(mock_settings):
    """Test content analysis."""
    with patch("api.services.gpt_research_service.get_ai_manager") as mock_get_manager:
        mock_manager = MagicMock()
        mock_manager.generate_json = AsyncMock(
            return_value={
                "summary": "Content summary",
                "sentiment": "positive",
                "topics": ["Topic A"],
            }
        )
        mock_get_manager.return_value = mock_manager

        service = GPTResearchService()

        result = await service.analyze_content(
            content="Some content to analyze", analysis_type="sentiment"
        )

        assert result["summary"] == "Content summary"
        assert result["sentiment"] == "positive"


@pytest.mark.asyncio
async def test_error_handling(mock_settings):
    """Test error handling during research."""
    with patch("api.services.gpt_research_service.get_ai_manager") as mock_get_manager:
        mock_manager = MagicMock()
        mock_manager.generate_json = AsyncMock(side_effect=Exception("AI Error"))
        mock_get_manager.return_value = mock_manager

        service = GPTResearchService()

        # Should raise exception or handle gracefully depending on implementation
        # Assuming it propagates for now based on typical service patterns
        with pytest.raises(Exception):
            await service.conduct_research("query", "category")
