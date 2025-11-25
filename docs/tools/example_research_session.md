# Example Research Session with Claude Code

This document shows how to run a complete research automation session using Claude Code's WebSearch and WebFetch tools.

## Quick Start

### Step 1: Generate Research Plan

```bash
python tools/research_runner.py \
    --brand "Pilsen" \
    --industry "cerveza" \
    --country "Paraguay" \
    --target "jóvenes 18-35 años" \
    --output "./investigacion-pilsen-2025"
```

### Step 2: Execute with Claude Code

Open Claude Code and paste the following prompt:

---

## Research Automation Prompt for Claude Code

```
Execute a systematic research automation for the following campaign:

**Brand:** Pilsen
**Industry:** Cerveza (Beer)
**Country:** Paraguay
**Target Audience:** Jóvenes 18-35 años
**Campaign Type:** Fin de Año 2025

For each research phase below, use WebSearch to find information and WebFetch to extract content from the most relevant results. Then compile findings into markdown documents.

---

### PHASE 1: Market Analysis (01-mercado-general)

**Searches to execute:**

1. WebSearch: "cerveza mercado Paraguay 2025 estadísticas"
2. WebSearch: "cerveza industria Paraguay tamaño mercado crecimiento"
3. WebSearch: "cerveza tendencias mercado Paraguay 2025"

**For each search:**
- Review top 3-5 results
- WebFetch the most relevant URLs
- Extract: market size, growth rates, key players, trends

**Output:** Create `investigacion-pilsen-2025/01-mercado-general/resumen-mercado.md`

---

### PHASE 2: Brand Analysis (02-marca)

**Searches to execute:**

1. WebSearch: "Pilsen Paraguay historia marca"
2. WebSearch: "Pilsen campañas marketing 2024 2025"
3. WebSearch: "Pilsen posicionamiento estrategia marca"
4. WebSearch: "Cervepar Pilsen productos portafolio"

**For each search:**
- Focus on official sources and news articles
- Extract: brand history, campaigns, positioning, product range

**Output:** Create `investigacion-pilsen-2025/02-marca/analisis-marca.md`

---

### PHASE 3: Competitive Analysis (03-competencia)

**Searches to execute:**

1. WebSearch: "Pilsen competidores Paraguay participación mercado"
2. WebSearch: "cerveza marcas Paraguay comparación Munich Brahma"
3. WebSearch: "cerveza Paraguay market share 2024"

**For each search:**
- Extract: competitor list, market shares, positioning differences

**Output:** Create `investigacion-pilsen-2025/03-competencia/analisis-competitivo.md`

---

### PHASE 4: Consumer Research (04-consumidor)

**Searches to execute:**

1. WebSearch: "jóvenes Paraguay demografía estadísticas 2024"
2. WebSearch: "consumidor cerveza Paraguay comportamiento"
3. WebSearch: "jóvenes Paraguay hábitos digitales redes sociales"
4. WebSearch: "millennials Paraguay preferencias consumo"

**For each search:**
- Extract: demographics, digital behavior, preferences, decision factors

**Output:** Create `investigacion-pilsen-2025/04-consumidor/comportamiento-consumidor.md`

---

### PHASE 5: Cultural Context (05-cultura-local)

**Searches to execute:**

1. WebSearch: "Paraguay cultura tradiciones cerveza"
2. WebSearch: "Paraguay expresiones jopará jerga juvenil"
3. WebSearch: "Paraguay diciembre tradiciones fiestas"
4. WebSearch: "Paraguay valores culturales familia amistad"

**For each search:**
- Extract: traditions, expressions, values, occasions

**Output:** Create `investigacion-pilsen-2025/05-cultura-local/contexto-cultural.md`

---

### PHASE 6: Statistics (06-estadisticas)

**Searches to execute:**

1. WebSearch: "cerveza Paraguay estadísticas 2024 oficial"
2. WebSearch: "Pilsen participación mercado Paraguay porcentaje"
3. WebSearch: "consumo cerveza per capita Paraguay"

**For each search:**
- Focus on official sources, industry reports
- Extract: verified statistics with sources

**Output:** Create `investigacion-pilsen-2025/06-estadisticas/datos-estadisticos.md`

---

### PHASE 7: Creative Research (08-investigacion-creativa)

**Searches to execute:**

1. WebSearch: "cerveza campañas premiadas Cannes Lions 2024"
2. WebSearch: "cerveza campañas virales Latinoamérica"
3. WebSearch: "Paraguay contenido viral redes sociales 2024"
4. WebSearch: "Pilsen campañas exitosas caso estudio"

**For each search:**
- Extract: campaign examples, insights, creative approaches

**Output:** Create `investigacion-pilsen-2025/08-investigacion-creativa/investigacion-creativa.md`

---

### FINAL: Summary Documents

After completing all phases, create:

1. **QUICK-REFERENCE.md** - 1-page summary with key data points
2. **RESUMEN-EJECUTIVO.md** - Executive summary of all findings
3. **INSIGHTS-CREATIVOS.md** - Key insights for creative development

Place these in the root of `investigacion-pilsen-2025/`

---

For each document, include:
- Clear section headers
- Specific data points with sources
- Source URLs and access dates
- Reliability assessment

Begin with Phase 1 and proceed systematically through all phases.
```

---

## Alternative: Direct Research Request

If you prefer a more conversational approach:

```
I need to research for a Pilsen beer campaign in Paraguay targeting young adults 18-35 for end of year 2025.

Please systematically research:

1. **Market data**: Size, growth, key players in Paraguay beer market
2. **Brand info**: Pilsen history, campaigns, positioning
3. **Competition**: Main competitors, market shares
4. **Consumer**: Demographics, digital behavior, preferences of young Paraguayans
5. **Culture**: Local traditions, expressions (jopará), values
6. **Statistics**: Verified data points from official sources
7. **Creative**: Award-winning beer campaigns, viral content examples

For each topic:
- Use WebSearch to find relevant information
- Use WebFetch on the best 2-3 sources
- Compile findings with statistics and source citations

Create the output in investigacion-pilsen-2025/ with a markdown file for each topic.
```

---

## Expected Output Structure

After execution, you should have:

```
investigacion-pilsen-2025/
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
└── INSIGHTS-CREATIVOS.md
```

---

## Tips for Better Results

### 1. Be Specific with Queries
Instead of: "beer market Paraguay"
Use: "cerveza mercado Paraguay 2024 estadísticas tamaño"

### 2. Use Spanish for Local Results
Queries in Spanish yield better results for LATAM markets.

### 3. Request Source Triangulation
Ask Claude Code to find 3+ sources for key statistics.

### 4. Specify Output Format
Request specific data points you need:
- Market size in USD
- Growth percentage
- Market share percentages

### 5. Ask for Reliability Assessment
Request that sources be rated:
- High: Official government, industry reports
- Medium: News articles, market research
- Low: Blogs, social media

---

## Troubleshooting

### "No results found"
- Simplify the query
- Try English alternative
- Use broader terms

### "Cannot fetch URL"
- Some sites block automated access
- Note URL for manual review later
- Try alternative sources

### "Data conflicts between sources"
- Keep both data points
- Note the range (e.g., "88-92%")
- Prioritize official sources

---

## Next Steps After Research

1. Review all documents for completeness
2. Identify any gaps to fill
3. Create QUICK-REFERENCE if not generated
4. Begin ideation phase using research insights
