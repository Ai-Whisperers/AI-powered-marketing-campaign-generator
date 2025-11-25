# Project Roadmap & Milestones

Detailed timeline with specific deliverables for each phase of development.

---

## Overview

**Total Duration**: 6 weeks to v1.0
**Work Style**: Can be parallelized with n8n and Python work

```
Week 0: Preparation     ████████████████████ 100%
Week 1: Foundation      ░░░░░░░░░░░░░░░░░░░░   0%
Week 2: Generator       ░░░░░░░░░░░░░░░░░░░░   0%
Week 3: Research        ░░░░░░░░░░░░░░░░░░░░   0%
Week 4: Scoring         ░░░░░░░░░░░░░░░░░░░░   0%
Week 5: Synthesis       ░░░░░░░░░░░░░░░░░░░░   0%
Week 6: Export & Polish ░░░░░░░░░░░░░░░░░░░░   0%
```

---

## Week 0: Preparation (Current)

### Milestone: Development Environment Ready

**Duration**: 2-3 days

**Deliverables**:
- [x] Documentation complete (01-07)
- [ ] Python environment configured
- [ ] n8n installed and running
- [ ] API keys obtained and tested
- [ ] Directory structure created
- [ ] Config files in place
- [ ] Test fixtures ready

**Exit Criteria**:
- `uvicorn main:app` starts without errors
- n8n accessible at localhost:5678
- Claude API responds to test call
- Sample project exists for testing

**Tasks**:

```
Day 0.1: Environment
- [ ] Create virtual environment
- [ ] Install all dependencies
- [ ] Set up VS Code
- [ ] Install n8n

Day 0.2: Configuration
- [ ] Create .env with API keys
- [ ] Create default.yaml
- [ ] Create docker-compose.yml
- [ ] Set up .gitignore

Day 0.3: Foundation Files
- [ ] Create all __init__.py
- [ ] Create exceptions.py
- [ ] Create logging_config.py
- [ ] Create sample project fixture
- [ ] Create Jinja2 templates
- [ ] Create AI prompts
```

---

## Week 1: Foundation

### Milestone: API Skeleton + First Workflow

**Duration**: 5 days

**Deliverables**:
- FastAPI app with health check
- Configuration loading
- First n8n workflow (Create Project)
- Basic error handling
- First passing test

**Exit Criteria**:
- POST /api/projects creates project folder
- n8n workflow triggers successfully
- Logs show proper formatting
- pytest passes

**Tasks**:

```
Day 1.1: FastAPI Setup
- [ ] Create main.py with FastAPI app
- [ ] Add CORS middleware
- [ ] Create /health endpoint
- [ ] Create /health/detailed endpoint
- [ ] Test with curl

Day 1.2: Configuration
- [ ] Implement config.py with Pydantic
- [ ] Load default.yaml
- [ ] Environment variable override
- [ ] Test configuration loading

Day 1.3: Logging & Errors
- [ ] Set up logging configuration
- [ ] Create all exception classes
- [ ] Add global exception handler
- [ ] Test error responses

Day 1.4: First Endpoint
- [ ] Create POST /api/projects endpoint
- [ ] Implement ProjectCreator service (basic)
- [ ] Create project folder only (no templates yet)
- [ ] Test with curl/Postman

Day 1.5: First Workflow
- [ ] Create WF-001 in n8n
- [ ] Webhook trigger
- [ ] Call Python API
- [ ] Return result
- [ ] Test end-to-end
```

**Code to Write**:
```
code/api/
├── main.py           # FastAPI app
├── config.py         # Configuration
├── exceptions.py     # Custom exceptions
├── logging_config.py # Logging setup
└── services/
    └── generator.py  # ProjectCreator (basic)
```

**Tests**:
```python
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_project_basic():
    response = client.post("/api/projects", json={
        "brand": "TestBrand",
        "country": "Paraguay"
    })
    assert response.status_code == 200
    assert "project_path" in response.json()
```

---

## Week 2: Generator Module

### Milestone: Complete Project Generation

**Duration**: 5 days

**Deliverables**:
- Full project structure creation
- All templates rendered
- Research folders with files
- Ideas folder with templates
- GET project info endpoint

**Exit Criteria**:
- Creating project generates 50+ files
- All templates render correctly
- README files have proper content
- Can retrieve project info

**Tasks**:

```
Day 2.1: Template Engine
- [ ] Implement templates.py
- [ ] Load Jinja2 templates
- [ ] Render with variables
- [ ] Test rendering

Day 2.2: Research Structure
- [ ] Create 10 research folders
- [ ] Create files per category
- [ ] Render research templates
- [ ] Create investigation README

Day 2.3: Ideas Structure
- [ ] Create ideas folder
- [ ] Generate 25 idea templates
- [ ] Create 00-RESUMEN-IDEAS.md
- [ ] Render idea templates

Day 2.4: Project README & Brief
- [ ] Generate project README
- [ ] Create BRIEF-CAMPANA.md template
- [ ] Create QUICK-REFERENCE.md template
- [ ] Test full project creation

Day 2.5: Project Info Endpoint
- [ ] GET /api/projects/{id}
- [ ] Return file/folder counts
- [ ] Return creation date
- [ ] Test retrieval
```

**Code to Write**:
```
code/api/
├── services/
│   ├── generator.py      # Full implementation
│   └── templates.py      # Template engine
└── templates/            # All Jinja2 templates
    ├── readme.md.j2
    ├── research_file.md.j2
    ├── idea.md.j2
    ├── brief.md.j2
    └── quick_reference.md.j2
```

**Tests**:
```python
def test_create_project_full():
    response = client.post("/api/projects", json={
        "brand": "Nike",
        "country": "Argentina"
    })
    project_path = Path(response.json()["project_path"])

    # Check structure
    assert (project_path / "README.md").exists()
    assert (project_path / "ideas").exists()
    assert len(list((project_path / "ideas").glob("idea-*.md"))) == 25

def test_research_structure():
    # Check all 10 research folders exist
    research_path = project_path / "investigacion-nike-argentina"
    assert len(list(research_path.glob("*/"))) >= 10
```

---

## Week 3: Research Module

### Milestone: Source Management + AI Summaries

**Duration**: 5 days

**Deliverables**:
- Add source with formatting
- URL validation
- AI summarization
- Progress tracking
- n8n workflows for research

**Exit Criteria**:
- Adding source updates fuentes-completas.md
- Invalid URLs are flagged
- AI summaries work via n8n
- Progress shows completion %

**Tasks**:

```
Day 3.1: Source Manager
- [ ] Implement sources.py
- [ ] Parse existing sources
- [ ] Add new source
- [ ] Format citation
- [ ] Update sources file

Day 3.2: URL Validation
- [ ] Validate URL format
- [ ] Check accessibility (HEAD request)
- [ ] Mark valid/invalid
- [ ] Handle timeouts

Day 3.3: AI Summarization Workflow
- [ ] Create WF-101 in n8n
- [ ] Fetch URL content
- [ ] Claude node for summary
- [ ] Call Python to save
- [ ] Test with real URLs

Day 3.4: Progress Tracking
- [ ] Implement tracker.py
- [ ] Calculate per-category progress
- [ ] Check file content completeness
- [ ] Create status endpoint

Day 3.5: Research Endpoints
- [ ] POST /api/sources
- [ ] GET /api/sources/{project}
- [ ] POST /api/sources/{project}/validate
- [ ] GET /api/projects/{id}/progress
```

**Code to Write**:
```
code/api/services/
├── research.py       # SourceManager, ResearchTracker
```

**n8n Workflows**:
- WF-101: Add Source with Summary
- WF-102: Validate All Sources
- WF-103: Check Progress

**Tests**:
```python
@pytest.mark.asyncio
async def test_add_source():
    response = await client.post("/api/sources", json={
        "project": "campana-test-2025",
        "url": "https://example.com",
        "title": "Test Article",
        "category": "media",
        "topic": "market"
    })
    assert response.status_code == 200
    assert "formatted" in response.json()
```

---

## Week 4: Scoring Module

### Milestone: Score Calculation + Rankings

**Duration**: 5 days

**Deliverables**:
- Parse scores from ideas
- Calculate weighted totals
- Classify into tiers
- Generate ranking report
- Update summary file

**Exit Criteria**:
- Scores parsed correctly from markdown
- Rankings sorted properly
- Tiers assigned correctly
- Summary file updated automatically

**Tasks**:

```
Day 4.1: Score Parser
- [ ] Implement calculator.py
- [ ] Parse scoring table from markdown
- [ ] Extract criterion scores
- [ ] Handle missing/invalid scores

Day 4.2: Score Calculation
- [ ] Calculate weighted total
- [ ] Support custom weights
- [ ] Validate score ranges
- [ ] Test with sample ideas

Day 4.3: Tier Classification
- [ ] Implement tier thresholds
- [ ] Assign tier labels
- [ ] Handle edge cases
- [ ] Test classification

Day 4.4: Ranking Report
- [ ] Implement reports.py
- [ ] Generate ranking table
- [ ] Create Top 10 analysis
- [ ] Generate recommendations (A/B/C)

Day 4.5: Summary Update
- [ ] Update 00-RESUMEN-IDEAS.md
- [ ] Include all rankings
- [ ] Include tier groupings
- [ ] Create n8n workflow
```

**Code to Write**:
```
code/api/services/
├── scoring.py        # ScoreCalculator, ReportGenerator
```

**n8n Workflows**:
- WF-301: Calculate Scores

**Tests**:
```python
def test_score_calculation():
    scores = {
        "Diferenciación": 8,
        "Autenticidad": 7,
        # ... all 10
    }
    calculator = ScoreCalculator(config)
    total = calculator.calculate_total(scores)
    assert 0 <= total <= 100

def test_tier_classification():
    assert calculator.get_tier(95) == "🏆 MUY ALTO"
    assert calculator.get_tier(85) == "🥇 ALTO"
    assert calculator.get_tier(55) == "❌ NO RECOMENDADO"
```

---

## Week 5: Synthesis Module

### Milestone: Brief Analysis + Quick Reference

**Duration**: 5 days

**Deliverables**:
- AI brief analysis
- Quick reference generation
- Cross-reference validation
- Index generation
- n8n workflows

**Exit Criteria**:
- Brief analysis extracts all components
- Quick reference auto-generates from research
- Internal links validated
- Indexes auto-update

**Tasks**:

```
Day 5.1: Brief Analysis Workflow
- [ ] Create WF-201 in n8n
- [ ] Parse brief content
- [ ] Claude: extract challenge
- [ ] Claude: extract target
- [ ] Claude: suggest directions

Day 5.2: Brief Generator
- [ ] Implement brief_analyzer.py
- [ ] Receive AI analysis
- [ ] Render BRIEF-CAMPANA.md
- [ ] Save to project

Day 5.3: Quick Reference Workflow
- [ ] Create WF-203 in n8n
- [ ] Gather all research content
- [ ] Claude: extract key data
- [ ] Claude: generate insights
- [ ] Claude: dos/donts

Day 5.4: Quick Reference Generator
- [ ] Implement quick_reference.py
- [ ] Receive AI extractions
- [ ] Render QUICK-REFERENCE.md
- [ ] Save to project

Day 5.5: Validation & Indexes
- [ ] Implement cross_reference.py
- [ ] Validate internal links
- [ ] Generate folder indexes
- [ ] Report broken links
```

**Code to Write**:
```
code/api/services/
├── synthesis.py      # BriefAnalyzer, QuickReferenceGenerator
├── cross_reference.py
```

**n8n Workflows**:
- WF-201: Analyze Brief
- WF-203: Generate Quick Reference

**Tests**:
```python
@pytest.mark.asyncio
async def test_quick_reference_generation():
    response = await client.post("/api/synthesis/quick-reference", json={
        "project": "campana-test-2025",
        "market_data": {...},
        "insights": [...],
        # ...
    })
    assert response.status_code == 200

    # Check file was created
    qr_path = project_path / "investigacion-test-paraguay" / "QUICK-REFERENCE.md"
    assert qr_path.exists()
```

---

## Week 6: Export & Polish

### Milestone: v1.0 Release

**Duration**: 5 days

**Deliverables**:
- PDF export
- PPTX export
- Full test coverage
- Documentation complete
- Bug fixes

**Exit Criteria**:
- PDFs generate correctly
- PPTX opens in PowerPoint
- 80%+ test coverage
- All docs reviewed
- No critical bugs

**Tasks**:

```
Day 6.1: PDF Export
- [ ] Implement pdf.py
- [ ] Markdown to PDF conversion
- [ ] Apply styling
- [ ] Batch export top N
- [ ] Test output

Day 6.2: PPTX Export
- [ ] Implement presentation.py
- [ ] Create slide templates
- [ ] Populate from project data
- [ ] Export to PPTX
- [ ] Test in PowerPoint

Day 6.3: Testing
- [ ] Add missing unit tests
- [ ] Integration tests
- [ ] n8n workflow tests
- [ ] Coverage report

Day 6.4: Documentation
- [ ] User guide
- [ ] API documentation
- [ ] Update README
- [ ] Example walkthrough

Day 6.5: Polish & Release
- [ ] Bug fixes
- [ ] Performance tuning
- [ ] Final testing
- [ ] Tag v1.0.0
- [ ] Celebrate! 🎉
```

**Code to Write**:
```
code/api/services/
├── export.py         # PDFExporter, PresentationGenerator
```

**n8n Workflows**:
- WF-401: Export PDF
- WF-402: Export PPTX

---

## Post-v1.0 Enhancements

### v1.1 (Week 7-8)
- [ ] Idea generation assist (AI)
- [ ] Better PDF styling
- [ ] Google Slides export
- [ ] Dashboard UI

### v1.2 (Week 9-10)
- [ ] Multi-user support
- [ ] Project sharing
- [ ] Commenting system
- [ ] Version history

### v2.0 (Future)
- [ ] Web interface
- [ ] Real-time collaboration
- [ ] Cloud storage
- [ ] Mobile app

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| AI API changes | Low | High | Abstract AI service, fallback provider |
| n8n learning curve | Medium | Medium | Start simple, use documentation |
| Complex markdown parsing | Medium | Medium | Use established regex patterns |
| PDF generation issues | Medium | Low | Test with real content early |
| Scope creep | High | High | Strict milestone definition |

---

## Success Metrics

### Week 1
- [ ] API starts successfully
- [ ] Health endpoint returns 200
- [ ] First n8n workflow runs

### Week 2
- [ ] 50+ files generated per project
- [ ] All templates render
- [ ] Project info retrieval works

### Week 3
- [ ] Sources add successfully
- [ ] AI summaries generate
- [ ] Progress tracking works

### Week 4
- [ ] Scores calculate correctly
- [ ] Rankings sort properly
- [ ] Summary updates automatically

### Week 5
- [ ] Brief analysis complete
- [ ] Quick reference generates
- [ ] Links validated

### Week 6
- [ ] PDFs export correctly
- [ ] PPTX opens successfully
- [ ] 80%+ test coverage
- [ ] v1.0 released

---

## Daily Standup Format

```
Yesterday: [What was completed]
Today: [What will be worked on]
Blockers: [Any issues]
```

## Weekly Review Format

```
Milestone: [Name]
Status: [On Track / At Risk / Blocked]
Completed: [List of completed items]
Remaining: [List of remaining items]
Blockers: [Any issues]
Next Week: [Upcoming focus]
```

---

## Tools for Tracking

- **GitHub Issues** - Task tracking
- **GitHub Projects** - Kanban board
- **Daily notes** - Progress journal

---

Ready to start Week 1! 🚀
