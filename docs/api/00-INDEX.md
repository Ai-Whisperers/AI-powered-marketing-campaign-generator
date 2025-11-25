# Campaign Generator Documentation Index

Complete documentation for the Campaign Research Generator system.

---

## Documentation Suite

| # | Document | Purpose | Pages |
|---|----------|---------|-------|
| 01 | [Technology Evaluation](01-TECHNOLOGY-EVALUATION.md) | Compare Full Code vs n8n vs Hybrid | Analysis & recommendation |
| 02 | [Feature Specification](02-FEATURE-SPECIFICATION.md) | All features, user stories, acceptance criteria | Product requirements |
| 03 | [Architecture](03-ARCHITECTURE.md) | System design, data flows, API endpoints | Technical design |
| 04 | [Preparation Checklist](04-PREPARATION-CHECKLIST.md) | Setup, config, templates, pre-flight | Development setup |
| 05 | [AI Prompts](05-AI-PROMPTS.md) | All Claude/GPT prompts with examples | AI integration |
| 06 | [Additional Preparation](06-ADDITIONAL-PREPARATION.md) | Error handling, security, monitoring, tests | Production readiness |
| 07 | [Project Roadmap](07-PROJECT-ROADMAP.md) | Week-by-week timeline with milestones | Project planning |

---

## Quick Start

### If you want to understand the approach
→ Read [01-TECHNOLOGY-EVALUATION.md](01-TECHNOLOGY-EVALUATION.md)

### If you want to know what we're building
→ Read [02-FEATURE-SPECIFICATION.md](02-FEATURE-SPECIFICATION.md)

### If you want to understand how it works
→ Read [03-ARCHITECTURE.md](03-ARCHITECTURE.md)

### If you want to start development
→ Read [04-PREPARATION-CHECKLIST.md](04-PREPARATION-CHECKLIST.md)

### If you want to work on AI integration
→ Read [05-AI-PROMPTS.md](05-AI-PROMPTS.md)

### If you need production-ready details
→ Read [06-ADDITIONAL-PREPARATION.md](06-ADDITIONAL-PREPARATION.md)

### If you want to see the timeline
→ Read [07-PROJECT-ROADMAP.md](07-PROJECT-ROADMAP.md)

---

## Key Decisions

### Architecture: Hybrid (n8n + Python)

**Why**: Best of both worlds
- n8n for AI calls, workflow orchestration, visual debugging
- Python for complex logic, file operations, calculations

### AI Provider: Anthropic Claude (Primary)

**Model**: claude-sonnet-4-20250514
- Best for marketing content
- Excellent Spanish language support
- Strong structured output

**Fallback**: OpenAI GPT-4-turbo

### Stack Summary

```
Orchestration: n8n
Backend API:   FastAPI (Python 3.11+)
AI:            Claude via n8n nodes
Templates:     Jinja2
PDF Export:    ReportLab
PPTX Export:   python-pptx
Storage:       File system (Markdown)
Config:        YAML
```

---

## Feature Summary

### MVP (P0)
- Create new project with structure
- Project templates
- Add research sources
- Calculate idea scores
- Tier classification

### v1.0 (P1)
- Research progress tracking
- AI research summaries
- Brief analysis
- Quick reference generation
- Ranking reports
- PDF export

### v1.1 (P2)
- Source validation
- Idea generation assist
- Cross-reference validation
- Index generation
- PPTX export

---

## Development Timeline

| Week | Phase | Focus |
|------|-------|-------|
| 1 | Setup | Environment, skeleton, first endpoint |
| 2 | Generator | Project creation, templates |
| 3 | Research | Sources, tracking, AI summaries |
| 4 | Scoring | Calculations, tiers, reports |
| 5 | Synthesis | Quick reference, brief analysis |
| 6 | Export | PDF, PPTX generation |

---

## Quick Reference

### API Endpoints

```
POST /api/projects              # Create project
GET  /api/projects/{id}         # Get project info
POST /api/sources               # Add source
POST /api/scoring/calculate     # Calculate scores
POST /api/synthesis/brief       # Generate brief analysis
POST /api/synthesis/quick-ref   # Generate quick reference
POST /api/export/pdf            # Export to PDF
POST /api/export/pptx           # Export to PPTX
```

### n8n Workflows

```
WF-001: Create New Project
WF-101: Add Source with Summary
WF-201: Analyze Brief
WF-203: Generate Quick Reference
WF-301: Calculate Scores
WF-401: Export PDF
```

### AI Prompts

```
PROMPT-001: Research Content Summary
PROMPT-010: Extract Core Challenge
PROMPT-011: Extract Target Audience
PROMPT-012: Suggest Creative Directions
PROMPT-020: Generate Quick Reference Data
PROMPT-030: Generate Idea Concepts
```

---

## File Structure

```
code/
├── api/                    # FastAPI application
│   ├── main.py            # Entry point
│   ├── config.py          # Configuration
│   └── services/          # Business logic
│
├── config/
│   ├── default.yaml       # Default settings
│   ├── prompts/           # AI prompts
│   └── templates/         # Jinja2 templates
│
├── tests/                 # Pytest tests
├── docs/                  # This documentation
└── n8n/workflows/         # Exported workflows
```

---

## Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
PYTHON_API_URL=http://localhost:8000
PROJECTS_DIR=./projects
```

---

## Next Steps

1. **Complete environment setup** per [04-PREPARATION-CHECKLIST.md](04-PREPARATION-CHECKLIST.md)
2. **Create Python API skeleton** with FastAPI
3. **Build first n8n workflow** (Create Project)
4. **Test AI prompts** with sample data
5. **Iterate and expand**

---

## Support

For questions about:
- **Architecture decisions** → Review doc 01
- **Feature requirements** → Review doc 02
- **Technical implementation** → Review doc 03
- **Setup issues** → Review doc 04
- **AI integration** → Review doc 05
- **Error handling, security, monitoring** → Review doc 06
- **Timeline and milestones** → Review doc 07

---

**Total Documentation**: ~20,000+ words across 7 comprehensive documents

Ready to build! 🚀
