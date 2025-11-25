# MAGA v2.0 - Option B Implementation Plan
**LangGraph Centralized Architecture with Internal AI Model**

---

## Executive Summary

This document provides a **complete, step-by-step implementation plan** for upgrading MAGA to v2.0 using **LangGraph as the centralized orchestration platform**.

### Key Decisions
- ✅ **Framework**: LangGraph (single framework for all orchestration)
- ✅ **AI Provider**: Your internal AI model (zero token costs)
- ✅ **Observability**: LangSmith free tier (zero cost)
- ✅ **Storage**: Self-hosted PostgreSQL + Redis (zero additional cost)
- ✅ **Timeline**: 3 weeks (15 working days)
- ✅ **Budget**: $7,200 development + $50/month ongoing

### Expected Outcomes
- **60% faster** idea generation (10min → 4min)
- **Parallel research** execution (3 agents simultaneously)
- **Visual workflow** debugging and monitoring
- **State persistence** with automatic checkpointing
- **Real-time streaming** progress updates
- **Zero vendor lock-in** (100% open source)

---

## Table of Contents

1. [Pre-Implementation Checklist](#1-pre-implementation-checklist)
2. [Week 1: Foundation & Parallel Research](#2-week-1-foundation--parallel-research)
3. [Week 2: Ideation & Evaluation Subgraphs](#3-week-2-ideation--evaluation-subgraphs)
4. [Week 3: Streaming, Testing & Deployment](#4-week-3-streaming-testing--deployment)
5. [Migration Strategy](#5-migration-strategy)
6. [Testing & Quality Assurance](#6-testing--quality-assurance)
7. [Deployment & Rollout](#7-deployment--rollout)
8. [Monitoring & Maintenance](#8-monitoring--maintenance)
9. [Troubleshooting Guide](#9-troubleshooting-guide)
10. [Appendices](#10-appendices)

---

## 1. Pre-Implementation Checklist

### 1.1 Prerequisites

**Before starting, ensure you have**:

- [ ] Python 3.11+ installed
- [ ] PostgreSQL 15+ running (for checkpointing)
- [ ] Redis 7+ running (for task queue)
- [ ] Git repository with current MAGA code
- [ ] Access to your internal AI model API
- [ ] Development environment set up
- [ ] 1 developer dedicated for 3 weeks
- [ ] Staging environment for testing

### 1.2 Environment Setup

**Step 1: Create feature branch**

```bash
cd c:\Users\Alejandro\Documents\Ivan\maga
git checkout -b feature/langgraph-v2
git push -u origin feature/langgraph-v2
```

**Step 2: Install dependencies**

```bash
# Install new packages
pip install langgraph==0.2.50
pip install langgraph-checkpoint-postgres==1.0.0
pip install langchain==0.3.0
pip install langchain-core==0.3.0
pip install langchain-community==0.3.0

# Optional: For visualization
pip install pygraphviz  # Requires graphviz system package
pip install grandalf
```

**Step 3: Update pyproject.toml**

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.115.0"
uvicorn = "^0.30.0"
sqlalchemy = "^2.0.0"
asyncpg = "^0.29.0"
redis = "^5.0.0"
pydantic = "^2.0.0"
pydantic-settings = "^2.0.0"

# LangGraph ecosystem
langgraph = "^0.2.50"
langgraph-checkpoint-postgres = "^1.0.0"
langchain = "^0.3.0"
langchain-core = "^0.3.0"
langchain-community = "^0.3.0"

# Your internal AI model (example - adjust to your needs)
# langchain-custom = { path = "vendors/internal-llm" }

# Existing dependencies
celery = "^5.3.0"
jinja2 = "^3.1.0"
```

**Step 4: Configure environment variables**

```bash
# code/.env

# =============================================================================
# LangGraph Configuration
# =============================================================================
# LangSmith (free tier - no credit card required)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=  # Get from https://smith.langchain.com (free)
LANGCHAIN_PROJECT=maga-campaign-generator
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# =============================================================================
# Internal AI Model Configuration
# =============================================================================
INTERNAL_AI_MODEL_ENDPOINT=http://your-internal-llm.company.com/v1/chat
INTERNAL_AI_MODEL_API_KEY=your-internal-api-key
INTERNAL_AI_MODEL_NAME=your-model-name
INTERNAL_AI_MODEL_TEMPERATURE=0.7
INTERNAL_AI_MODEL_MAX_TOKENS=4096

# =============================================================================
# Feature Flags
# =============================================================================
USE_LANGGRAPH_V2=false  # Set to true when ready to switch
ENABLE_PARALLEL_RESEARCH=false  # Enable after Week 1
ENABLE_STREAMING=false  # Enable after Week 3

# =============================================================================
# Database (for checkpointing)
# =============================================================================
DATABASE_URL=postgresql+asyncpg://maga_user:maga_dev_password@localhost:5432/maga_dev

# =============================================================================
# Existing configuration (keep as-is)
# =============================================================================
API_KEY=test-key
PROJECTS_DIR=campanas-completadas
LOG_LEVEL=INFO
DEBUG=true
```

**Step 5: Get LangSmith API key (free)**

1. Go to https://smith.langchain.com
2. Sign up with email (no credit card required)
3. Go to Settings → API Keys
4. Create new API key
5. Copy to `LANGCHAIN_API_KEY` in `.env`

---

## 2. Week 1: Foundation & Parallel Research

### Day 1-2: Core Graph Setup + Internal LLM Integration

**Goal**: Create the main CampaignGraph structure with your internal AI model

#### Task 1.1: Create Internal LLM Wrapper

**File**: `code/api/llm/internal_llm.py` (NEW)

```python
"""
Internal LLM integration for MAGA.
This adapter allows LangGraph to use your company's internal AI model.
"""

from typing import Any, List, Optional, AsyncIterator
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
import aiohttp
import json
from pydantic import Field

from ..config import get_settings

settings = get_settings()


class InternalChatModel(BaseChatModel):
    """
    LangChain-compatible wrapper for your internal AI model.

    Usage:
        llm = InternalChatModel()
        response = await llm.ainvoke("Generate a campaign idea")
    """

    endpoint: str = Field(default_factory=lambda: settings.internal_ai_model_endpoint)
    api_key: str = Field(default_factory=lambda: settings.internal_ai_model_api_key)
    model_name: str = Field(default_factory=lambda: settings.internal_ai_model_name)
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=4096)

    @property
    def _llm_type(self) -> str:
        """Return identifier for this LLM."""
        return "internal_chat_model"

    def _format_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """Convert LangChain messages to your API format."""
        formatted = []

        for message in messages:
            if isinstance(message, SystemMessage):
                role = "system"
            elif isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                role = "user"  # fallback

            formatted.append({
                "role": role,
                "content": message.content
            })

        return formatted

    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Synchronous call (not recommended for async apps)."""
        import requests

        payload = {
            "model": self.model_name,
            "messages": self._format_messages(messages),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": stop or []
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.endpoint,
            json=payload,
            headers=headers,
            timeout=120
        )

        response.raise_for_status()
        data = response.json()

        # Adjust based on your API response format
        # Common formats:
        # OpenAI-style: data["choices"][0]["message"]["content"]
        # Anthropic-style: data["content"][0]["text"]
        # Custom: data["response"]

        return data["choices"][0]["message"]["content"]

    async def _acall(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Async call (recommended)."""
        payload = {
            "model": self.model_name,
            "messages": self._format_messages(messages),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": stop or []
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                response.raise_for_status()
                data = await response.json()

                # Adjust based on your API response format
                return data["choices"][0]["message"]["content"]

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """Stream response tokens (if your model supports streaming)."""
        payload = {
            "model": self.model_name,
            "messages": self._format_messages(messages),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
            "stop": stop or []
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                response.raise_for_status()

                async for line in response.content:
                    if line:
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: '):
                            data = json.loads(line[6:])
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate chat result."""
        content = self._call(messages, stop, run_manager, **kwargs)
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Async generate chat result."""
        content = await self._acall(messages, stop, run_manager, **kwargs)
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])


# Convenience factory function
def get_internal_llm(temperature: float = 0.7) -> InternalChatModel:
    """Get configured internal LLM instance."""
    return InternalChatModel(temperature=temperature)
```

**File**: `code/api/config.py` (ADD these settings)

```python
# Add to Settings class
class Settings(BaseSettings):
    # ... existing settings ...

    # Internal AI Model
    internal_ai_model_endpoint: str = "http://localhost:8080/v1/chat"
    internal_ai_model_api_key: str = ""
    internal_ai_model_name: str = "default"
    internal_ai_model_temperature: float = 0.7
    internal_ai_model_max_tokens: int = 4096

    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "maga-campaign-generator"

    # Feature flags
    use_langgraph_v2: bool = False
    enable_parallel_research: bool = False
    enable_streaming: bool = False
```

**Test the integration**:

```bash
# Test internal LLM connection
python -c "
import asyncio
from code.api.llm.internal_llm import get_internal_llm

async def test():
    llm = get_internal_llm()
    response = await llm.ainvoke('Say hello in Spanish')
    print(f'Response: {response}')

asyncio.run(test())
"
```

**Expected output**: "Hola" (or similar in Spanish)

---

#### Task 1.2: Create Campaign State Model

**File**: `code/api/graphs/state.py` (NEW)

```python
"""
State definitions for LangGraph workflows.
"""

from typing import TypedDict, Annotated, Optional, Literal
from datetime import datetime
import operator


class CampaignState(TypedDict):
    """
    Global state for campaign generation workflow.

    This state is passed between all nodes in the graph and persisted
    via checkpointing for resumability.
    """

    # ========================================================================
    # Project Information
    # ========================================================================
    project_id: str
    """Unique project identifier"""

    brief: str
    """Campaign brief text"""

    client: str
    """Client name (e.g., 'Ueno Bank')"""

    country: str
    """Target country (e.g., 'Paraguay')"""

    language: str
    """Content language (e.g., 'es')"""

    campaign_type: str
    """Campaign type (e.g., 'digital')"""

    # ========================================================================
    # Research Phase
    # ========================================================================
    market_research: str
    """Market trends and competitive analysis"""

    cultural_insights: str
    """Cultural context and local insights"""

    digital_trends: str
    """Digital behavior and social media trends"""

    research_synthesis: str
    """Combined research summary"""

    research_complete: bool
    """Flag indicating all research is done"""

    research_start_time: Optional[datetime]
    """When research started"""

    research_end_time: Optional[datetime]
    """When research completed"""

    # ========================================================================
    # Ideation Phase
    # ========================================================================
    ideas: Annotated[list[dict], operator.add]
    """
    List of generated ideas (append-only).
    Each idea is a dict with: title, headline, description, rationale, execution
    """

    current_batch: int
    """Current batch number (for progress tracking)"""

    total_batches: int
    """Total number of batches to generate"""

    ideation_start_time: Optional[datetime]
    """When ideation started"""

    # ========================================================================
    # Evaluation Phase
    # ========================================================================
    scored_ideas: list[dict]
    """Ideas with scores attached"""

    top_ideas: list[dict]
    """Top 5 ideas ranked by score"""

    evaluation_complete: bool
    """Flag indicating evaluation is done"""

    # ========================================================================
    # Export Phase
    # ========================================================================
    export_complete: bool
    """Flag indicating export is done"""

    export_paths: list[str]
    """Paths to exported files"""

    # ========================================================================
    # Metadata & Monitoring
    # ========================================================================
    total_cost: float
    """Cumulative cost in USD (if tracking token costs)"""

    total_tokens_input: int
    """Total input tokens used"""

    total_tokens_output: int
    """Total output tokens generated"""

    execution_start_time: datetime
    """When workflow started"""

    execution_end_time: Optional[datetime]
    """When workflow completed"""

    errors: Annotated[list[str], operator.add]
    """List of errors encountered (append-only)"""

    warnings: Annotated[list[str], operator.add]
    """List of warnings (append-only)"""

    current_node: str
    """Name of currently executing node (for debugging)"""

    # ========================================================================
    # Control Flow
    # ========================================================================
    should_continue: bool
    """Flag to control conditional edges"""

    retry_count: int
    """Number of retries for current operation"""

    max_retries: int
    """Maximum retries before failing"""


class IdeationSubgraphState(TypedDict):
    """State for the ideation subgraph (idea generation with critique loop)."""

    brief: str
    """Campaign brief"""

    research_context: str
    """Research synthesis to inform ideation"""

    current_idea: dict
    """The idea currently being refined"""

    critique: dict
    """Critique scores and feedback"""

    iteration: int
    """Current iteration number"""

    max_iterations: int
    """Maximum iterations before accepting idea"""

    should_refine: bool
    """Whether to refine the idea further"""

    final_idea: Optional[dict]
    """Final approved idea"""


class EvaluationSubgraphState(TypedDict):
    """State for the evaluation subgraph."""

    idea: dict
    """Idea to evaluate"""

    brief: str
    """Campaign brief for relevance check"""

    research_context: str
    """Research for grounding check"""

    relevancy_score: float
    """Score 0-1 for relevance to brief"""

    creativity_score: float
    """Score 0-1 for originality"""

    feasibility_score: float
    """Score 0-1 for execution feasibility"""

    impact_score: float
    """Score 0-1 for potential impact"""

    overall_score: float
    """Weighted average of all scores"""

    feedback: str
    """Human-readable feedback"""
```

---

#### Task 1.3: Create Main Campaign Graph

**File**: `code/api/graphs/campaign_graph.py` (NEW)

```python
"""
Main campaign generation graph using LangGraph.

This is the core orchestration logic for MAGA v2.0.
"""

from typing import Literal
from datetime import datetime
import logging

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, SystemMessage

from .state import CampaignState
from ..llm.internal_llm import get_internal_llm
from ..services.file_operations import FileOperationsService
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CampaignGraph:
    """
    Main workflow graph for campaign generation.

    Flow:
        LoadProject → ResearchMarket ┐
                   → ResearchCulture├→ SynthesizeResearch → GenerateIdeas
                   → ResearchDigital ┘                           ↓
                                                                 ↓ (loop)
                                                            EvaluateIdeas → ExportResults → END
    """

    def __init__(self):
        """Initialize the campaign graph."""
        self.llm = get_internal_llm(temperature=0.7)
        self.file_service = FileOperationsService()

        # Set up PostgreSQL checkpointing for state persistence
        self.checkpointer = PostgresSaver.from_conn_string(
            settings.database_url
        )

        # Build the graph
        self.graph = self._build_graph()

        logger.info("CampaignGraph initialized with internal LLM")

    def _build_graph(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(CampaignState)

        # ====================================================================
        # Add Nodes
        # ====================================================================
        workflow.add_node("load_project", self.load_project_node)
        workflow.add_node("research_market", self.research_market_node)
        workflow.add_node("research_culture", self.research_culture_node)
        workflow.add_node("research_digital", self.research_digital_node)
        workflow.add_node("synthesize_research", self.synthesize_research_node)
        workflow.add_node("generate_ideas", self.generate_ideas_node)
        workflow.add_node("evaluate_ideas", self.evaluate_ideas_node)
        workflow.add_node("export_results", self.export_results_node)

        # ====================================================================
        # Define Flow
        # ====================================================================

        # Entry point
        workflow.set_entry_point("load_project")

        # After loading project, branch to 3 parallel research nodes
        workflow.add_edge("load_project", "research_market")
        workflow.add_edge("load_project", "research_culture")
        workflow.add_edge("load_project", "research_digital")

        # All research nodes converge to synthesis
        # (LangGraph waits for all incoming edges before proceeding)
        workflow.add_edge("research_market", "synthesize_research")
        workflow.add_edge("research_culture", "synthesize_research")
        workflow.add_edge("research_digital", "synthesize_research")

        # After synthesis, start ideation
        workflow.add_edge("synthesize_research", "generate_ideas")

        # Conditional: continue generating or move to evaluation
        workflow.add_conditional_edges(
            "generate_ideas",
            self._should_generate_more_ideas,
            {
                "continue": "generate_ideas",  # Loop back
                "done": "evaluate_ideas"        # Move forward
            }
        )

        # Linear flow after evaluation
        workflow.add_edge("evaluate_ideas", "export_results")
        workflow.add_edge("export_results", END)

        # Compile with checkpointing
        return workflow.compile(checkpointer=self.checkpointer)

    # ========================================================================
    # Node Implementations
    # ========================================================================

    async def load_project_node(self, state: CampaignState) -> dict:
        """
        Load project details and brief from disk.

        This is the entry point of the workflow.
        """
        logger.info(f"Loading project: {state['project_id']}")

        try:
            # Load project metadata
            project = await self.file_service.load_project(state["project_id"])

            # Load brief
            brief_path = f"campanas-completadas/{state['project_id']}/brief-original.md"
            with open(brief_path, 'r', encoding='utf-8') as f:
                brief = f.read()

            return {
                "brief": brief,
                "client": project.get("client", "Unknown Client"),
                "country": project.get("country", "Unknown Country"),
                "language": project.get("language", "es"),
                "campaign_type": project.get("campaign_type", "digital"),
                "execution_start_time": datetime.now(),
                "current_node": "load_project"
            }

        except Exception as e:
            logger.error(f"Error loading project: {e}")
            return {
                "errors": [f"Failed to load project: {str(e)}"],
                "current_node": "load_project"
            }

    async def research_market_node(self, state: CampaignState) -> dict:
        """
        Research market trends and competitive landscape.

        This runs in PARALLEL with research_culture and research_digital.
        """
        logger.info(f"Researching market for {state['client']} in {state['country']}")

        prompt = f"""You are a market research expert analyzing the {state['client']} campaign opportunity.

BRIEF:
{state['brief']}

TASK:
Research and analyze:
1. Market overview for {state['client']}'s industry in {state['country']}
2. Competitive landscape (main competitors, their positioning)
3. Market trends and opportunities
4. Consumer behavior patterns
5. Price sensitivity and value propositions

Provide a comprehensive market analysis (500-800 words) with specific insights for this campaign.
"""

        try:
            messages = [
                SystemMessage(content="You are a market research expert."),
                HumanMessage(content=prompt)
            ]

            response = await self.llm.ainvoke(messages)

            logger.info(f"Market research complete: {len(response.content)} chars")

            return {
                "market_research": response.content,
                "current_node": "research_market"
            }

        except Exception as e:
            logger.error(f"Error in market research: {e}")
            return {
                "market_research": f"Error: {str(e)}",
                "errors": [f"Market research failed: {str(e)}"],
                "current_node": "research_market"
            }

    async def research_culture_node(self, state: CampaignState) -> dict:
        """
        Research cultural insights and local context.

        This runs in PARALLEL with research_market and research_digital.
        """
        logger.info(f"Researching culture for {state['country']}")

        prompt = f"""You are a cultural anthropologist analyzing {state['country']} for a marketing campaign.

BRIEF:
{state['brief']}

TASK:
Analyze and provide insights on:
1. Cultural values and traditions in {state['country']}
2. Communication style preferences (formal vs casual, humor, tone)
3. Local expressions, slang, and language nuances
4. Important cultural dates, celebrations, and moments
5. Do's and don'ts for marketing in this culture
6. What makes content go viral locally

Provide a deep cultural analysis (500-800 words) that will inform campaign creative.
"""

        try:
            messages = [
                SystemMessage(content="You are a cultural anthropologist."),
                HumanMessage(content=prompt)
            ]

            response = await self.llm.ainvoke(messages)

            logger.info(f"Cultural research complete: {len(response.content)} chars")

            return {
                "cultural_insights": response.content,
                "current_node": "research_culture"
            }

        except Exception as e:
            logger.error(f"Error in cultural research: {e}")
            return {
                "cultural_insights": f"Error: {str(e)}",
                "errors": [f"Cultural research failed: {str(e)}"],
                "current_node": "research_culture"
            }

    async def research_digital_node(self, state: CampaignState) -> dict:
        """
        Research digital behavior and social media trends.

        This runs in PARALLEL with research_market and research_culture.
        """
        logger.info(f"Researching digital trends for {state['country']}")

        prompt = f"""You are a digital strategist analyzing online behavior in {state['country']}.

BRIEF:
{state['brief']}

TASK:
Research and analyze:
1. Social media platform usage and preferences
2. Content formats that perform well (video, images, text, memes)
3. Influencer landscape and typical engagement rates
4. Viral content patterns and examples
5. Best times to post and engagement patterns
6. Digital advertising trends and benchmarks

Provide a digital strategy brief (500-800 words) with actionable insights.
"""

        try:
            messages = [
                SystemMessage(content="You are a digital strategist."),
                HumanMessage(content=prompt)
            ]

            response = await self.llm.ainvoke(messages)

            logger.info(f"Digital research complete: {len(response.content)} chars")

            return {
                "digital_trends": response.content,
                "current_node": "research_digital"
            }

        except Exception as e:
            logger.error(f"Error in digital research: {e}")
            return {
                "digital_trends": f"Error: {str(e)}",
                "errors": [f"Digital research failed: {str(e)}"],
                "current_node": "research_digital"
            }

    async def synthesize_research_node(self, state: CampaignState) -> dict:
        """
        Synthesize all research into a coherent brief.

        This node waits for all 3 parallel research nodes to complete.
        """
        logger.info("Synthesizing research findings")

        # Check if all research completed successfully
        has_errors = (
            "Error:" in state.get("market_research", "") or
            "Error:" in state.get("cultural_insights", "") or
            "Error:" in state.get("digital_trends", "")
        )

        if has_errors:
            logger.warning("Some research tasks had errors, proceeding with available data")

        synthesis = f"""# RESEARCH SYNTHESIS

## Market Analysis
{state.get('market_research', 'Not available')}

## Cultural Insights
{state.get('cultural_insights', 'Not available')}

## Digital Trends
{state.get('digital_trends', 'Not available')}
"""

        return {
            "research_synthesis": synthesis,
            "research_complete": True,
            "research_end_time": datetime.now(),
            "current_node": "synthesize_research"
        }

    async def generate_ideas_node(self, state: CampaignState) -> dict:
        """
        Generate a batch of campaign ideas.

        This node may loop multiple times via conditional edge.
        """
        current_batch = state.get("current_batch", 0) + 1
        total_batches = state.get("total_batches", 3)

        logger.info(f"Generating ideas batch {current_batch}/{total_batches}")

        prompt = f"""You are an award-winning Creative Director generating campaign ideas.

BRIEF:
{state['brief']}

RESEARCH:
{state.get('research_synthesis', '')}

TASK:
Generate 5 creative campaign ideas for {state['client']} in {state['country']}.

For each idea, provide:
1. **Title**: Catchy campaign name
2. **Headline**: Main tagline/headline
3. **Description**: 3 paragraphs explaining the concept
4. **Rationale**: Why this will work (insights from research)
5. **Execution**: List of 5 specific tactics/channels

Output format:
```json
{{
  "ideas": [
    {{
      "title": "Campaign Name",
      "headline": "Main Tagline",
      "description": "Paragraph 1...\n\nParagraph 2...\n\nParagraph 3...",
      "rationale": "Why this works...",
      "execution": ["Tactic 1", "Tactic 2", "Tactic 3", "Tactic 4", "Tactic 5"]
    }},
    // ... 4 more ideas
  ]
}}
```

Generate ideas now.
"""

        try:
            messages = [
                SystemMessage(content="You are an award-winning Creative Director. Output ONLY valid JSON, no markdown or explanations."),
                HumanMessage(content=prompt)
            ]

            response = await self.llm.ainvoke(messages)

            # Parse JSON response
            import json
            import re

            # Extract JSON from markdown code blocks if present
            content = response.content
            if "```json" in content:
                content = re.search(r'```json\n(.*?)\n```', content, re.DOTALL).group(1)
            elif "```" in content:
                content = re.search(r'```\n(.*?)\n```', content, re.DOTALL).group(1)

            data = json.loads(content)
            new_ideas = data.get("ideas", [])

            # Add batch number to each idea
            for i, idea in enumerate(new_ideas):
                idea["id"] = f"idea-{current_batch:03d}-{i+1:02d}"
                idea["batch"] = current_batch

            logger.info(f"Generated {len(new_ideas)} ideas in batch {current_batch}")

            return {
                "ideas": new_ideas,
                "current_batch": current_batch,
                "current_node": "generate_ideas"
            }

        except Exception as e:
            logger.error(f"Error generating ideas: {e}")
            return {
                "errors": [f"Idea generation failed (batch {current_batch}): {str(e)}"],
                "current_batch": current_batch,
                "current_node": "generate_ideas"
            }

    async def evaluate_ideas_node(self, state: CampaignState) -> dict:
        """
        Evaluate all generated ideas and rank them.
        """
        logger.info(f"Evaluating {len(state['ideas'])} ideas")

        scored_ideas = []

        for idea in state["ideas"]:
            try:
                # Evaluate with LLM
                prompt = f"""You are a Strategic Planner evaluating campaign ideas.

BRIEF:
{state['brief']}

IDEA:
Title: {idea['title']}
Headline: {idea['headline']}
Description: {idea['description']}
Rationale: {idea['rationale']}

TASK:
Evaluate this idea on:
1. **Relevance** (0-10): How well does it address the brief?
2. **Creativity** (0-10): How original and breakthrough is it?
3. **Feasibility** (0-10): How realistic is execution?
4. **Impact** (0-10): How likely is it to achieve results?

Output format:
```json
{{
  "relevance": 8,
  "creativity": 9,
  "feasibility": 7,
  "impact": 8,
  "feedback": "Brief explanation of scores"
}}
```
"""

                messages = [
                    SystemMessage(content="You are a Strategic Planner. Output ONLY valid JSON."),
                    HumanMessage(content=prompt)
                ]

                response = await self.llm.ainvoke(messages)

                # Parse scores
                import json
                import re
                content = response.content
                if "```json" in content:
                    content = re.search(r'```json\n(.*?)\n```', content, re.DOTALL).group(1)
                elif "```" in content:
                    content = re.search(r'```\n(.*?)\n```', content, re.DOTALL).group(1)

                scores = json.loads(content)

                # Calculate overall score (weighted average)
                overall = (
                    scores["relevance"] * 0.3 +
                    scores["creativity"] * 0.3 +
                    scores["feasibility"] * 0.2 +
                    scores["impact"] * 0.2
                )

                scored_idea = {
                    **idea,
                    "scores": scores,
                    "overall_score": overall
                }

                scored_ideas.append(scored_idea)

            except Exception as e:
                logger.error(f"Error evaluating idea {idea.get('id')}: {e}")
                scored_ideas.append({
                    **idea,
                    "scores": {"error": str(e)},
                    "overall_score": 0
                })

        # Sort by overall score
        scored_ideas.sort(key=lambda x: x["overall_score"], reverse=True)

        logger.info(f"Evaluation complete. Top score: {scored_ideas[0]['overall_score']:.1f}")

        return {
            "scored_ideas": scored_ideas,
            "top_ideas": scored_ideas[:5],
            "evaluation_complete": True,
            "current_node": "evaluate_ideas"
        }

    async def export_results_node(self, state: CampaignState) -> dict:
        """
        Export results to markdown files.
        """
        logger.info("Exporting results")

        try:
            project_id = state["project_id"]
            ideas_dir = f"campanas-completadas/{project_id}/ideas"

            # Create ideas directory if it doesn't exist
            import os
            os.makedirs(ideas_dir, exist_ok=True)

            # Export each idea
            export_paths = []
            for idea in state["scored_ideas"]:
                filename = f"{ideas_dir}/{idea['id']}.md"

                content = f"""# {idea['title']}

## Headline
{idea['headline']}

## Description
{idea['description']}

## Rationale
{idea['rationale']}

## Execution
{chr(10).join(f"{i+1}. {tactic}" for i, tactic in enumerate(idea['execution']))}

## Scores
- **Relevance**: {idea['scores'].get('relevance', 0)}/10
- **Creativity**: {idea['scores'].get('creativity', 0)}/10
- **Feasibility**: {idea['scores'].get('feasibility', 0)}/10
- **Impact**: {idea['scores'].get('impact', 0)}/10
- **Overall**: {idea['overall_score']:.1f}/10

### Feedback
{idea['scores'].get('feedback', 'No feedback available')}
"""

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)

                export_paths.append(filename)

            # Create summary
            summary_path = f"campanas-completadas/{project_id}/ideas-summary.md"
            summary = f"""# Campaign Ideas Summary - {state['client']}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Top 5 Ideas

"""

            for i, idea in enumerate(state["top_ideas"], 1):
                summary += f"""### {i}. {idea['title']} (Score: {idea['overall_score']:.1f}/10)
**Headline**: {idea['headline']}

{idea['description'][:200]}...

---

"""

            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary)

            export_paths.append(summary_path)

            logger.info(f"Exported {len(export_paths)} files")

            return {
                "export_complete": True,
                "export_paths": export_paths,
                "execution_end_time": datetime.now(),
                "current_node": "export_results"
            }

        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            return {
                "export_complete": False,
                "errors": [f"Export failed: {str(e)}"],
                "current_node": "export_results"
            }

    # ========================================================================
    # Conditional Edge Functions
    # ========================================================================

    def _should_generate_more_ideas(
        self,
        state: CampaignState
    ) -> Literal["continue", "done"]:
        """
        Decide whether to generate more idea batches or move to evaluation.
        """
        current = state.get("current_batch", 0)
        total = state.get("total_batches", 3)

        if current < total:
            logger.info(f"Batch {current}/{total} complete, continuing...")
            return "continue"
        else:
            logger.info(f"All {total} batches complete, moving to evaluation")
            return "done"

    # ========================================================================
    # Public API
    # ========================================================================

    async def run_campaign(
        self,
        project_id: str,
        num_ideas: int = 15
    ) -> CampaignState:
        """
        Run the complete campaign generation workflow.

        Args:
            project_id: Unique project identifier
            num_ideas: Total number of ideas to generate

        Returns:
            Final state with all results
        """
        logger.info(f"Starting campaign generation for {project_id}")

        # Calculate batches (5 ideas per batch)
        total_batches = (num_ideas + 4) // 5  # Round up

        # Create initial state
        initial_state: CampaignState = {
            "project_id": project_id,
            "brief": "",
            "client": "",
            "country": "",
            "language": "es",
            "campaign_type": "digital",
            "market_research": "",
            "cultural_insights": "",
            "digital_trends": "",
            "research_synthesis": "",
            "research_complete": False,
            "research_start_time": None,
            "research_end_time": None,
            "ideas": [],
            "current_batch": 0,
            "total_batches": total_batches,
            "ideation_start_time": None,
            "scored_ideas": [],
            "top_ideas": [],
            "evaluation_complete": False,
            "export_complete": False,
            "export_paths": [],
            "total_cost": 0.0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
            "execution_start_time": datetime.now(),
            "execution_end_time": None,
            "errors": [],
            "warnings": [],
            "current_node": "start",
            "should_continue": True,
            "retry_count": 0,
            "max_retries": 3
        }

        # Configure checkpointing
        config = {
            "configurable": {
                "thread_id": f"campaign-{project_id}"
            }
        }

        # Execute graph
        try:
            final_state = await self.graph.ainvoke(initial_state, config=config)

            duration = (
                final_state.get("execution_end_time", datetime.now()) -
                final_state["execution_start_time"]
            ).total_seconds()

            logger.info(
                f"Campaign generation complete in {duration:.1f}s. "
                f"Generated {len(final_state['ideas'])} ideas."
            )

            return final_state

        except Exception as e:
            logger.error(f"Campaign generation failed: {e}")
            raise

    async def stream_campaign(self, project_id: str, num_ideas: int = 15):
        """
        Stream campaign generation with real-time updates.

        Yields state updates after each node execution.
        """
        total_batches = (num_ideas + 4) // 5

        initial_state: CampaignState = {
            "project_id": project_id,
            "brief": "",
            "client": "",
            "country": "",
            "language": "es",
            "campaign_type": "digital",
            "market_research": "",
            "cultural_insights": "",
            "digital_trends": "",
            "research_synthesis": "",
            "research_complete": False,
            "research_start_time": None,
            "research_end_time": None,
            "ideas": [],
            "current_batch": 0,
            "total_batches": total_batches,
            "ideation_start_time": None,
            "scored_ideas": [],
            "top_ideas": [],
            "evaluation_complete": False,
            "export_complete": False,
            "export_paths": [],
            "total_cost": 0.0,
            "total_tokens_input": 0,
            "total_tokens_output": 0,
            "execution_start_time": datetime.now(),
            "execution_end_time": None,
            "errors": [],
            "warnings": [],
            "current_node": "start",
            "should_continue": True,
            "retry_count": 0,
            "max_retries": 3
        }

        config = {
            "configurable": {
                "thread_id": f"campaign-{project_id}"
            }
        }

        # Stream events
        async for event in self.graph.astream(initial_state, config=config):
            yield event

    def visualize(self, output_path: str = "campaign_graph.png"):
        """
        Generate visual diagram of the workflow.

        Args:
            output_path: Where to save the diagram
        """
        try:
            from IPython.display import Image

            # Generate Mermaid diagram
            img = self.graph.get_graph().draw_mermaid_png()

            with open(output_path, 'wb') as f:
                f.write(img)

            logger.info(f"Graph visualization saved to {output_path}")
            return img

        except Exception as e:
            logger.error(f"Could not generate visualization: {e}")
            return None


# Convenience factory function
def get_campaign_graph() -> CampaignGraph:
    """Get configured campaign graph instance."""
    return CampaignGraph()
```

---

**Testing**: Test the graph structure

```bash
# Test graph initialization
python -c "
from code.api.graphs.campaign_graph import get_campaign_graph

graph = get_campaign_graph()
print('✓ Graph initialized successfully')

# Try to visualize (requires graphviz)
# graph.visualize('test_graph.png')
"
```

**Expected output**: "✓ Graph initialized successfully"

---

### Day 3: PostgreSQL Checkpointing Setup

**Goal**: Configure state persistence so workflows can be resumed after crashes

#### Task 3.1: Create Checkpointing Table

```sql
-- Run this SQL in your PostgreSQL database

CREATE TABLE IF NOT EXISTS langgraph_checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (thread_id, checkpoint_id)
);

CREATE INDEX idx_langgraph_thread ON langgraph_checkpoints(thread_id);
CREATE INDEX idx_langgraph_parent ON langgraph_checkpoints(parent_checkpoint_id);
```

Or run via Python:

```python
# code/scripts/setup_checkpointing.py
import asyncio
import asyncpg
from code.api.config import get_settings

settings = get_settings()

async def setup_checkpointing():
    """Create checkpointing table in PostgreSQL."""

    conn = await asyncpg.connect(settings.database_url.replace('+asyncpg', ''))

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS langgraph_checkpoints (
            thread_id TEXT NOT NULL,
            checkpoint_id TEXT NOT NULL,
            parent_checkpoint_id TEXT,
            checkpoint JSONB NOT NULL,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (thread_id, checkpoint_id)
        );

        CREATE INDEX IF NOT EXISTS idx_langgraph_thread
        ON langgraph_checkpoints(thread_id);

        CREATE INDEX IF NOT EXISTS idx_langgraph_parent
        ON langgraph_checkpoints(parent_checkpoint_id);
    """)

    await conn.close()
    print("✓ Checkpointing table created")

if __name__ == "__main__":
    asyncio.run(setup_checkpointing())
```

Run it:

```bash
python code/scripts/setup_checkpointing.py
```

---

### Day 4-5: Integration with Existing Services

**Goal**: Connect the new graph to existing API routes with feature flag

#### Task 4.1: Update Ideas Service

**File**: `code/api/services/ideas_service.py` (MODIFY)

```python
# Add at the top
from ..graphs.campaign_graph import get_campaign_graph
from ..config import get_settings

settings = get_settings()

class IdeasService:
    def __init__(self):
        # Existing code...

        # Add LangGraph
        if settings.use_langgraph_v2:
            self.campaign_graph = get_campaign_graph()

    async def generate_ideas(
        self,
        project_id: str,
        num_ideas: int = 15,
        batch_size: int = 5
    ) -> list:
        """
        Generate ideas (routes to v1 or v2 based on feature flag).
        """

        if settings.use_langgraph_v2:
            # Use LangGraph v2
            logger.info("Using LangGraph v2 for idea generation")

            result = await self.campaign_graph.run_campaign(
                project_id=project_id,
                num_ideas=num_ideas
            )

            return result["scored_ideas"]

        else:
            # Use existing v1 implementation
            logger.info("Using legacy v1 for idea generation")

            # ... existing code ...
```

#### Task 4.2: Add API Route for Streaming

**File**: `code/api/routes/ideas_routes.py` (ADD)

```python
from fastapi.responses import StreamingResponse
import json

@router.post("/projects/{project_id}/ideas/stream")
async def stream_idea_generation(
    project_id: str,
    num_ideas: int = 15,
    api_key: str = Depends(verify_api_key)
):
    """
    Stream idea generation with real-time updates (LangGraph v2 only).

    Returns Server-Sent Events (SSE) stream.
    """

    if not settings.use_langgraph_v2:
        raise HTTPException(
            status_code=400,
            detail="Streaming requires LangGraph v2. Set USE_LANGGRAPH_V2=true"
        )

    graph = get_campaign_graph()

    async def event_stream():
        """Generate SSE events."""

        try:
            async for event in graph.stream_campaign(project_id, num_ideas):
                # event is a dict like: {"node_name": {...state_updates...}}

                for node_name, state_update in event.items():
                    # Send update to client
                    sse_data = {
                        "type": "node_update",
                        "node": node_name,
                        "current_batch": state_update.get("current_batch", 0),
                        "total_batches": state_update.get("total_batches", 0),
                        "ideas_count": len(state_update.get("ideas", [])),
                        "current_node": state_update.get("current_node", ""),
                        "timestamp": datetime.now().isoformat()
                    }

                    yield f"data: {json.dumps(sse_data)}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

---

### End of Week 1 Deliverables

**Completed**:
- ✅ Internal LLM integration (zero vendor lock-in)
- ✅ Campaign state models defined
- ✅ Main CampaignGraph with parallel research
- ✅ PostgreSQL checkpointing configured
- ✅ Integration with existing API (feature flag)
- ✅ Streaming endpoint for real-time updates

**Testing**:

```bash
# Test end-to-end with v2
export USE_LANGGRAPH_V2=true

cd code
python cli.py generate \
  --project-id "campana-ueno-bank-paraguay-2025" \
  --num-ideas 15 \
  --batch-size 5
```

**Expected**: Campaign generates successfully using LangGraph, faster than v1 due to parallel research.

---

## 3. Week 2: Ideation & Evaluation Subgraphs

### Day 6-7: Ideation Subgraph with Critique Loop

**Goal**: Add iterative refinement to idea generation

[Continue with detailed Week 2 and Week 3 implementation steps...]

---

**Would you like me to continue with the complete Week 2 and Week 3 detailed implementation? This document is getting very long (currently at ~8,000 words). I can either:**

1. **Continue in this file** with complete Week 2 & 3 details (will be ~20,000 words total)
2. **Create separate files** for each week (easier to navigate)
3. **Provide a condensed version** with just the key steps

What would you prefer?
