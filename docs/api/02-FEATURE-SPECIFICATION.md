# Feature Specification Document

Complete specification of all features, user stories, and acceptance criteria for the Campaign Research Generator.

---

## Table of Contents

1. [Feature Overview](#feature-overview)
2. [User Personas](#user-personas)
3. [Core Features](#core-features)
4. [Feature Details](#feature-details)
5. [User Flows](#user-flows)
6. [Edge Cases](#edge-cases)
7. [Non-Functional Requirements](#non-functional-requirements)

---

## Feature Overview

### System Purpose
Automate the creation and management of marketing campaign research projects, from initial brief analysis to final deliverables.

### Feature Categories

| Category | Features | Priority |
|----------|----------|----------|
| Project Generation | Create structure, templates | P0 - Critical |
| Research Management | Sources, tracking, summaries | P0 - Critical |
| AI Integration | Brief analysis, idea assist | P0 - Critical |
| Scoring System | Calculate, rank, report | P1 - High |
| Synthesis | Quick reference, cross-refs | P1 - High |
| Export | PDF, PPTX | P2 - Medium |
| Collaboration | Share, comment | P3 - Future |

---

## User Personas

### Primary: Creative Strategist
**Name**: María
**Role**: Junior Creative at Agency
**Goals**:
- Complete campaign research faster
- Generate more ideas
- Present professional deliverables

**Pain Points**:
- Manual folder creation is tedious
- Tracking sources is chaotic
- Scoring ideas is subjective
- Formatting takes too long

**Tech Comfort**: Medium (knows tools, not coding)

### Secondary: Account Executive
**Name**: Carlos
**Role**: Account Executive
**Goals**:
- Review research progress
- Share updates with clients
- Get quick summaries

**Pain Points**:
- Hard to know project status
- No quick overview of findings
- Manual report creation

**Tech Comfort**: Low (uses UI only)

### Tertiary: Creative Director
**Name**: Ana
**Role**: Creative Director
**Goals**:
- Review top ideas quickly
- Understand scoring rationale
- Make final selections

**Pain Points**:
- Too many ideas to review
- No clear ranking system
- Missing context for decisions

**Tech Comfort**: Low (reviews outputs only)

---

## Core Features

### F1: Project Generation

#### F1.1: Create New Project
**Description**: Generate complete project structure with all folders and template files.

**User Story**:
> As a creative strategist, I want to create a new campaign project with one command so that I can start working immediately without manual setup.

**Acceptance Criteria**:
- [ ] Creates project folder with correct naming (campana-{brand}-{year})
- [ ] Creates 10 research category folders
- [ ] Generates template files in each folder
- [ ] Creates ideas folder with 25 numbered templates
- [ ] Creates README.md with project overview
- [ ] Creates BRIEF-CAMPANA.md template
- [ ] Creates QUICK-REFERENCE.md template
- [ ] Supports custom number of ideas
- [ ] Supports custom output directory

**Input**:
```yaml
brand: string (required)
country: string (default: "Paraguay")
campaign_type: string (default: "digital")
year: integer (default: current year)
num_ideas: integer (default: 25)
output_dir: path (default: current directory)
```

**Output**:
```yaml
project_path: path to created project
files_created: count of files
folders_created: count of folders
```

**Error Handling**:
- Project folder already exists → Ask to overwrite or rename
- Invalid brand name → Show validation error
- Insufficient disk space → Show error with required space

---

#### F1.2: Project Templates
**Description**: All generated files contain useful templates, not empty files.

**User Story**:
> As a creative strategist, I want generated files to have template content so that I know what information to fill in each section.

**Acceptance Criteria**:
- [ ] Research files have standard sections (Resumen, Datos, Referencias)
- [ ] Idea files have complete structure (Concepto, Ejecución, Scoring)
- [ ] Brief template has all required sections
- [ ] Quick Reference has placeholder format
- [ ] All templates are in Spanish
- [ ] Templates include example content/placeholders

---

### F2: Research Management

#### F2.1: Add Source
**Description**: Add a research source with automatic formatting and validation.

**User Story**:
> As a creative strategist, I want to add sources with just a URL so that citation formatting is handled automatically.

**Acceptance Criteria**:
- [ ] Accepts URL, title, category, topic
- [ ] Validates URL is accessible
- [ ] Auto-formats citation in markdown
- [ ] Adds to fuentes-completas.md
- [ ] Categorizes correctly (media, corporate, study, institutional)
- [ ] Records date accessed
- [ ] Optionally fetches and summarizes content

**Input**:
```yaml
url: string (required, valid URL)
title: string (required)
category: enum (media, corporate, study, institutional)
topic: string (required)
summarize: boolean (default: false)
```

**Output**:
```yaml
source_id: unique identifier
formatted_citation: markdown string
is_valid: boolean
summary: string (if requested)
```

---

#### F2.2: Validate Sources
**Description**: Check all sources for broken links.

**User Story**:
> As a creative strategist, I want to validate all my sources before presenting so that I don't have broken links.

**Acceptance Criteria**:
- [ ] Checks all URLs in sources file
- [ ] Reports valid/invalid counts
- [ ] Lists broken URLs
- [ ] Optionally removes or marks broken links
- [ ] Shows last validation date

---

#### F2.3: Research Progress Tracking
**Description**: Track completion status of each research category.

**User Story**:
> As a creative strategist, I want to see my research progress so that I know what areas need more work.

**Acceptance Criteria**:
- [ ] Shows progress per category (01-10)
- [ ] Calculates based on file content (not just existence)
- [ ] Visual progress bar
- [ ] Shows total progress percentage
- [ ] Identifies empty/incomplete files
- [ ] Lists pending items

**Progress Calculation**:
```
Category Progress =
  (Files with content / Total expected files) ×
  (Average content completeness)

Content Completeness =
  (Filled sections / Total sections) × 100
```

---

#### F2.4: AI Research Summary
**Description**: AI-powered summarization of web content for research.

**User Story**:
> As a creative strategist, I want to get AI summaries of web articles so that I can quickly extract relevant information.

**Acceptance Criteria**:
- [ ] Fetches URL content
- [ ] Extracts text from HTML
- [ ] Summarizes with AI (Claude/GPT)
- [ ] Focuses on marketing-relevant data
- [ ] Returns in Spanish
- [ ] Extracts key statistics
- [ ] Identifies insights

**AI Prompt Requirements**:
- Focus on market data, statistics
- Extract consumer insights
- Identify competitive information
- Note cultural relevance
- Maximum 500 characters

---

### F3: AI Integration

#### F3.1: Brief Analysis
**Description**: AI analyzes campaign brief to extract structured information.

**User Story**:
> As a creative strategist, I want the AI to analyze my brief so that I have a clear structure of challenges, targets, and opportunities.

**Acceptance Criteria**:
- [ ] Parses brief document (PDF or MD)
- [ ] Extracts core challenge
- [ ] Identifies target audience details
- [ ] Lists brand requirements/restrictions
- [ ] Defines success metrics
- [ ] Suggests creative directions
- [ ] Generates expanded BRIEF-CAMPANA.md

**Output Structure**:
```yaml
challenge:
  main: string
  constraints: list
target:
  demographics: dict
  psychographics: dict
  media_consumption: dict
brand:
  tone: list
  restrictions: list
  visual_guidelines: string
kpis:
  - metric: string
    goal: string
directions:
  - name: string
    description: string
    rationale: string
```

---

#### F3.2: Idea Generation Assist
**Description**: AI helps generate campaign ideas based on research and brief.

**User Story**:
> As a creative strategist, I want AI to help generate initial ideas so that I have starting points to develop.

**Acceptance Criteria**:
- [ ] Uses research summary as context
- [ ] Uses brief analysis as requirements
- [ ] Generates specified number of ideas
- [ ] Each idea has: name, concept, insight, execution
- [ ] Ideas are culturally relevant
- [ ] Ideas align with brand voice
- [ ] Saves to idea template files

**AI Prompt Requirements**:
- Generate diverse approaches
- Connect to documented insights
- Consider cultural context
- Include specific executions
- Vary tone and format

**Note**: AI-generated ideas are starting points. Human creativity refines them.

---

#### F3.3: Quick Reference Generation
**Description**: AI compiles Quick Reference from research files.

**User Story**:
> As a creative strategist, I want the system to auto-generate my Quick Reference so that I always have an updated 1-page summary.

**Acceptance Criteria**:
- [ ] Reads all research files
- [ ] Extracts key metrics
- [ ] Compiles target profile
- [ ] Identifies top insights
- [ ] Generates Do/Don't lists
- [ ] Creates brainstorming questions
- [ ] Formats in QR template
- [ ] Updates when research changes

---

### F4: Scoring System

#### F4.1: Score Calculation
**Description**: Calculate weighted scores for ideas.

**User Story**:
> As a creative strategist, I want automatic score calculation so that rankings are consistent and objective.

**Acceptance Criteria**:
- [ ] Parses scores from idea files
- [ ] Applies weights to criteria
- [ ] Calculates total (0-100)
- [ ] Supports 10 default criteria
- [ ] Allows custom criteria
- [ ] Allows custom weights
- [ ] Validates score ranges (1-10)

**Default Criteria**:
1. Diferenciación (1.0)
2. Autenticidad (1.0)
3. Potencial Viral (1.0)
4. Conexión Emocional (1.0)
5. Ejecutabilidad (1.0)
6. Esencia de Marca (1.0)
7. Target Connection (1.0)
8. Formato Digital (1.0)
9. Memorable (1.0)
10. Valor al Consumidor (1.0)

---

#### F4.2: Tier Classification
**Description**: Classify ideas into tiers based on score.

**User Story**:
> As a creative director, I want ideas grouped by potential so that I can focus review on top tiers.

**Acceptance Criteria**:
- [ ] Classifies into 5 tiers
- [ ] Uses configurable thresholds
- [ ] Assigns visual indicators
- [ ] Shows count per tier

**Default Thresholds**:
- 🏆 MUY ALTO: 90-100
- 🥇 ALTO: 80-89
- 🥈 MEDIO: 70-79
- ⚠️ NECESITA TRABAJO: 60-69
- ❌ NO RECOMENDADO: <60

---

#### F4.3: Ranking Report
**Description**: Generate comprehensive ranking report.

**User Story**:
> As a creative director, I want a complete ranking report so that I can make informed selection decisions.

**Acceptance Criteria**:
- [ ] Lists all ideas sorted by score
- [ ] Shows rank, name, score, tier
- [ ] Groups by tier
- [ ] Provides Top 10 detailed analysis
- [ ] Generates 3 recommendation options
- [ ] Updates 00-RESUMEN-IDEAS.md

**Recommendation Options**:
- Option A: Best overall score
- Option B: Best viral potential
- Option C: Best differentiation

---

### F5: Synthesis

#### F5.1: Cross-Reference Validation
**Description**: Validate internal links between documents.

**User Story**:
> As a creative strategist, I want to check that all my internal links work so that navigation is reliable.

**Acceptance Criteria**:
- [ ] Finds all markdown links
- [ ] Validates file exists
- [ ] Reports broken links
- [ ] Suggests fixes
- [ ] Optionally auto-fixes

---

#### F5.2: Index Generation
**Description**: Auto-generate README indexes for folders.

**User Story**:
> As a creative strategist, I want auto-generated indexes so that navigation is always up to date.

**Acceptance Criteria**:
- [ ] Lists all files in folder
- [ ] Shows file descriptions
- [ ] Indicates completion status
- [ ] Links to each file
- [ ] Updates on changes

---

### F6: Export

#### F6.1: PDF Export
**Description**: Export ideas and reports to PDF.

**User Story**:
> As a creative strategist, I want to export ideas as PDFs so that I can share them professionally.

**Acceptance Criteria**:
- [ ] Converts markdown to PDF
- [ ] Applies consistent styling
- [ ] Includes cover page
- [ ] Supports batch export
- [ ] Exports top N ideas
- [ ] Creates combined PDF option

**PDF Styling**:
- Professional fonts
- Brand colors (configurable)
- Headers and footers
- Page numbers
- Table of contents (for combined)

---

#### F6.2: Presentation Export
**Description**: Generate PowerPoint presentation from project.

**User Story**:
> As an account executive, I want to generate presentations automatically so that I can share with clients quickly.

**Acceptance Criteria**:
- [ ] Creates title slide
- [ ] Creates research summary slides
- [ ] Creates idea slides
- [ ] Creates recommendation slide
- [ ] Uses template design
- [ ] Exports to PPTX
- [ ] Optionally exports to Google Slides

**Slide Structure**:
1. Title + Client + Date
2. Challenge Overview
3. Target Profile
4. Key Insights (3-5 slides)
5. Top Ideas (1 slide each)
6. Recommendations
7. Next Steps

---

## User Flows

### Flow 1: Complete Campaign Creation

```
Start
  │
  ▼
[Create New Project]
  │ Input: brand, country, type
  ▼
[Import Original Brief]
  │ Copy PDF to project
  ▼
[Analyze Brief with AI]
  │ Generate BRIEF-CAMPANA.md
  ▼
[Conduct Research]
  │ For each category:
  │   - Add sources
  │   - Get AI summaries
  │   - Fill templates
  ▼
[Check Progress]
  │ View status, identify gaps
  ▼
[Generate Quick Reference]
  │ AI compiles from research
  ▼
[Generate Ideas]
  │ AI assists with starting points
  │ Human refines and adds
  ▼
[Score Ideas]
  │ Fill scoring tables
  │ Calculate rankings
  ▼
[Generate Report]
  │ Update 00-RESUMEN-IDEAS.md
  ▼
[Select Final Concepts]
  │ Choose 1-3 from top 10
  ▼
[Export Deliverables]
  │ PDF, PPTX
  ▼
End
```

### Flow 2: Quick Source Addition

```
Start
  │
  ▼
[Find relevant URL]
  │
  ▼
[Add Source Command]
  │ Input: URL, title, category, topic
  ▼
[System Validates URL]
  │
  ├─ Invalid → Show error
  │
  ▼
[AI Summarizes Content]
  │
  ▼
[Format Citation]
  │
  ▼
[Add to fuentes-completas.md]
  │
  ▼
End (Source added)
```

### Flow 3: Scoring Workflow

```
Start
  │
  ▼
[Ideas Created and Filled]
  │
  ▼
[Fill Scoring Tables]
  │ For each idea:
  │   - Rate 10 criteria (1-10)
  ▼
[Calculate Scores Command]
  │
  ▼
[System Parses All Ideas]
  │
  ▼
[Calculate Weighted Totals]
  │
  ▼
[Classify into Tiers]
  │
  ▼
[Generate Ranking]
  │
  ▼
[Update Summary File]
  │
  ▼
[Review Rankings]
  │
  ▼
End
```

---

## Edge Cases

### Project Generation
1. **Brand name with special characters** → Sanitize to alphanumeric + hyphens
2. **Very long brand name** → Truncate to 50 characters
3. **Project already exists** → Prompt: overwrite, rename, or cancel
4. **No write permission** → Show clear error with path

### Source Management
1. **URL returns 404** → Mark as invalid, still add with warning
2. **URL requires authentication** → Show error, suggest manual entry
3. **URL is PDF** → Extract text if possible, else note limitation
4. **Duplicate URL** → Warn user, allow update or skip
5. **Non-Spanish content** → Summarize and translate key points

### AI Integration
1. **AI rate limited** → Queue request, retry with backoff
2. **AI returns error** → Fallback to other provider
3. **Context too long** → Chunk and summarize in parts
4. **AI returns incomplete** → Retry with clearer prompt
5. **API key invalid** → Clear error with setup instructions

### Scoring
1. **Missing scores in file** → Warn, exclude from ranking
2. **Invalid score (not 1-10)** → Show validation error
3. **All ideas same score** → Rank by secondary criteria
4. **No ideas to score** → Show message, no report

### Export
1. **Markdown parse error** → Show line number, skip file
2. **PDF generation fails** → Show error, suggest fix
3. **Very long content** → Paginate appropriately
4. **Missing images** → Show placeholder, warn

---

## Non-Functional Requirements

### Performance
- Project creation: < 5 seconds
- Source addition: < 3 seconds
- AI summary: < 30 seconds
- Score calculation: < 2 seconds
- PDF export (single): < 5 seconds
- PDF export (batch 25): < 60 seconds

### Reliability
- AI fallback if primary fails
- Graceful degradation without AI
- No data loss on errors
- Atomic file operations

### Usability
- Clear error messages in Spanish
- Progress indicators for long operations
- Confirmation for destructive actions
- Help text for all commands

### Security
- API keys in environment variables
- No secrets in generated files
- Validate all user input
- Sanitize file paths

### Maintainability
- Modular code structure
- Comprehensive logging
- Configuration over code
- Documented APIs

### Compatibility
- Windows, macOS, Linux
- Python 3.11+
- n8n latest stable
- UTF-8 throughout

---

## Feature Priority Matrix

### P0 - Must Have (MVP)
- F1.1: Create New Project
- F1.2: Project Templates
- F2.1: Add Source
- F4.1: Score Calculation
- F4.2: Tier Classification

### P1 - Should Have (v1.0)
- F2.3: Research Progress
- F2.4: AI Research Summary
- F3.1: Brief Analysis
- F3.3: Quick Reference Generation
- F4.3: Ranking Report
- F6.1: PDF Export

### P2 - Nice to Have (v1.1)
- F2.2: Validate Sources
- F3.2: Idea Generation Assist
- F5.1: Cross-Reference Validation
- F5.2: Index Generation
- F6.2: Presentation Export

### P3 - Future (v2.0)
- Collaboration features
- Cloud storage
- Real-time sync
- Mobile app

---

## Success Metrics

### Efficiency
- Time to create project: From 30 min → 30 sec
- Time to add source: From 5 min → 30 sec
- Time to score ideas: From 2 hours → 10 min
- Time to generate QR: From 1 hour → 1 min

### Quality
- Sources properly formatted: 100%
- Scoring consistency: Same input = same output
- AI summaries relevant: >80% user approval
- Export formatting correct: 100%

### Adoption
- Projects created per week
- Sources added per project
- AI features used
- Exports generated

---

## Glossary

| Term | Definition |
|------|------------|
| Brief | Campaign requirements document from client |
| Quick Reference (QR) | 1-page summary for brainstorming |
| Tier | Classification of idea quality (Very High to Not Recommended) |
| Source | Research reference with URL and citation |
| Insight | Human truth that inspires creative idea |
| Execution | Specific implementation of an idea |
