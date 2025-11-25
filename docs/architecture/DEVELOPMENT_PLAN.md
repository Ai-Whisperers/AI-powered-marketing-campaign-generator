# Campaign Generator - Development Plan

Detailed implementation plan for the Campaign Research Generator system.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Design](#architecture-design)
4. [Module Specifications](#module-specifications)
5. [AI Integration Strategy](#ai-integration-strategy)
6. [Development Phases](#development-phases)
7. [API Specifications](#api-specifications)
8. [Data Models](#data-models)
9. [Testing Strategy](#testing-strategy)
10. [Deployment](#deployment)

---

## Project Overview

### Vision
Build an AI-powered campaign research generator that automates the creation, research, ideation, and synthesis of marketing campaign projects.

### Goals
1. **Reduce time** from 11 days to 3-5 days per campaign
2. **Ensure consistency** across all projects
3. **Leverage AI** for research summarization and idea generation
4. **Provide insights** through automated scoring and analysis

### Success Metrics
- Time to complete campaign research: < 5 days
- Research sources per project: 50+ automatically formatted
- Ideas generated per campaign: 25 with full scoring
- User satisfaction: Professional-grade outputs

---

## Technology Stack

### Core Framework
```yaml
Language: Python 3.11+
CLI Framework: Click 8.x
Config: PyYAML + Pydantic
Templates: Jinja2
Testing: Pytest
```

### AI Providers
```yaml
Primary: Anthropic Claude (claude-sonnet-4-20250514)
  - Research summarization
  - Brief analysis
  - Idea generation assistance
  - Content synthesis

Secondary: OpenAI GPT-4
  - Fallback provider
  - Embeddings for similarity
  - Vision for image analysis

Local: Claude Code CLI
  - Development assistance
  - Code generation
  - Debugging
```

### Data & Storage
```yaml
File Format: Markdown + YAML frontmatter
Config: YAML
Cache: SQLite (local)
Export: PDF (ReportLab), PPTX (python-pptx)
```

### External Services
```yaml
URL Validation: requests + validators
Web Scraping: BeautifulSoup4 + httpx
Rate Limiting: tenacity
```

---

## Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                    CLI Interface                     │
│              (Click command groups)                  │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                  Core Services                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Config   │ │ Template │ │ AI       │ │ Cache  │ │
│  │ Manager  │ │ Engine   │ │ Service  │ │ Layer  │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                 Domain Modules                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │Generator │ │ Research │ │ Scoring  │ │Synthesis│ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│  ┌──────────┐                                       │
│  │ Export   │                                       │
│  └──────────┘                                       │
└─────────────────────────────────────────────────────┘
```

### Directory Structure

```
code/
├── pyproject.toml              # Project config & dependencies
├── README.md                   # Development documentation
├── DEVELOPMENT_PLAN.md         # This file
│
├── src/
│   ├── __init__.py
│   ├── cli.py                  # Main CLI entry point
│   │
│   ├── core/                   # Core services
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── templates.py        # Jinja2 template engine
│   │   ├── ai_service.py       # AI provider abstraction
│   │   ├── cache.py            # Local caching
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── generator/              # Project generation
│   │   ├── __init__.py
│   │   ├── project.py          # Project creator
│   │   ├── structure.py        # Folder structure
│   │   └── templates.py        # Content templates
│   │
│   ├── research/               # Research management
│   │   ├── __init__.py
│   │   ├── sources.py          # Source CRUD
│   │   ├── tracker.py          # Progress tracking
│   │   ├── scraper.py          # Web scraping
│   │   └── summarizer.py       # AI summarization
│   │
│   ├── scoring/                # Idea scoring
│   │   ├── __init__.py
│   │   ├── calculator.py       # Score computation
│   │   ├── criteria.py         # Criteria management
│   │   └── reports.py          # Ranking reports
│   │
│   ├── synthesis/              # Content synthesis
│   │   ├── __init__.py
│   │   ├── quick_reference.py  # QR generation
│   │   ├── brief_analyzer.py   # Brief parsing
│   │   └── cross_reference.py  # Link validation
│   │
│   └── export/                 # Output generation
│       ├── __init__.py
│       ├── pdf.py              # PDF export
│       ├── presentation.py     # PPTX generation
│       └── reports.py          # Executive reports
│
├── config/
│   ├── default.yaml            # Default configuration
│   ├── prompts/                # AI prompts
│   │   ├── research_summary.txt
│   │   ├── brief_analysis.txt
│   │   ├── idea_generation.txt
│   │   └── quick_reference.txt
│   └── templates/              # Jinja2 templates
│       ├── idea.md.j2
│       ├── quick_reference.md.j2
│       ├── brief.md.j2
│       └── research_file.md.j2
│
└── tests/
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures
    ├── test_generator.py
    ├── test_research.py
    ├── test_scoring.py
    ├── test_synthesis.py
    └── test_export.py
```

---

## Module Specifications

### 1. Core Module (`src/core/`)

#### config.py
```python
"""Configuration management with Pydantic validation."""

from pydantic import BaseModel, Field
from pathlib import Path
import yaml

class AIConfig(BaseModel):
    provider: str = "anthropic"  # or "openai"
    model: str = "claude-sonnet-4-20250514"
    api_key_env: str = "ANTHROPIC_API_KEY"
    max_tokens: int = 4096
    temperature: float = 0.7

class ScoringConfig(BaseModel):
    criteria: list[dict]
    thresholds: dict[str, int]
    weights: dict[str, float] = {}

class ProjectConfig(BaseModel):
    default_country: str = "Paraguay"
    default_type: str = "digital"
    num_ideas: int = 25
    research_categories: int = 10

class AppConfig(BaseModel):
    ai: AIConfig
    scoring: ScoringConfig
    project: ProjectConfig
    templates_dir: Path
    prompts_dir: Path

def load_config(config_path: Path = None) -> AppConfig:
    """Load configuration from YAML file."""
    pass

def get_config() -> AppConfig:
    """Get global configuration singleton."""
    pass
```

#### ai_service.py
```python
"""Unified AI service supporting multiple providers."""

from abc import ABC, abstractmethod
from anthropic import Anthropic
from openai import OpenAI

class AIProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, system: str = None) -> str:
        pass

    @abstractmethod
    async def summarize(self, content: str, max_length: int = 500) -> str:
        pass

class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    async def complete(self, prompt: str, system: str = None) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or "You are a marketing research assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def summarize(self, content: str, max_length: int = 500) -> str:
        prompt = f"Summarize the following in {max_length} characters:\n\n{content}"
        return await self.complete(prompt)

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def complete(self, prompt: str, system: str = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system or "You are a marketing research assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

class AIService:
    """Factory for AI providers with fallback support."""

    def __init__(self, primary: str = "anthropic", fallback: str = "openai"):
        self.primary = self._create_provider(primary)
        self.fallback = self._create_provider(fallback) if fallback else None

    def _create_provider(self, name: str) -> AIProvider:
        if name == "anthropic":
            return AnthropicProvider(os.getenv("ANTHROPIC_API_KEY"))
        elif name == "openai":
            return OpenAIProvider(os.getenv("OPENAI_API_KEY"))
        raise ValueError(f"Unknown provider: {name}")

    async def complete(self, prompt: str, **kwargs) -> str:
        try:
            return await self.primary.complete(prompt, **kwargs)
        except Exception as e:
            if self.fallback:
                return await self.fallback.complete(prompt, **kwargs)
            raise
```

---

### 2. Generator Module (`src/generator/`)

#### project.py
```python
"""Project creation and management."""

from pathlib import Path
from datetime import datetime
from ..core.config import get_config
from ..core.templates import TemplateEngine

class ProjectCreator:
    def __init__(self, templates: TemplateEngine):
        self.templates = templates
        self.config = get_config()

    def create(
        self,
        brand: str,
        country: str = None,
        campaign_type: str = None,
        year: int = None,
        num_ideas: int = None,
        output_dir: Path = None
    ) -> Path:
        """Create complete project structure."""

        # Apply defaults
        country = country or self.config.project.default_country
        campaign_type = campaign_type or self.config.project.default_type
        year = year or datetime.now().year
        num_ideas = num_ideas or self.config.project.num_ideas
        output_dir = output_dir or Path.cwd()

        # Create project folder
        project_name = f"campana-{self._normalize(brand)}-{year}"
        project_path = output_dir / project_name
        project_path.mkdir(parents=True, exist_ok=True)

        # Create structure
        self._create_readme(project_path, brand, country, campaign_type, year)
        self._create_research_structure(project_path, brand, country)
        self._create_ideas_structure(project_path, brand, num_ideas)

        return project_path

    def _normalize(self, name: str) -> str:
        return name.lower().replace(" ", "-")

    def _create_readme(self, path: Path, brand: str, country: str,
                       campaign_type: str, year: int):
        content = self.templates.render("readme.md.j2", {
            "brand": brand,
            "country": country,
            "campaign_type": campaign_type,
            "year": year,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        })
        (path / "README.md").write_text(content, encoding="utf-8")

    def _create_research_structure(self, path: Path, brand: str, country: str):
        """Create 10 research category folders with templates."""
        research_path = path / f"investigacion-{self._normalize(brand)}-{self._normalize(country)}"
        research_path.mkdir(parents=True, exist_ok=True)

        categories = [
            ("01-mercado-general", ["resumen-mercado.md", "tendencias.md"]),
            ("02-marca", ["historia.md", "posicionamiento.md"]),
            ("03-competencia", ["directa.md", "indirecta.md"]),
            ("04-consumidor", ["perfil.md", "comportamiento.md"]),
            ("05-cultura", ["local.md", "tradiciones.md"]),
            ("06-tendencias", ["industria.md", "digital.md"]),
            ("07-estadisticas", ["datos-clave.md"]),
            ("08-referencias", ["fuentes-completas.md"]),
            ("09-nuevos-hallazgos", ["resumen.md"]),
            ("10-investigacion-creativa", [
                "campanas-ganadoras.md",
                "contenido-viral.md",
                "comportamiento-digital.md"
            ])
        ]

        for folder, files in categories:
            folder_path = research_path / folder
            folder_path.mkdir(exist_ok=True)

            for filename in files:
                content = self.templates.render("research_file.md.j2", {
                    "title": filename.replace(".md", "").replace("-", " ").title(),
                    "category": folder,
                    "brand": brand
                })
                (folder_path / filename).write_text(content, encoding="utf-8")

    def _create_ideas_structure(self, path: Path, brand: str, num_ideas: int):
        """Create idea templates."""
        ideas_path = path / "ideas"
        ideas_path.mkdir(exist_ok=True)

        # Summary file
        summary = self.templates.render("ideas_summary.md.j2", {"brand": brand})
        (ideas_path / "00-RESUMEN-IDEAS.md").write_text(summary, encoding="utf-8")

        # Individual ideas
        for i in range(1, num_ideas + 1):
            content = self.templates.render("idea.md.j2", {
                "number": i,
                "brand": brand
            })
            (ideas_path / f"idea-{i:02d}-nombre.md").write_text(content, encoding="utf-8")
```

---

### 3. Research Module (`src/research/`)

#### sources.py
```python
"""Source management with validation and formatting."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import yaml
import httpx
from validators import url as validate_url

@dataclass
class Source:
    url: str
    title: str
    category: str  # media, corporate, study, institutional
    topic: str
    date_accessed: datetime = field(default_factory=datetime.now)
    is_valid: bool = True
    summary: Optional[str] = None

    def to_markdown(self) -> str:
        return f"- [{self.title}]({self.url}) - {self.topic} ({self.date_accessed.strftime('%Y')})"

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "category": self.category,
            "topic": self.topic,
            "date_accessed": self.date_accessed.isoformat(),
            "is_valid": self.is_valid,
            "summary": self.summary
        }

class SourceManager:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.sources_file = self._find_sources_file()
        self.sources: list[Source] = []
        self._load_sources()

    def _find_sources_file(self) -> Path:
        """Find fuentes-completas.md in the project."""
        for path in self.project_path.rglob("fuentes-completas.md"):
            return path
        raise FileNotFoundError("Sources file not found")

    def _load_sources(self):
        """Load existing sources from file."""
        # Parse markdown and extract sources
        pass

    async def add(self, url: str, title: str, category: str, topic: str) -> Source:
        """Add a new source with validation."""
        # Validate URL
        if not validate_url(url):
            raise ValueError(f"Invalid URL: {url}")

        # Check if URL is accessible
        async with httpx.AsyncClient() as client:
            try:
                response = await client.head(url, follow_redirects=True)
                is_valid = response.status_code < 400
            except:
                is_valid = False

        source = Source(
            url=url,
            title=title,
            category=category,
            topic=topic,
            is_valid=is_valid
        )

        self.sources.append(source)
        await self._save_sources()

        return source

    async def validate_all(self) -> dict[str, list[Source]]:
        """Validate all sources and return status."""
        valid = []
        invalid = []

        async with httpx.AsyncClient() as client:
            for source in self.sources:
                try:
                    response = await client.head(source.url, follow_redirects=True)
                    source.is_valid = response.status_code < 400
                except:
                    source.is_valid = False

                if source.is_valid:
                    valid.append(source)
                else:
                    invalid.append(source)

        await self._save_sources()
        return {"valid": valid, "invalid": invalid}

    def get_by_category(self, category: str) -> list[Source]:
        """Get sources by category."""
        return [s for s in self.sources if s.category == category]

    def get_stats(self) -> dict:
        """Get source statistics."""
        categories = {}
        for source in self.sources:
            categories[source.category] = categories.get(source.category, 0) + 1

        return {
            "total": len(self.sources),
            "by_category": categories,
            "valid": sum(1 for s in self.sources if s.is_valid),
            "invalid": sum(1 for s in self.sources if not s.is_valid)
        }

    async def _save_sources(self):
        """Save sources to markdown file."""
        # Generate markdown content
        content = self._generate_markdown()
        self.sources_file.write_text(content, encoding="utf-8")

    def _generate_markdown(self) -> str:
        """Generate fuentes-completas.md content."""
        sections = {
            "media": "## Medios de Comunicación",
            "corporate": "## Fuentes Corporativas",
            "study": "## Estudios e Informes",
            "institutional": "## Fuentes Institucionales"
        }

        content = "# Fuentes Completas\n\n"

        # Stats table
        stats = self.get_stats()
        content += "## Resumen\n\n"
        content += "| Categoría | Cantidad |\n|-----------|----------|\n"
        for cat, count in stats["by_category"].items():
            content += f"| {cat.title()} | {count} |\n"
        content += f"| **Total** | **{stats['total']}** |\n\n"

        # Sources by category
        for category, header in sections.items():
            sources = self.get_by_category(category)
            if sources:
                content += f"{header}\n\n"
                for source in sources:
                    content += source.to_markdown() + "\n"
                content += "\n"

        return content
```

#### summarizer.py
```python
"""AI-powered content summarization."""

from ..core.ai_service import AIService
from pathlib import Path

class ResearchSummarizer:
    def __init__(self, ai_service: AIService):
        self.ai = ai_service

    async def summarize_url(self, url: str, max_length: int = 500) -> str:
        """Fetch and summarize content from URL."""
        # Fetch content
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            html = response.text

        # Extract text from HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)

        # Summarize with AI
        prompt = f"""Summarize the following content for marketing research purposes.
Focus on:
- Key statistics and data points
- Market insights
- Consumer behavior patterns
- Competitive information

Content:
{text[:8000]}

Provide a summary in Spanish, maximum {max_length} characters."""

        return await self.ai.complete(prompt)

    async def summarize_file(self, file_path: Path) -> str:
        """Summarize a research markdown file."""
        content = file_path.read_text(encoding="utf-8")
        return await self.ai.summarize(content)

    async def extract_insights(self, content: str) -> list[str]:
        """Extract key insights from content."""
        prompt = f"""Extract 3-5 key insights from this marketing research content.
Each insight should be:
- Actionable for creative development
- Specific (include numbers when available)
- Relevant to campaign strategy

Content:
{content}

Return as a numbered list in Spanish."""

        response = await self.ai.complete(prompt)
        # Parse numbered list
        insights = []
        for line in response.split('\n'):
            line = line.strip()
            if line and line[0].isdigit():
                insights.append(line.split('.', 1)[-1].strip())

        return insights
```

---

### 4. Scoring Module (`src/scoring/`)

#### calculator.py
```python
"""Score calculation and ranking."""

from dataclasses import dataclass
from pathlib import Path
import re
import yaml

@dataclass
class IdeaScore:
    idea_number: int
    idea_name: str
    scores: dict[str, int]  # criterion -> score
    total: int
    tier: str
    file_path: Path

class ScoreCalculator:
    def __init__(self, config: dict):
        self.criteria = config.get("criteria", [])
        self.thresholds = config.get("thresholds", {
            "very_high": 90,
            "high": 80,
            "medium": 70,
            "needs_work": 60
        })
        self.weights = config.get("weights", {})

    def calculate_total(self, scores: dict[str, int]) -> int:
        """Calculate weighted total score."""
        total = 0
        for criterion, score in scores.items():
            weight = self.weights.get(criterion, 1.0)
            total += score * weight
        return int(total)

    def get_tier(self, total: int) -> str:
        """Get tier classification based on total score."""
        if total >= self.thresholds["very_high"]:
            return "🏆 MUY ALTO"
        elif total >= self.thresholds["high"]:
            return "🥇 ALTO"
        elif total >= self.thresholds["medium"]:
            return "🥈 MEDIO"
        elif total >= self.thresholds["needs_work"]:
            return "⚠️ NECESITA TRABAJO"
        else:
            return "❌ NO RECOMENDADO"

    def parse_idea_file(self, file_path: Path) -> IdeaScore:
        """Parse an idea markdown file and extract scores."""
        content = file_path.read_text(encoding="utf-8")

        # Extract idea number and name
        title_match = re.search(r"# Idea (\d+): \"(.+?)\"", content)
        if not title_match:
            raise ValueError(f"Could not parse idea title from {file_path}")

        idea_number = int(title_match.group(1))
        idea_name = title_match.group(2)

        # Extract scores from table
        scores = {}
        score_pattern = r"\| (\w+[\w\s]*) \| (\d+)/10 \|"
        for match in re.finditer(score_pattern, content):
            criterion = match.group(1).strip()
            score = int(match.group(2))
            scores[criterion] = score

        total = self.calculate_total(scores)
        tier = self.get_tier(total)

        return IdeaScore(
            idea_number=idea_number,
            idea_name=idea_name,
            scores=scores,
            total=total,
            tier=tier,
            file_path=file_path
        )

    def rank_ideas(self, ideas_dir: Path) -> list[IdeaScore]:
        """Parse all ideas and return ranked list."""
        ideas = []

        for file_path in sorted(ideas_dir.glob("idea-*.md")):
            try:
                idea = self.parse_idea_file(file_path)
                ideas.append(idea)
            except Exception as e:
                print(f"Warning: Could not parse {file_path}: {e}")

        # Sort by total score descending
        ideas.sort(key=lambda x: x.total, reverse=True)

        return ideas

    def generate_ranking_table(self, ideas: list[IdeaScore]) -> str:
        """Generate markdown ranking table."""
        table = "| # | Rank | Nombre | Puntaje | Tier |\n"
        table += "|---|------|--------|---------|------|\n"

        for rank, idea in enumerate(ideas, 1):
            table += f"| {idea.idea_number:02d} | {rank} | {idea.idea_name} | {idea.total}/100 | {idea.tier} |\n"

        return table
```

#### reports.py
```python
"""Generate scoring reports and summaries."""

from pathlib import Path
from .calculator import ScoreCalculator, IdeaScore
from ..core.templates import TemplateEngine

class ScoringReportGenerator:
    def __init__(self, calculator: ScoreCalculator, templates: TemplateEngine):
        self.calculator = calculator
        self.templates = templates

    def generate_summary(self, ideas: list[IdeaScore], brand: str) -> str:
        """Generate 00-RESUMEN-IDEAS.md content."""

        # Group by tier
        tiers = {
            "🏆 MUY ALTO": [],
            "🥇 ALTO": [],
            "🥈 MEDIO": [],
            "⚠️ NECESITA TRABAJO": [],
            "❌ NO RECOMENDADO": []
        }

        for idea in ideas:
            tiers[idea.tier].append(idea)

        # Get top 10
        top_10 = ideas[:10]

        # Generate recommendations
        recommendations = self._generate_recommendations(ideas)

        return self.templates.render("ideas_summary_complete.md.j2", {
            "brand": brand,
            "ideas": ideas,
            "tiers": tiers,
            "top_10": top_10,
            "recommendations": recommendations,
            "ranking_table": self.calculator.generate_ranking_table(ideas)
        })

    def _generate_recommendations(self, ideas: list[IdeaScore]) -> dict:
        """Generate three strategic recommendation options."""
        if not ideas:
            return {}

        # Option A: Highest overall score
        option_a = ideas[0]

        # Option B: Best for virality (if we have that criterion)
        viral_scores = [(i, i.scores.get("Potencial Viral", 0)) for i in ideas]
        viral_scores.sort(key=lambda x: x[1], reverse=True)
        option_b = viral_scores[0][0]

        # Option C: Best for differentiation
        diff_scores = [(i, i.scores.get("Diferenciación", 0)) for i in ideas]
        diff_scores.sort(key=lambda x: x[1], reverse=True)
        option_c = diff_scores[0][0]

        return {
            "option_a": {
                "idea": option_a,
                "rationale": "Máxima resolución del brief"
            },
            "option_b": {
                "idea": option_b,
                "rationale": "Máximo potencial viral"
            },
            "option_c": {
                "idea": option_c,
                "rationale": "Máxima diferenciación"
            }
        }

    def update_summary_file(self, project_path: Path, brand: str):
        """Update the summary file with current scores."""
        ideas_dir = project_path / "ideas"
        ideas = self.calculator.rank_ideas(ideas_dir)

        content = self.generate_summary(ideas, brand)
        summary_file = ideas_dir / "00-RESUMEN-IDEAS.md"
        summary_file.write_text(content, encoding="utf-8")

        return len(ideas)
```

---

### 5. Synthesis Module (`src/synthesis/`)

#### quick_reference.py
```python
"""Quick reference generation from research files."""

from pathlib import Path
from ..core.ai_service import AIService
from ..core.templates import TemplateEngine

class QuickReferenceGenerator:
    def __init__(self, ai_service: AIService, templates: TemplateEngine):
        self.ai = ai_service
        self.templates = templates

    async def generate(self, project_path: Path, brand: str) -> str:
        """Generate QUICK-REFERENCE.md from research files."""

        # Find research folder
        research_dir = None
        for d in project_path.iterdir():
            if d.is_dir() and d.name.startswith("investigacion-"):
                research_dir = d
                break

        if not research_dir:
            raise FileNotFoundError("Research directory not found")

        # Gather data from research files
        market_data = await self._extract_market_data(research_dir)
        target_profile = await self._extract_target(research_dir)
        insights = await self._extract_insights(research_dir)
        directions = await self._extract_directions(research_dir)

        # Generate with template
        content = self.templates.render("quick_reference.md.j2", {
            "brand": brand,
            "market_data": market_data,
            "target_profile": target_profile,
            "insights": insights,
            "directions": directions,
            "dos": await self._generate_dos(research_dir),
            "donts": await self._generate_donts(research_dir)
        })

        return content

    async def _extract_market_data(self, research_dir: Path) -> dict:
        """Extract key market metrics."""
        market_file = research_dir / "01-mercado-general" / "resumen-mercado.md"
        if not market_file.exists():
            return {}

        content = market_file.read_text(encoding="utf-8")

        prompt = f"""Extract key market metrics from this research file.
Return as JSON with these keys:
- market_size: string (e.g., "USD 832M")
- growth: string (e.g., "5.2%")
- market_share: string (e.g., "45%")
- main_competitor: string

Content:
{content}"""

        response = await self.ai.complete(prompt)
        # Parse JSON from response
        import json
        try:
            return json.loads(response)
        except:
            return {}

    async def _extract_target(self, research_dir: Path) -> dict:
        """Extract target profile."""
        consumer_dir = research_dir / "04-consumidor"
        if not consumer_dir.exists():
            return {}

        # Read all consumer files
        content = ""
        for f in consumer_dir.glob("*.md"):
            content += f.read_text(encoding="utf-8") + "\n"

        prompt = f"""Extract target audience profile from this research.
Return as JSON with these keys:
- who: string (one sentence description)
- age: string (range)
- motivation: string (main driver)
- barrier: string (main obstacle)
- media: string (where they are)

Content:
{content[:4000]}"""

        response = await self.ai.complete(prompt)
        import json
        try:
            return json.loads(response)
        except:
            return {}

    async def _extract_insights(self, research_dir: Path) -> list[dict]:
        """Extract key insights as problem-reality-opportunity."""
        # Gather all research content
        content = ""
        for md_file in research_dir.rglob("*.md"):
            if md_file.name != "fuentes-completas.md":
                content += md_file.read_text(encoding="utf-8")[:1000] + "\n"

        prompt = f"""Extract 3 key insights from this marketing research.
Each insight should have:
- problem: what the challenge is
- reality: what's actually happening
- opportunity: how to leverage it

Return as JSON array.

Content:
{content[:6000]}"""

        response = await self.ai.complete(prompt)
        import json
        try:
            return json.loads(response)
        except:
            return []

    async def _extract_directions(self, research_dir: Path) -> list[dict]:
        """Extract creative directions."""
        # Similar implementation
        pass

    async def _generate_dos(self, research_dir: Path) -> list[str]:
        """Generate list of things TO do."""
        pass

    async def _generate_donts(self, research_dir: Path) -> list[str]:
        """Generate list of things NOT to do."""
        pass

    async def save(self, project_path: Path, brand: str):
        """Generate and save quick reference file."""
        content = await self.generate(project_path, brand)

        # Find research dir and save
        for d in project_path.iterdir():
            if d.is_dir() and d.name.startswith("investigacion-"):
                qr_path = d / "QUICK-REFERENCE.md"
                qr_path.write_text(content, encoding="utf-8")
                return qr_path

        raise FileNotFoundError("Research directory not found")
```

---

### 6. CLI Module (`src/cli.py`)

```python
"""Command-line interface for Campaign Generator."""

import click
from pathlib import Path
import asyncio
from .core.config import load_config, get_config
from .core.ai_service import AIService
from .core.templates import TemplateEngine
from .generator.project import ProjectCreator
from .research.sources import SourceManager
from .research.tracker import ResearchTracker
from .scoring.calculator import ScoreCalculator
from .scoring.reports import ScoringReportGenerator
from .synthesis.quick_reference import QuickReferenceGenerator

@click.group()
@click.option('--config', '-c', type=click.Path(), help='Config file path')
@click.pass_context
def cli(ctx, config):
    """Campaign Research Generator - AI-powered campaign creation."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config) if config else get_config()

# =============================================================================
# NEW COMMAND
# =============================================================================

@cli.command()
@click.option('--brand', '-b', required=True, help='Brand name')
@click.option('--country', '-c', default='Paraguay', help='Country')
@click.option('--type', '-t', 'campaign_type', default='digital', help='Campaign type')
@click.option('--year', '-y', type=int, help='Campaign year')
@click.option('--ideas', '-i', type=int, default=25, help='Number of ideas')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.pass_context
def new(ctx, brand, country, campaign_type, year, ideas, output):
    """Create a new campaign project."""
    config = ctx.obj['config']
    templates = TemplateEngine(config.templates_dir)
    creator = ProjectCreator(templates)

    output_path = Path(output) if output else Path.cwd()

    project_path = creator.create(
        brand=brand,
        country=country,
        campaign_type=campaign_type,
        year=year,
        num_ideas=ideas,
        output_dir=output_path
    )

    click.echo(f"✅ Project created: {project_path}")
    click.echo(f"\nNext steps:")
    click.echo(f"  1. Review README.md")
    click.echo(f"  2. Import original brief")
    click.echo(f"  3. Start research in 01-mercado-general/")

# =============================================================================
# STATUS COMMAND
# =============================================================================

@cli.command()
@click.option('--project', '-p', type=click.Path(exists=True), help='Project path')
@click.pass_context
def status(ctx, project):
    """Show research progress status."""
    project_path = Path(project) if project else Path.cwd()
    tracker = ResearchTracker(project_path)

    status = tracker.get_status()

    click.echo(f"\n📊 Research Progress: {project_path.name}\n")

    for category, data in status.items():
        progress = data['progress']
        bar = '█' * int(progress / 10) + '░' * (10 - int(progress / 10))
        click.echo(f"  {category:30} {bar} {progress:3}%")

    total = sum(d['progress'] for d in status.values()) / len(status)
    click.echo(f"\n  {'Total':30} {total:.0f}%")

# =============================================================================
# SOURCE COMMANDS
# =============================================================================

@cli.group()
def source():
    """Manage research sources."""
    pass

@source.command()
@click.option('--url', required=True, help='Source URL')
@click.option('--title', required=True, help='Source title')
@click.option('--category', type=click.Choice(['media', 'corporate', 'study', 'institutional']), required=True)
@click.option('--topic', required=True, help='Topic covered')
@click.option('--project', '-p', type=click.Path(exists=True))
@click.pass_context
def add(ctx, url, title, category, topic, project):
    """Add a new source."""
    project_path = Path(project) if project else Path.cwd()
    manager = SourceManager(project_path)

    source = asyncio.run(manager.add(url, title, category, topic))

    status = "✅" if source.is_valid else "⚠️"
    click.echo(f"{status} Source added: {title}")
    if not source.is_valid:
        click.echo(f"   Warning: URL may not be accessible")

@source.command()
@click.option('--project', '-p', type=click.Path(exists=True))
def validate(project):
    """Validate all source URLs."""
    project_path = Path(project) if project else Path.cwd()
    manager = SourceManager(project_path)

    result = asyncio.run(manager.validate_all())

    click.echo(f"\n📋 Source Validation Results:\n")
    click.echo(f"  ✅ Valid: {len(result['valid'])}")
    click.echo(f"  ❌ Invalid: {len(result['invalid'])}")

    if result['invalid']:
        click.echo(f"\nInvalid URLs:")
        for source in result['invalid']:
            click.echo(f"  - {source.url}")

# =============================================================================
# SCORE COMMAND
# =============================================================================

@cli.command()
@click.option('--project', '-p', type=click.Path(exists=True))
@click.option('--update', is_flag=True, help='Update summary file')
@click.pass_context
def score(ctx, project, update):
    """Calculate and display idea scores."""
    config = ctx.obj['config']
    project_path = Path(project) if project else Path.cwd()

    calculator = ScoreCalculator(config.scoring)
    ideas_dir = project_path / "ideas"

    ideas = calculator.rank_ideas(ideas_dir)

    click.echo(f"\n📈 Idea Rankings:\n")

    for rank, idea in enumerate(ideas[:10], 1):
        medal = ["🏆", "🥇", "🥈"][rank-1] if rank <= 3 else "  "
        click.echo(f"  {medal} #{rank} {idea.idea_name:30} {idea.total}/100 {idea.tier}")

    if len(ideas) > 10:
        click.echo(f"\n  ... and {len(ideas) - 10} more ideas")

    if update:
        templates = TemplateEngine(config.templates_dir)
        reporter = ScoringReportGenerator(calculator, templates)
        # Extract brand from project name
        brand = project_path.name.split('-')[1].title()
        count = reporter.update_summary_file(project_path, brand)
        click.echo(f"\n✅ Updated 00-RESUMEN-IDEAS.md with {count} ideas")

# =============================================================================
# SYNTHESIZE COMMAND
# =============================================================================

@cli.command()
@click.option('--project', '-p', type=click.Path(exists=True))
@click.pass_context
def synthesize(ctx, project):
    """Generate quick reference from research."""
    config = ctx.obj['config']
    project_path = Path(project) if project else Path.cwd()

    ai = AIService()
    templates = TemplateEngine(config.templates_dir)
    generator = QuickReferenceGenerator(ai, templates)

    # Extract brand from project name
    brand = project_path.name.split('-')[1].title()

    qr_path = asyncio.run(generator.save(project_path, brand))

    click.echo(f"✅ Quick reference generated: {qr_path}")

# =============================================================================
# EXPORT COMMANDS
# =============================================================================

@cli.group()
def export():
    """Export to various formats."""
    pass

@export.command()
@click.option('--project', '-p', type=click.Path(exists=True))
@click.option('--top', type=int, default=10, help='Export top N ideas')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def pdf(project, top, output):
    """Export ideas to PDF."""
    from .export.pdf import PDFExporter

    project_path = Path(project) if project else Path.cwd()
    output_path = Path(output) if output else project_path / "output"
    output_path.mkdir(exist_ok=True)

    exporter = PDFExporter()
    ideas_dir = project_path / "ideas"

    exported = exporter.export_top_ideas(ideas_dir, output_path, top)

    click.echo(f"✅ Exported {exported} PDFs to {output_path}")

@export.command()
@click.option('--project', '-p', type=click.Path(exists=True))
@click.option('--template', default='pitch-deck', help='Presentation template')
@click.option('--output', '-o', type=click.Path())
def pptx(project, template, output):
    """Generate PowerPoint presentation."""
    from .export.presentation import PresentationGenerator

    project_path = Path(project) if project else Path.cwd()
    output_path = Path(output) if output else project_path / "output"

    generator = PresentationGenerator()
    pptx_path = generator.generate(project_path, output_path, template)

    click.echo(f"✅ Presentation generated: {pptx_path}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    cli(obj={})

if __name__ == '__main__':
    main()
```

---

## AI Integration Strategy

### Provider Configuration

```yaml
# config/default.yaml

ai:
  primary_provider: anthropic
  fallback_provider: openai

  anthropic:
    model: claude-sonnet-4-20250514
    max_tokens: 4096
    temperature: 0.7

  openai:
    model: gpt-4-turbo
    max_tokens: 4096
    temperature: 0.7
```

### Prompt Library

Store prompts in `config/prompts/`:

#### research_summary.txt
```
You are a marketing research analyst specializing in Latin American markets.

Summarize the following content for a campaign research project:

{content}

Focus on:
1. Key statistics and data points
2. Market insights relevant to advertising
3. Consumer behavior patterns
4. Competitive positioning opportunities

Provide your summary in Spanish, using professional marketing terminology.
Maximum length: {max_length} characters.
```

#### brief_analysis.txt
```
You are a creative strategist analyzing a campaign brief.

Brief content:
{brief}

Extract and structure the following:

1. CORE CHALLENGE
   - Main problem to solve
   - Key constraints

2. TARGET AUDIENCE
   - Demographics
   - Psychographics
   - Media consumption

3. BRAND REQUIREMENTS
   - Tone of voice
   - Visual guidelines
   - Restrictions

4. SUCCESS METRICS
   - KPIs
   - Goals

5. CREATIVE OPPORTUNITIES
   - 3 potential directions
   - Each with rationale

Output in Spanish with clear headers and bullet points.
```

#### idea_generation.txt
```
You are a creative director generating campaign concepts.

Based on this research:
{research_summary}

And this brief:
{brief_summary}

Generate {num_ideas} campaign ideas. For each idea:

1. NAME: Catchy, memorable title
2. CONCEPT: One-sentence description
3. INSIGHT: The human truth it builds on
4. EXECUTION: How it would look/feel
5. WHY IT WORKS: 3 reasons connected to brief/research

Ideas should be:
- Culturally relevant to {country}
- Aligned with brand voice
- Feasible to execute
- Differentiated from competition

Output in Spanish.
```

### Usage Patterns

```python
# Example: AI-assisted brief analysis
async def analyze_brief(brief_content: str) -> dict:
    ai = AIService()

    # Load prompt template
    prompt_template = load_prompt("brief_analysis.txt")
    prompt = prompt_template.format(brief=brief_content)

    # Get analysis
    response = await ai.complete(
        prompt=prompt,
        system="You are a senior creative strategist."
    )

    # Parse structured response
    return parse_analysis(response)
```

---

## Data Models

### Project Model

```python
@dataclass
class Project:
    name: str
    brand: str
    country: str
    campaign_type: str
    year: int
    path: Path
    created_at: datetime

    @property
    def research_path(self) -> Path:
        return self.path / f"investigacion-{self.brand.lower()}-{self.country.lower()}"

    @property
    def ideas_path(self) -> Path:
        return self.path / "ideas"
```

### Idea Model

```python
@dataclass
class Idea:
    number: int
    name: str
    concept: str
    insight: str
    executions: list[Execution]
    tone: list[str]
    reasons: list[str]
    scores: dict[str, int]
    total_score: int
    tier: str
    variants: list[str]

@dataclass
class Execution:
    name: str
    visual: str
    copy: str
```

### Source Model

```python
@dataclass
class Source:
    url: str
    title: str
    category: str
    topic: str
    date_accessed: datetime
    is_valid: bool
    summary: Optional[str]
```

---

## Testing Strategy

### Test Structure

```python
# tests/conftest.py

import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_project():
    """Create a temporary project for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "campana-test-2025"
        project_path.mkdir()

        # Create minimal structure
        (project_path / "ideas").mkdir()
        (project_path / "investigacion-test-paraguay").mkdir()

        yield project_path

@pytest.fixture
def sample_idea_file(temp_project):
    """Create a sample idea file."""
    idea_content = '''# Idea 01: "Test Idea"

## Concepto Central
Test concept

## Puntuación
| Criterio | Puntaje |
|----------|---------|
| Diferenciación | 8/10 |
| Autenticidad | 7/10 |
'''
    idea_path = temp_project / "ideas" / "idea-01-test.md"
    idea_path.write_text(idea_content)
    return idea_path

@pytest.fixture
def mock_ai_service(mocker):
    """Mock AI service for testing."""
    mock = mocker.patch('src.core.ai_service.AIService')
    mock.return_value.complete.return_value = "Mocked response"
    return mock
```

### Test Examples

```python
# tests/test_scoring.py

def test_calculate_total_score():
    calculator = ScoreCalculator({})
    scores = {
        "Diferenciación": 8,
        "Autenticidad": 7,
        "Potencial Viral": 9
    }
    total = calculator.calculate_total(scores)
    assert total == 24

def test_get_tier_very_high():
    calculator = ScoreCalculator({
        "thresholds": {"very_high": 90}
    })
    tier = calculator.get_tier(95)
    assert "MUY ALTO" in tier

def test_parse_idea_file(sample_idea_file):
    calculator = ScoreCalculator({})
    idea = calculator.parse_idea_file(sample_idea_file)

    assert idea.idea_number == 1
    assert idea.idea_name == "Test Idea"
    assert idea.scores["Diferenciación"] == 8

# tests/test_research.py

@pytest.mark.asyncio
async def test_add_source(temp_project):
    manager = SourceManager(temp_project)

    source = await manager.add(
        url="https://example.com",
        title="Test Source",
        category="media",
        topic="test"
    )

    assert source.title == "Test Source"
    assert source.category == "media"

@pytest.mark.asyncio
async def test_validate_urls(temp_project, httpx_mock):
    httpx_mock.add_response(status_code=200)

    manager = SourceManager(temp_project)
    await manager.add("https://example.com", "Test", "media", "test")

    result = await manager.validate_all()
    assert len(result["valid"]) == 1
```

---

## Deployment

### Package Setup

```toml
# pyproject.toml

[project]
name = "campaign-generator"
version = "1.0.0"
description = "AI-powered campaign research generator"
authors = [{name = "Your Name"}]
requires-python = ">=3.11"

dependencies = [
    "click>=8.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.0",
    "jinja2>=3.0.0",
    "httpx>=0.24.0",
    "beautifulsoup4>=4.11.0",
    "validators>=0.20.0",
    "reportlab>=4.0.0",
    "markdown2>=2.4.0",
    "python-pptx>=0.6.21",
    "anthropic>=0.5.0",
    "openai>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-httpx>=0.22.0",
    "pytest-mock>=3.10.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "ruff>=0.0.270",
]

[project.scripts]
campaign = "src.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Environment Setup

```bash
# .env.example

# AI Providers
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Optional
LOG_LEVEL=INFO
CACHE_DIR=~/.campaign-generator/cache
```

### Installation

```bash
# Development install
pip install -e ".[dev]"

# Production install
pip install campaign-generator

# Or with pipx
pipx install campaign-generator
```

### Usage After Install

```bash
# Set up API keys
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# Create new project
campaign new --brand "Nike" --country "Argentina"

# Check status
campaign status -p campana-nike-2025

# Add sources
campaign source add --url "https://..." --title "Article" --category media --topic "market"

# Calculate scores
campaign score -p campana-nike-2025 --update

# Generate quick reference
campaign synthesize -p campana-nike-2025

# Export
campaign export pdf -p campana-nike-2025 --top 10
campaign export pptx -p campana-nike-2025
```

---

## Development Phases - Detailed Timeline

### Phase 1: Core Infrastructure (Week 1)

**Day 1-2: Project Setup**
- [ ] Initialize pyproject.toml
- [ ] Set up directory structure
- [ ] Configure linting (ruff, black, mypy)
- [ ] Set up pytest

**Day 3-4: Core Services**
- [ ] Implement config.py with Pydantic
- [ ] Implement templates.py with Jinja2
- [ ] Implement ai_service.py with both providers
- [ ] Write tests for core services

**Day 5: CLI Foundation**
- [ ] Set up Click CLI structure
- [ ] Implement `new` command
- [ ] Migrate existing generator code
- [ ] Test project creation

### Phase 2: Research Tools (Week 2)

**Day 1-2: Source Management**
- [ ] Implement sources.py
- [ ] Add URL validation
- [ ] Implement source CRUD
- [ ] Generate fuentes-completas.md

**Day 3-4: Research Tracking**
- [ ] Implement tracker.py
- [ ] Progress calculation per folder
- [ ] Status command
- [ ] Visual progress bars

**Day 5: AI Summarization**
- [ ] Implement summarizer.py
- [ ] URL content extraction
- [ ] Insight extraction
- [ ] Test with real URLs

### Phase 3: Scoring System (Week 3)

**Day 1-2: Score Calculator**
- [ ] Implement calculator.py
- [ ] Parse idea files
- [ ] Calculate weighted totals
- [ ] Tier classification

**Day 3-4: Reports**
- [ ] Implement reports.py
- [ ] Generate ranking tables
- [ ] Create recommendations
- [ ] Update summary files

**Day 5: CLI Integration**
- [ ] Implement `score` command
- [ ] Add `--update` flag
- [ ] Test full workflow

### Phase 4: Synthesis (Week 4)

**Day 1-2: Quick Reference**
- [ ] Implement quick_reference.py
- [ ] AI extraction of key data
- [ ] Template rendering
- [ ] Save to file

**Day 3-4: Brief Analyzer**
- [ ] Implement brief_analyzer.py
- [ ] Parse PDF briefs
- [ ] Extract structured data
- [ ] Generate expanded brief

**Day 5: Cross-References**
- [ ] Implement cross_reference.py
- [ ] Validate internal links
- [ ] Generate indexes
- [ ] Check consistency

### Phase 5: Export (Week 5)

**Day 1-2: PDF Export**
- [ ] Improve existing PDF code
- [ ] Styled templates
- [ ] Batch export
- [ ] Cover pages

**Day 3-4: Presentations**
- [ ] Implement presentation.py
- [ ] Slide templates
- [ ] Auto-populate content
- [ ] Export to PPTX

**Day 5: Executive Reports**
- [ ] One-page summaries
- [ ] Research reports
- [ ] Competitive analysis

### Phase 6: Polish (Week 6)

**Day 1-2: Testing**
- [ ] Unit tests for all modules
- [ ] Integration tests
- [ ] 80%+ coverage

**Day 3-4: Documentation**
- [ ] README with examples
- [ ] API documentation
- [ ] User guide

**Day 5: Release**
- [ ] Final testing
- [ ] Version tagging
- [ ] Package publishing

---

## Next Immediate Steps

1. **Create `pyproject.toml`** with all dependencies
2. **Set up `src/` structure** with `__init__.py` files
3. **Implement `config.py`** with Pydantic models
4. **Implement `ai_service.py`** with Anthropic + OpenAI
5. **Create basic CLI** with `new` command working

Ready to start coding?
