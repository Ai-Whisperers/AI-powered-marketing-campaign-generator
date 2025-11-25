# System Architecture & Data Flow

Complete technical architecture for the Campaign Research Generator using the hybrid n8n + Python approach.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow Diagrams](#data-flow-diagrams)
4. [n8n Workflow Designs](#n8n-workflow-designs)
5. [Python API Design](#python-api-design)
6. [Data Models](#data-models)
7. [File System Structure](#file-system-structure)
8. [Integration Points](#integration-points)
9. [Error Handling Strategy](#error-handling-strategy)
10. [Deployment Architecture](#deployment-architecture)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │  n8n Web UI  │    │   Webhooks   │    │  CLI (opt)   │     │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
└──────────┼───────────────────┼───────────────────┼─────────────┘
           │                   │                   │
           ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      n8n WORKFLOW ENGINE                        │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Campaign   │  │  Research   │  │   Export    │   ...        │
│  │  Workflows  │  │  Workflows  │  │  Workflows  │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
└─────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Claude AI  │  │  OpenAI     │  │  Web URLs   │              │
│  │  (Anthropic)│  │  (Fallback) │  │  (Scraping) │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PYTHON API (FastAPI)                       │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Generator  │  │  Scoring    │  │   Export    │              │
│  │  Endpoints  │  │  Endpoints  │  │  Endpoints  │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
└─────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FILE SYSTEM STORAGE                        │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Projects   │  │  Templates  │  │   Config    │              │
│  │  (Markdown) │  │  (Jinja2)   │  │   (YAML)    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| n8n Workflows | Orchestration, AI calls, routing, error handling |
| Python API | Complex logic, file operations, templates, calculations |
| Claude AI | Content analysis, summarization, generation |
| OpenAI | Fallback AI provider |
| File System | Persistent storage for all project data |

---

## Component Architecture

### n8n Workflows Layer

```
┌─────────────────────────────────────────────────────────┐
│                    n8n Workflows                         │
│                                                          │
│  Campaign Workflows                                      │
│  ├── WF-001: Create New Project                         │
│  ├── WF-002: Import Brief                               │
│  └── WF-003: Delete Project                             │
│                                                          │
│  Research Workflows                                      │
│  ├── WF-101: Add Source                                 │
│  ├── WF-102: Summarize URL                              │
│  ├── WF-103: Validate Sources                           │
│  └── WF-104: Check Progress                             │
│                                                          │
│  AI Workflows                                            │
│  ├── WF-201: Analyze Brief                              │
│  ├── WF-202: Generate Ideas                             │
│  └── WF-203: Generate Quick Reference                   │
│                                                          │
│  Scoring Workflows                                       │
│  ├── WF-301: Calculate Scores                           │
│  └── WF-302: Generate Ranking Report                    │
│                                                          │
│  Export Workflows                                        │
│  ├── WF-401: Export PDF                                 │
│  └── WF-402: Export PPTX                                │
└─────────────────────────────────────────────────────────┘
```

### Python API Layer

```
┌─────────────────────────────────────────────────────────┐
│                    Python FastAPI                        │
│                                                          │
│  Core Services                                           │
│  ├── config.py          # Configuration management       │
│  ├── templates.py       # Jinja2 rendering               │
│  └── exceptions.py      # Custom exceptions              │
│                                                          │
│  API Endpoints                                           │
│  ├── /api/projects/*    # Project CRUD                  │
│  ├── /api/sources/*     # Source management             │
│  ├── /api/scoring/*     # Score calculation             │
│  ├── /api/synthesis/*   # Content synthesis             │
│  └── /api/export/*      # PDF/PPTX generation           │
│                                                          │
│  Domain Logic                                            │
│  ├── generator/         # Project structure creation    │
│  ├── scoring/           # Score algorithms              │
│  ├── synthesis/         # Content compilation           │
│  └── export/            # Document generation           │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Flow 1: Create New Project

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│   n8n   │     │   n8n   │     │ Python  │     │  File   │
│ Trigger │────▶│Workflow │────▶│   API   │────▶│ System  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     │ brand,        │ HTTP POST     │ Create        │
     │ country,      │ /api/projects │ folders &     │
     │ type          │               │ templates     │
     │               │               │               │
     ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. User triggers workflow (manual/webhook)             │
│  2. n8n sets parameters (brand, country, type)          │
│  3. n8n calls Python API POST /api/projects             │
│  4. Python creates folder structure                     │
│  5. Python renders Jinja2 templates                     │
│  6. Python writes all files                             │
│  7. Python returns project path                         │
│  8. n8n returns success response                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Flow 2: Add Source with AI Summary

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│Webhook  │     │  Fetch  │     │ Claude  │     │ Python  │     │  File   │
│Trigger  │────▶│   URL   │────▶│   AI    │────▶│   API   │────▶│ System  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │               │
     │ url,          │ HTML          │ Summary       │ Formatted     │
     │ title,        │ content       │ in Spanish    │ citation      │
     │ category      │               │               │               │
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  1. Webhook receives: url, title, category, topic                   │
│  2. n8n HTTP Request fetches URL content                            │
│  3. n8n Claude node summarizes for marketing research               │
│  4. n8n calls Python API POST /api/sources with summary             │
│  5. Python validates URL, formats citation                          │
│  6. Python updates fuentes-completas.md                             │
│  7. Python returns formatted source                                 │
│  8. n8n returns confirmation                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Flow 3: Brief Analysis with AI

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│Webhook  │     │  Read   │     │ Claude  │     │ Python  │
│Trigger  │────▶│  File   │────▶│   AI    │────▶│   API   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     │ project       │ Brief         │ Structured    │ BRIEF-CAMPANA
     │ path          │ content       │ analysis      │ .md created
     │               │               │               │
     ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Webhook receives project path                       │
│  2. n8n reads brief file from project                   │
│  3. n8n Claude extracts: challenge, target, brand, KPIs │
│  4. n8n Claude suggests creative directions             │
│  5. n8n calls Python API POST /api/synthesis/brief      │
│  6. Python renders BRIEF-CAMPANA.md template            │
│  7. Python writes file to project                       │
│  8. n8n returns analysis summary                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Flow 4: Score Calculation

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│Webhook  │     │ Python  │     │  File   │
│Trigger  │────▶│   API   │────▶│ System  │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     │ project       │ Parse, calc,  │ Update
     │ path          │ rank          │ RESUMEN
     │               │               │
     ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Webhook receives project path                       │
│  2. n8n calls Python API POST /api/scoring/calculate    │
│  3. Python reads all idea-*.md files                    │
│  4. Python parses scoring tables                        │
│  5. Python calculates weighted totals                   │
│  6. Python classifies into tiers                        │
│  7. Python generates ranking                            │
│  8. Python updates 00-RESUMEN-IDEAS.md                  │
│  9. n8n returns ranking data                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Flow 5: Quick Reference Generation

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│Webhook  │────▶│ Python  │────▶│ Claude  │────▶│  File   │
│Trigger  │     │   API   │     │   AI    │     │ System  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     │ project       │ Read all      │ Extract       │ QUICK-
     │ path          │ research      │ key data      │ REFERENCE.md
     │               │               │               │
     ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Webhook receives project path                       │
│  2. n8n calls Python API GET /api/projects/{id}/research│
│  3. Python reads all research files, returns content    │
│  4. n8n Claude extracts market data from content        │
│  5. n8n Claude extracts target profile                  │
│  6. n8n Claude generates insights, dos/donts            │
│  7. n8n calls Python POST /api/synthesis/quick-reference│
│  8. Python renders template with AI data                │
│  9. Python writes QUICK-REFERENCE.md                    │
│  10. n8n returns success                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## n8n Workflow Designs

### WF-001: Create New Project

```yaml
name: "Create New Project"
trigger: Webhook
nodes:
  - type: Webhook
    path: /create-project
    method: POST

  - type: Set
    name: Set Parameters
    values:
      brand: "={{ $json.brand }}"
      country: "={{ $json.country || 'Paraguay' }}"
      campaign_type: "={{ $json.type || 'digital' }}"
      year: "={{ $json.year || new Date().getFullYear() }}"
      num_ideas: "={{ $json.ideas || 25 }}"

  - type: HTTP Request
    name: Create Project
    method: POST
    url: "{{ $env.PYTHON_API_URL }}/api/projects"
    body:
      brand: "={{ $node['Set Parameters'].json.brand }}"
      country: "={{ $node['Set Parameters'].json.country }}"
      campaign_type: "={{ $node['Set Parameters'].json.campaign_type }}"
      year: "={{ $node['Set Parameters'].json.year }}"
      num_ideas: "={{ $node['Set Parameters'].json.num_ideas }}"

  - type: Respond to Webhook
    response:
      status: "success"
      project_path: "={{ $json.project_path }}"
      message: "Project created successfully"
```

### WF-101: Add Source with Summary

```yaml
name: "Add Source"
trigger: Webhook
nodes:
  - type: Webhook
    path: /add-source
    method: POST

  - type: HTTP Request
    name: Fetch URL
    method: GET
    url: "={{ $json.url }}"
    options:
      response: text

  - type: Claude
    name: Summarize Content
    model: claude-sonnet-4-20250514
    prompt: |
      Summarize this content for marketing research in Spanish.
      Focus on: statistics, market data, consumer insights, competitive info.
      Maximum 500 characters.

      Content:
      {{ $node['Fetch URL'].json.data }}

  - type: HTTP Request
    name: Save Source
    method: POST
    url: "{{ $env.PYTHON_API_URL }}/api/sources"
    body:
      project: "={{ $json.project }}"
      url: "={{ $json.url }}"
      title: "={{ $json.title }}"
      category: "={{ $json.category }}"
      topic: "={{ $json.topic }}"
      summary: "={{ $node['Summarize Content'].json.content }}"

  - type: Respond to Webhook
    response:
      status: "success"
      source: "={{ $json }}"
```

### WF-201: Analyze Brief

```yaml
name: "Analyze Brief"
trigger: Webhook
nodes:
  - type: Webhook
    path: /analyze-brief
    method: POST

  - type: HTTP Request
    name: Get Brief Content
    method: GET
    url: "{{ $env.PYTHON_API_URL }}/api/projects/{{ $json.project }}/brief"

  - type: Claude
    name: Extract Challenge
    prompt: |
      Extract the core challenge from this campaign brief.
      Return JSON: {"main": "...", "constraints": ["..."]}

      Brief:
      {{ $node['Get Brief Content'].json.content }}

  - type: Claude
    name: Extract Target
    prompt: |
      Extract target audience details from this brief.
      Return JSON with demographics, psychographics, media_consumption.

      Brief:
      {{ $node['Get Brief Content'].json.content }}

  - type: Claude
    name: Suggest Directions
    prompt: |
      Suggest 3 creative directions based on this brief.
      Return JSON array: [{"name": "...", "description": "...", "rationale": "..."}]

      Brief:
      {{ $node['Get Brief Content'].json.content }}

  - type: Merge
    name: Combine Analysis

  - type: HTTP Request
    name: Save Brief Analysis
    method: POST
    url: "{{ $env.PYTHON_API_URL }}/api/synthesis/brief"
    body:
      project: "={{ $json.project }}"
      challenge: "={{ $node['Extract Challenge'].json }}"
      target: "={{ $node['Extract Target'].json }}"
      directions: "={{ $node['Suggest Directions'].json }}"

  - type: Respond to Webhook
    response:
      status: "success"
      analysis: "={{ $json }}"
```

### WF-301: Calculate Scores

```yaml
name: "Calculate Scores"
trigger: Webhook
nodes:
  - type: Webhook
    path: /calculate-scores
    method: POST

  - type: HTTP Request
    name: Calculate
    method: POST
    url: "{{ $env.PYTHON_API_URL }}/api/scoring/calculate"
    body:
      project: "={{ $json.project }}"
      update_summary: true

  - type: Code
    name: Format Results
    code: |
      const rankings = $input.first().json.rankings;
      const top10 = rankings.slice(0, 10).map((idea, i) => ({
        rank: i + 1,
        name: idea.name,
        score: idea.total,
        tier: idea.tier
      }));
      return [{ json: { top10, total: rankings.length } }];

  - type: Respond to Webhook
    response:
      status: "success"
      rankings: "={{ $json.top10 }}"
      total_ideas: "={{ $json.total }}"
```

---

## Python API Design

### Endpoint Structure

```
/api
├── /projects
│   ├── POST /                    # Create project
│   ├── GET /{id}                 # Get project info
│   ├── DELETE /{id}              # Delete project
│   ├── GET /{id}/brief           # Get brief content
│   └── GET /{id}/research        # Get all research content
│
├── /sources
│   ├── POST /                    # Add source
│   ├── GET /{project}            # List sources
│   ├── PUT /{project}/{id}       # Update source
│   ├── DELETE /{project}/{id}    # Delete source
│   └── POST /{project}/validate  # Validate all sources
│
├── /scoring
│   ├── POST /calculate           # Calculate scores
│   └── GET /{project}/rankings   # Get rankings
│
├── /synthesis
│   ├── POST /brief               # Generate brief analysis
│   ├── POST /quick-reference     # Generate QR
│   └── POST /indexes             # Generate indexes
│
└── /export
    ├── POST /pdf                 # Export to PDF
    └── POST /pptx                # Export to PPTX
```

### API Implementation

```python
# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os

app = FastAPI(title="Campaign Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECTS_DIR = Path(os.getenv("PROJECTS_DIR", "./projects"))

# =============================================================================
# MODELS
# =============================================================================

class ProjectCreate(BaseModel):
    brand: str
    country: str = "Paraguay"
    campaign_type: str = "digital"
    year: int = 2025
    num_ideas: int = 25

class SourceCreate(BaseModel):
    project: str
    url: str
    title: str
    category: str
    topic: str
    summary: str = None

class ScoreRequest(BaseModel):
    project: str
    update_summary: bool = True

class BriefAnalysis(BaseModel):
    project: str
    challenge: dict
    target: dict
    directions: list

class QuickReferenceData(BaseModel):
    project: str
    market_data: dict
    target_profile: dict
    insights: list
    directions: list
    dos: list
    donts: list

class ExportRequest(BaseModel):
    project: str
    format: str = "pdf"
    top_n: int = 10

# =============================================================================
# PROJECT ENDPOINTS
# =============================================================================

@app.post("/api/projects")
async def create_project(data: ProjectCreate):
    """Create a new campaign project."""
    from services.generator import ProjectCreator

    creator = ProjectCreator()
    project_path = creator.create(
        brand=data.brand,
        country=data.country,
        campaign_type=data.campaign_type,
        year=data.year,
        num_ideas=data.num_ideas,
        output_dir=PROJECTS_DIR
    )

    return {
        "project_path": str(project_path),
        "project_id": project_path.name
    }

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get project information."""
    project_path = PROJECTS_DIR / project_id

    if not project_path.exists():
        raise HTTPException(404, "Project not found")

    return {
        "id": project_id,
        "path": str(project_path),
        "files": len(list(project_path.rglob("*.md"))),
        "ideas": len(list((project_path / "ideas").glob("idea-*.md")))
    }

@app.get("/api/projects/{project_id}/brief")
async def get_brief(project_id: str):
    """Get brief content."""
    project_path = PROJECTS_DIR / project_id

    # Find brief file
    for brief_path in project_path.rglob("*BRIEF*.md"):
        return {"content": brief_path.read_text(encoding="utf-8")}

    raise HTTPException(404, "Brief not found")

@app.get("/api/projects/{project_id}/research")
async def get_research(project_id: str):
    """Get all research content compiled."""
    project_path = PROJECTS_DIR / project_id

    content = ""
    for research_dir in project_path.iterdir():
        if research_dir.is_dir() and research_dir.name.startswith("investigacion-"):
            for md_file in research_dir.rglob("*.md"):
                content += f"\n\n## {md_file.stem}\n\n"
                content += md_file.read_text(encoding="utf-8")[:2000]

    return {"content": content}

# =============================================================================
# SOURCE ENDPOINTS
# =============================================================================

@app.post("/api/sources")
async def add_source(data: SourceCreate):
    """Add a new research source."""
    from services.research import SourceManager

    project_path = PROJECTS_DIR / data.project
    manager = SourceManager(project_path)

    source = await manager.add(
        url=data.url,
        title=data.title,
        category=data.category,
        topic=data.topic,
        summary=data.summary
    )

    return {
        "id": source.id,
        "formatted": source.to_markdown(),
        "is_valid": source.is_valid
    }

@app.post("/api/sources/{project}/validate")
async def validate_sources(project: str):
    """Validate all sources in project."""
    from services.research import SourceManager

    project_path = PROJECTS_DIR / project
    manager = SourceManager(project_path)

    result = await manager.validate_all()

    return {
        "valid": len(result["valid"]),
        "invalid": len(result["invalid"]),
        "invalid_urls": [s.url for s in result["invalid"]]
    }

# =============================================================================
# SCORING ENDPOINTS
# =============================================================================

@app.post("/api/scoring/calculate")
async def calculate_scores(data: ScoreRequest):
    """Calculate scores and generate rankings."""
    from services.scoring import ScoreCalculator, ReportGenerator

    project_path = PROJECTS_DIR / data.project
    ideas_dir = project_path / "ideas"

    calculator = ScoreCalculator()
    rankings = calculator.rank_ideas(ideas_dir)

    if data.update_summary:
        reporter = ReportGenerator(calculator)
        brand = data.project.split("-")[1].title()
        reporter.update_summary(project_path, brand)

    return {
        "rankings": [
            {
                "number": idea.idea_number,
                "name": idea.idea_name,
                "total": idea.total,
                "tier": idea.tier,
                "scores": idea.scores
            }
            for idea in rankings
        ]
    }

# =============================================================================
# SYNTHESIS ENDPOINTS
# =============================================================================

@app.post("/api/synthesis/brief")
async def generate_brief_analysis(data: BriefAnalysis):
    """Generate BRIEF-CAMPANA.md from AI analysis."""
    from services.synthesis import BriefGenerator

    project_path = PROJECTS_DIR / data.project
    generator = BriefGenerator()

    file_path = generator.generate(
        project_path=project_path,
        challenge=data.challenge,
        target=data.target,
        directions=data.directions
    )

    return {"file": str(file_path)}

@app.post("/api/synthesis/quick-reference")
async def generate_quick_reference(data: QuickReferenceData):
    """Generate QUICK-REFERENCE.md from AI-extracted data."""
    from services.synthesis import QuickReferenceGenerator

    project_path = PROJECTS_DIR / data.project
    generator = QuickReferenceGenerator()

    file_path = generator.generate(
        project_path=project_path,
        market_data=data.market_data,
        target_profile=data.target_profile,
        insights=data.insights,
        directions=data.directions,
        dos=data.dos,
        donts=data.donts
    )

    return {"file": str(file_path)}

# =============================================================================
# EXPORT ENDPOINTS
# =============================================================================

@app.post("/api/export/pdf")
async def export_pdf(data: ExportRequest):
    """Export ideas to PDF."""
    from services.export import PDFExporter

    project_path = PROJECTS_DIR / data.project
    exporter = PDFExporter()

    output_path = project_path / "output"
    output_path.mkdir(exist_ok=True)

    files = exporter.export_top_ideas(
        ideas_dir=project_path / "ideas",
        output_dir=output_path,
        top_n=data.top_n
    )

    return {"files": [str(f) for f in files]}

@app.post("/api/export/pptx")
async def export_pptx(data: ExportRequest):
    """Export to PowerPoint."""
    from services.export import PresentationGenerator

    project_path = PROJECTS_DIR / data.project
    generator = PresentationGenerator()

    output_path = project_path / "output"
    output_path.mkdir(exist_ok=True)

    file_path = generator.generate(
        project_path=project_path,
        output_dir=output_path
    )

    return {"file": str(file_path)}

# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## Data Models

### Project Model

```python
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class Project:
    id: str
    brand: str
    country: str
    campaign_type: str
    year: int
    path: Path
    created_at: datetime

    @property
    def research_path(self) -> Path:
        for d in self.path.iterdir():
            if d.name.startswith("investigacion-"):
                return d
        return None

    @property
    def ideas_path(self) -> Path:
        return self.path / "ideas"
```

### Source Model

```python
@dataclass
class Source:
    id: str
    url: str
    title: str
    category: str  # media, corporate, study, institutional
    topic: str
    date_accessed: datetime
    is_valid: bool = True
    summary: str = None

    def to_markdown(self) -> str:
        return f"- [{self.title}]({self.url}) - {self.topic} ({self.date_accessed.year})"
```

### Idea Score Model

```python
@dataclass
class IdeaScore:
    idea_number: int
    idea_name: str
    scores: dict[str, int]
    total: int
    tier: str
    file_path: Path
```

---

## File System Structure

### Project Layout

```
projects/
└── campana-{brand}-{year}/
    ├── README.md
    ├── investigacion-{brand}-{country}/
    │   ├── README.md
    │   ├── 01-mercado-general/
    │   │   ├── resumen-mercado.md
    │   │   └── tendencias.md
    │   ├── 02-marca/
    │   ├── 03-competencia/
    │   ├── 04-consumidor/
    │   ├── 05-cultura/
    │   ├── 06-tendencias/
    │   ├── 07-estadisticas/
    │   ├── 08-referencias/
    │   │   └── fuentes-completas.md
    │   ├── 09-nuevos-hallazgos/
    │   ├── 10-investigacion-creativa/
    │   ├── BRIEF-CAMPANA.md
    │   └── QUICK-REFERENCE.md
    ├── ideas/
    │   ├── 00-RESUMEN-IDEAS.md
    │   ├── idea-01-nombre.md
    │   ├── idea-02-nombre.md
    │   └── ...
    └── output/
        ├── ideas/
        │   └── *.pdf
        └── presentation.pptx
```

---

## Integration Points

### n8n ↔ Python API

| n8n Action | Python Endpoint | Data Exchanged |
|------------|-----------------|----------------|
| Create project | POST /api/projects | brand, country, type → path |
| Add source | POST /api/sources | url, title, summary → formatted |
| Calculate scores | POST /api/scoring/calculate | project → rankings |
| Generate QR | POST /api/synthesis/quick-reference | extracted data → file path |
| Export PDF | POST /api/export/pdf | project, top_n → file paths |

### n8n ↔ Claude AI

| n8n Action | Claude Purpose | Prompt Type |
|------------|----------------|-------------|
| Summarize URL | Marketing research summary | Content extraction |
| Analyze brief | Extract challenge, target, directions | Structured extraction |
| Generate QR | Extract market data, insights | Data synthesis |
| Assist ideas | Generate starting concepts | Creative generation |

### Python ↔ File System

| Python Action | File Operation |
|---------------|----------------|
| Create project | mkdir, write templates |
| Add source | append to fuentes-completas.md |
| Calculate scores | read all idea-*.md, parse tables |
| Generate reports | render template, write file |
| Export PDF | read markdown, generate PDF |

---

## Error Handling Strategy

### n8n Level

```yaml
error_handling:
  - type: Retry
    max_attempts: 3
    wait_between: 5000

  - type: Error Workflow
    workflow: "Error Handler"

  - type: Continue on Fail
    output_on_fail: true
```

### Python API Level

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__
        }
    )

class ProjectNotFoundError(HTTPException):
    def __init__(self, project_id: str):
        super().__init__(
            status_code=404,
            detail=f"Project not found: {project_id}"
        )

class ScoringError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=f"Scoring error: {message}"
        )
```

### Error Categories

| Category | Example | Handling |
|----------|---------|----------|
| Not Found | Project doesn't exist | 404, clear message |
| Validation | Invalid URL format | 400, show what's wrong |
| AI Error | Claude rate limit | Retry, fallback to OpenAI |
| File Error | Permission denied | 500, log full error |
| Parse Error | Malformed markdown | 400, show line number |

---

## Deployment Architecture

### Development

```
┌─────────────────┐     ┌─────────────────┐
│   n8n Desktop   │────▶│  Python Local   │
│   localhost:5678│     │  localhost:8000 │
└─────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│           Local File System             │
│         ~/projects/campaigns            │
└─────────────────────────────────────────┘
```

### Production (Self-Hosted)

```
┌─────────────────┐     ┌─────────────────┐
│   n8n Docker    │────▶│  Python Docker  │
│   :5678         │     │  :8000          │
└─────────────────┘     └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│         Docker Volume / NAS             │
│           /data/campaigns               │
└─────────────────────────────────────────┘
```

### Docker Compose

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - PYTHON_API_URL=http://api:8000
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - api

  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - PROJECTS_DIR=/data/projects
    volumes:
      - projects:/data/projects
      - templates:/app/templates

volumes:
  n8n_data:
  projects:
  templates:
```

---

## Next: Preparation Checklist

The next document will cover everything you need to prepare before starting development.
