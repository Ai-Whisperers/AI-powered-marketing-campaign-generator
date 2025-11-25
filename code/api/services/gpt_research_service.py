"""
GPT Researcher Service

Adapter for the gpt-researcher library to conduct deep autonomous research.
"""

import os
from typing import Any

from ..logging_config import get_logger
from ..config import get_settings

logger = get_logger("gpt_research_service")


class GPTResearchService:
    """
    Service for conducting deep research using GPT Researcher.
    """

    def __init__(self):
        self.settings = get_settings()
        # Ensure API keys are set in environment for GPT Researcher
        # Use setdefault to avoid overwriting existing environment variables
        if self.settings.openai_api_key:
            if "OPENAI_API_KEY" not in os.environ:
                os.environ["OPENAI_API_KEY"] = self.settings.openai_api_key
                logger.debug("Set OPENAI_API_KEY from settings")

        if self.settings.tavily_api_key:
            if "TAVILY_API_KEY" not in os.environ:
                os.environ["TAVILY_API_KEY"] = self.settings.tavily_api_key
                logger.debug("Set TAVILY_API_KEY from settings")

    async def conduct_research(self, query: str, report_type: str = "research_report") -> str:
        """
        Conduct deep research on a query.

        Args:
            query: Research query or topic
            report_type: Type of report (research_report, resource_report, outline_report)

        Returns:
            Research report content
        """
        logger.info(f"Starting GPT Researcher for query: {query}")

        try:
            from gpt_researcher import GPTResearcher

            researcher = GPTResearcher(query=query, report_type=report_type)

            # Conduct research
            await researcher.conduct_research()

            # Write report
            report = await researcher.write_report()

            return report

        except Exception as e:
            logger.error(f"GPT Researcher failed: {e}")
            return f"Research failed: {str(e)}"


# Singleton
_gpt_research_service: GPTResearchService | None = None


def get_gpt_research_service() -> GPTResearchService:
    global _gpt_research_service
    if _gpt_research_service is None:
        _gpt_research_service = GPTResearchService()
    return _gpt_research_service
