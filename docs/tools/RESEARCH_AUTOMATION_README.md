# Research Automation Tool

Automated research gathering system for campaign development using web search and fetch capabilities.

## Overview

This tool systematically gathers research data for each phase of campaign development:

1. **01-mercado-general** - Market Analysis
2. **02-marca** - Brand Analysis
3. **03-competencia** - Competitive Analysis
4. **04-consumidor** - Consumer Research
5. **05-cultura-local** - Cultural Context
6. **06-estadisticas** - Statistics & Data
7. **08-investigacion-creativa** - Creative Research

## Components

### 1. Research Automation Service (`code/api/services/research_automation.py`)

Full API integration for automated research:

```python
from code.api.services.research_automation import get_research_automation_service

service = get_research_automation_service()

# Run full research
results = await service.run_full_research(
    project_id="campaign-123",
    brief_data={
        "brand": "Pilsen",
        "industry": "cerveza",
        "country": "Paraguay",
        "target_audience": "jóvenes 18-30"
    }
)

# Run single phase
results = await service.run_single_phase(
    project_id="campaign-123",
    phase_id="01-mercado-general",
    brief_data=brief_data
)

# Expand research for gaps
results = await service.expand_research(
    project_id="campaign-123",
    gaps=["market share 2024", "competitor pricing"],
    brief_data=brief_data
)
```

### 2. Research Runner CLI (`tools/research_runner.py`)

Standalone CLI tool for generating research plans:

```bash
python tools/research_runner.py \
    --brand "Pilsen" \
    --industry "cerveza" \
    --country "Paraguay" \
    --target "jóvenes 18-35 años" \
    --output "./investigacion-pilsen-2025"
```

**Output:**
- `research_plan.json` - Complete plan with all queries
- `RESEARCH_INSTRUCTIONS.md` - Step-by-step execution guide
- Phase directories with templates

## Usage with Claude Code

### Method 1: Generate Plan and Execute Manually

1. Generate the research plan:
```bash
python tools/research_runner.py --brand "Subway" --industry "fast food" --output "./research-subway"
```

2. Open `RESEARCH_INSTRUCTIONS.md` and follow with Claude Code:
```
Execute the research plan in research-subway/RESEARCH_INSTRUCTIONS.md
```

3. Claude Code will use WebSearch and WebFetch to gather data.

### Method 2: Direct Claude Code Command

Ask Claude Code directly:
```
Research the beer market in Paraguay for Pilsen brand targeting young adults 18-35.
Create a complete research folder with:
- Market analysis
- Brand analysis
- Competitive analysis
- Consumer behavior
- Cultural context
- Statistics
- Creative references

Use WebSearch for each topic and WebFetch to get detailed content.
```

### Method 3: Using the Research Automation API

For integration with the full campaign generator:

```python
# In your API endpoint
from code.api.services.research_automation import get_research_automation_service

@router.post("/projects/{project_id}/research/automate")
async def automate_research(project_id: str, brief_data: dict):
    service = get_research_automation_service()
    results = await service.run_full_research(project_id, brief_data)
    return results
```

## Research Phase Details

### 01-mercado-general (Market Analysis)
**Goal:** Understand market size, trends, and industry landscape

**Queries generated:**
- `{industry} mercado {country} {year} estadísticas`
- `{industry} industria {country} tamaño mercado crecimiento`
- `{industry} tendencias mercado {country} {year}`

**Output includes:**
- Market value (USD/local currency)
- Volume metrics
- Growth rates
- Key players and market share
- Trends and forecasts

### 02-marca (Brand Analysis)
**Goal:** Deep understanding of the brand's history, positioning, and current state

**Queries generated:**
- `{brand} {country} historia marca`
- `{brand} campañas marketing {year}`
- `{brand} posicionamiento estrategia marca`

**Output includes:**
- Brand history and heritage
- Product portfolio
- Past campaign analysis
- Brand positioning
- Tone and voice characteristics

### 03-competencia (Competitive Analysis)
**Goal:** Map competitive landscape and positioning opportunities

**Queries generated:**
- `{brand} competidores {country} participación mercado`
- `{industry} marcas {country} comparación`
- `{brand} vs competencia análisis`

**Output includes:**
- Direct competitors list
- Market share comparison
- Positioning map
- Competitive advantages
- Threat assessment

### 04-consumidor (Consumer Research)
**Goal:** Understand target audience deeply

**Queries generated:**
- `{target_audience} {country} demografía estadísticas`
- `{target_audience} comportamiento consumidor {country}`
- `{target_audience} hábitos digitales {country} redes sociales`

**Output includes:**
- Demographic profile
- Psychographic insights
- Digital behavior patterns
- Decision journey
- Media consumption

### 05-cultura-local (Cultural Context)
**Goal:** Cultural authenticity and local relevance

**Queries generated:**
- `{country} cultura tradiciones {industry}`
- `{country} expresiones locales lenguaje jerga`
- `{country} cultura consumidor valores`

**Output includes:**
- Local traditions
- Language/slang (jopará for Paraguay)
- Cultural values
- Important occasions
- Taboos and sensitivities

### 06-estadisticas (Statistics & Data)
**Goal:** Hard data and verified metrics

**Queries generated:**
- `{industry} {country} estadísticas {year} oficial`
- `{brand} participación mercado {country} {year}`
- `{industry} datos consumo {country}`

**Output includes:**
- Official statistics
- Verified data points
- Source attribution
- Confidence levels
- Data ranges when sources differ

### 08-investigacion-creativa (Creative Research)
**Goal:** Inspiration and reference material

**Queries generated:**
- `{industry} campañas premiadas Cannes Lions {year}`
- `{industry} campañas virales marketing Latinoamérica`
- `{country} contenido viral redes sociales {year}`

**Output includes:**
- Award-winning campaigns
- Viral content examples
- Visual references
- Creative patterns
- Applicable insights

## Output Structure

```
investigacion-{brand}-{year}/
├── 01-mercado-general/
│   └── resumen-mercado.md
├── 02-marca/
│   └── analisis-marca.md
├── 03-competencia/
│   └── analisis-competitivo.md
├── 04-consumidor/
│   └── comportamiento-consumidor.md
├── 05-cultura-local/
│   └── contexto-cultural.md
├── 06-estadisticas/
│   └── datos-estadisticos.md
├── 08-investigacion-creativa/
│   └── investigacion-creativa.md
├── QUICK-REFERENCE.md
├── RESUMEN-EJECUTIVO.md
├── INSIGHTS-CREATIVOS.md
└── research_plan.json
```

## Best Practices

### Source Quality
- Prioritize official sources (government, industry reports)
- Use multiple sources for key data points
- Note source reliability in documents
- Include access dates for all URLs

### Data Triangulation
- Get 3+ sources for important statistics
- Note when sources disagree
- Provide ranges when data varies
- Explain methodology differences

### Cultural Authenticity
- Research local expressions
- Understand context, not just translation
- Note regional variations
- Include native speaker insights

### Actionability
- Extract specific insights, not just data
- Connect findings to creative opportunities
- Provide concrete examples
- Make recommendations clear

## Customization

### Adding New Phases

Edit `RESEARCH_PHASES` in either file:

```python
"09-nuevos-hallazgos": {
    "name": "New Findings",
    "description": "Additional research to fill gaps",
    "query_templates": [
        "{gap_topic} {country} {year}",
        "{brand} {gap_topic} analysis"
    ],
    "min_sources": 2,
    "priority": 9,
    "output_file": "nuevos-hallazgos.md"
}
```

### Custom Query Templates

Variables available:
- `{brand}` - Brand name
- `{industry}` - Industry/category
- `{country}` - Target country
- `{target_audience}` - Target audience
- `{year}` - Current year
- `{season}` - Campaign season
- `{campaign_type}` - Type of campaign

### Region-Specific Research

For different countries, adjust:
- Language of queries (Spanish for LATAM)
- Cultural research focus
- Local platform emphasis
- Regional competitors

## Integration Examples

### With Brief Parser

```python
from code.api.services.brief_parser import get_brief_parser
from code.api.services.research_automation import get_research_automation_service

# Parse brief
parser = get_brief_parser()
brief_data = await parser.parse_brief(brief_file)

# Run research
research = get_research_automation_service()
results = await research.run_full_research(project_id, brief_data)
```

### With Ideas Generator

```python
# After research is complete
from code.api.services.ideas_service import get_ideas_service

ideas = get_ideas_service()
all_research = await research.get_all_research(project_id)
generated_ideas = await ideas.generate_ideas(project_id, all_research, brief_data)
```

## Troubleshooting

### Search Returns No Results
- Check query language matches region
- Simplify query terms
- Try alternative phrasings
- Use broader industry terms

### Fetch Errors
- Some sites block automated access
- Try alternative sources
- Note blocked URLs for manual review
- Use cached versions if available

### Missing Variables
- Ensure brief_data has all required fields
- Set defaults for optional fields
- Log warnings for missing data

## Performance Notes

- Rate limiting: 0.5-1 second between searches
- Parallel fetching: Up to 5 URLs at once
- Content truncation: 50,000 characters max per fetch
- Typical runtime: 5-15 minutes for full research

## License

Internal tool for campaign development.
