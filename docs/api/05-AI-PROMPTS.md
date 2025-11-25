# AI Prompt Engineering Guide

Complete collection of AI prompts for the Campaign Research Generator system.

---

## Table of Contents

1. [Prompt Engineering Principles](#prompt-engineering-principles)
2. [Research Prompts](#research-prompts)
3. [Brief Analysis Prompts](#brief-analysis-prompts)
4. [Synthesis Prompts](#synthesis-prompts)
5. [Idea Generation Prompts](#idea-generation-prompts)
6. [Quality Control Prompts](#quality-control-prompts)
7. [n8n Node Configuration](#n8n-node-configuration)
8. [Prompt Testing Strategy](#prompt-testing-strategy)

---

## Prompt Engineering Principles

### For This Project

1. **Always output in Spanish** - All generated content must be in Spanish
2. **Marketing context** - Claude should understand it's assisting marketing research
3. **Cultural awareness** - Prompts should emphasize Paraguay/Latin America context
4. **Structured output** - Request JSON or specific formats for parsing
5. **Concise outputs** - Specify character/word limits to avoid bloat
6. **Actionable insights** - Focus on information useful for creative development

### Claude Best Practices

```
1. Be specific about format needed
2. Provide examples when helpful
3. Set clear constraints (length, language, format)
4. Use system prompts for consistent behavior
5. Break complex tasks into steps
6. Request confidence indicators when appropriate
```

---

## Research Prompts

### PROMPT-001: Research Content Summary

**Purpose**: Summarize web article content for research database

**Use in**: WF-101 (Add Source workflow)

```
SYSTEM:
Eres un analista de investigación de mercado especializado en mercados latinoamericanos. Tu trabajo es extraer información relevante para campañas publicitarias.

USER:
Resume el siguiente contenido para un proyecto de investigación de campaña publicitaria.

Enfócate en:
1. Estadísticas y datos numéricos clave
2. Insights sobre comportamiento del consumidor
3. Información competitiva
4. Tendencias del mercado
5. Oportunidades para comunicación

Contenido:
{content}

Responde en español.
Máximo 500 caracteres.
Formato: Párrafo conciso con datos específicos.
```

**Expected Output**:
```
El mercado cervecero paraguayo alcanzó USD 832M en 2024, con Pilsen liderando con 45% del market share. El consumo per cápita es de 35L/año, concentrado en diciembre (40% del consumo anual). Los consumidores 18-35 prefieren compra en supermercados (60%) y valoran tradición sobre precio.
```

---

### PROMPT-002: Extract Key Statistics

**Purpose**: Pull specific numbers from research content

**Use in**: Quick Reference generation

```
SYSTEM:
Eres un analista de datos que extrae métricas clave de documentos de investigación.

USER:
Extrae las estadísticas clave de este contenido de investigación.

Contenido:
{content}

Responde en JSON con este formato:
{
  "market_size": "valor con unidad",
  "growth_rate": "porcentaje",
  "market_share": "porcentaje de la marca",
  "main_competitor": "nombre y share",
  "key_metrics": ["métrica 1", "métrica 2", "métrica 3"]
}

Si un dato no está disponible, usa null.
```

---

### PROMPT-003: Source Categorization

**Purpose**: Auto-categorize source type

**Use in**: Source management

```
USER:
Clasifica esta fuente en una categoría.

URL: {url}
Título: {title}

Categorías posibles:
- media: Medios de comunicación (periódicos, revistas, portales de noticias)
- corporate: Fuentes corporativas (reportes de empresa, comunicados de prensa)
- study: Estudios e informes (consultoras, investigación de mercado)
- institutional: Fuentes institucionales (gobierno, cámaras, asociaciones)

Responde solo con el nombre de la categoría en minúsculas.
```

---

## Brief Analysis Prompts

### PROMPT-010: Extract Core Challenge

**Purpose**: Identify the main challenge from campaign brief

**Use in**: WF-201 (Analyze Brief)

```
SYSTEM:
Eres un estratega creativo senior analizando briefs de campañas publicitarias.

USER:
Analiza este brief de campaña y extrae el desafío central.

Brief:
{brief_content}

Responde en JSON:
{
  "main_challenge": "El desafío principal en una oración",
  "context": "Por qué es un desafío (2-3 oraciones)",
  "constraints": [
    "Restricción o limitación 1",
    "Restricción o limitación 2",
    "Restricción o limitación 3"
  ],
  "success_looks_like": "Cómo se ve el éxito (1 oración)"
}
```

---

### PROMPT-011: Extract Target Audience

**Purpose**: Parse target audience details from brief

**Use in**: WF-201 (Analyze Brief)

```
SYSTEM:
Eres un planificador de medios extrayendo perfiles de audiencia.

USER:
Extrae el perfil del público objetivo de este brief.

Brief:
{brief_content}

Responde en JSON:
{
  "demographics": {
    "age_range": "rango de edad",
    "gender": "distribución de género",
    "location": "ubicación geográfica",
    "socioeconomic": "nivel socioeconómico"
  },
  "psychographics": {
    "interests": ["interés 1", "interés 2", "interés 3"],
    "values": ["valor 1", "valor 2"],
    "lifestyle": "descripción del estilo de vida"
  },
  "media_consumption": {
    "primary_platforms": ["plataforma 1", "plataforma 2"],
    "peak_times": "horarios de mayor consumo",
    "content_preferences": ["preferencia 1", "preferencia 2"]
  },
  "one_sentence_profile": "Descripción del target en una oración"
}
```

---

### PROMPT-012: Suggest Creative Directions

**Purpose**: Generate strategic creative directions from brief

**Use in**: WF-201 (Analyze Brief)

```
SYSTEM:
Eres un director creativo generando direcciones estratégicas para campañas.

USER:
Basándote en este brief, sugiere 3 direcciones creativas distintas.

Brief:
{brief_content}

Para cada dirección incluye:
- Nombre memorable (2-3 palabras)
- Descripción (1 oración)
- Insight que la soporta
- Tono sugerido
- Riesgo principal

Responde en JSON:
{
  "directions": [
    {
      "name": "Nombre de la Dirección",
      "description": "Descripción en una oración",
      "insight": "El insight humano que la soporta",
      "tone": ["adjetivo1", "adjetivo2"],
      "risk": "Principal riesgo o consideración"
    }
  ]
}

Las direcciones deben ser:
1. Una segura/esperada
2. Una arriesgada/diferente
3. Una balanceada
```

---

### PROMPT-013: Extract Brand Requirements

**Purpose**: Identify brand voice and restrictions

**Use in**: WF-201 (Analyze Brief)

```
USER:
Extrae los requisitos y restricciones de marca de este brief.

Brief:
{brief_content}

Responde en JSON:
{
  "tone_of_voice": ["adjetivo 1", "adjetivo 2", "adjetivo 3"],
  "must_include": ["elemento obligatorio 1", "elemento obligatorio 2"],
  "must_avoid": ["elemento prohibido 1", "elemento prohibido 2"],
  "visual_guidelines": "descripción de lineamientos visuales",
  "messaging_pillars": ["pilar 1", "pilar 2"],
  "competitive_differentiation": "cómo debe diferenciarse de competencia"
}
```

---

## Synthesis Prompts

### PROMPT-020: Generate Quick Reference Data

**Purpose**: Extract key information for quick reference

**Use in**: WF-203 (Generate Quick Reference)

```
SYSTEM:
Eres un estratega sintetizando investigación en información accionable.

USER:
Analiza esta investigación y extrae la información clave para una referencia rápida de brainstorming.

Investigación:
{research_content}

Responde en JSON:
{
  "challenge_one_liner": "El desafío en una frase impactante",

  "market_snapshot": {
    "size": "tamaño del mercado",
    "growth": "crecimiento",
    "brand_share": "participación de la marca",
    "main_competitor": "principal competidor"
  },

  "target_30_seconds": {
    "who": "descripción en una oración",
    "age": "rango de edad",
    "motivation": "motivación principal",
    "barrier": "barrera principal",
    "media": "dónde están"
  },

  "key_insights": [
    {
      "problem": "el problema",
      "reality": "la realidad",
      "opportunity": "la oportunidad"
    }
  ],

  "dos": [
    "Qué SÍ hacer 1",
    "Qué SÍ hacer 2",
    "Qué SÍ hacer 3",
    "Qué SÍ hacer 4",
    "Qué SÍ hacer 5"
  ],

  "donts": [
    "Qué NO hacer 1",
    "Qué NO hacer 2",
    "Qué NO hacer 3",
    "Qué NO hacer 4",
    "Qué NO hacer 5"
  ],

  "brainstorm_questions": [
    "Pregunta provocativa 1",
    "Pregunta provocativa 2",
    "Pregunta provocativa 3",
    "Pregunta provocativa 4",
    "Pregunta provocativa 5"
  ]
}
```

---

### PROMPT-021: Generate Insights Table

**Purpose**: Create problem-reality-opportunity insights

**Use in**: Quick Reference generation

```
USER:
Genera 3-5 insights clave en formato problema-realidad-oportunidad.

Investigación:
{research_content}

Brief:
{brief_summary}

Responde en JSON:
{
  "insights": [
    {
      "problem": "Lo que la gente asume o el desafío visible",
      "reality": "Lo que realmente está pasando",
      "opportunity": "Cómo la marca puede aprovecharlo"
    }
  ]
}

Cada insight debe ser:
- Accionable para creatividad
- Específico (con datos cuando sea posible)
- Relevante para la estrategia de campaña
```

---

### PROMPT-022: Generate Do's and Don'ts

**Purpose**: Create clear guidelines for creative work

**Use in**: Quick Reference generation

```
USER:
Basándote en esta investigación y brief, genera listas de Qué SÍ hacer y Qué NO hacer para el equipo creativo.

Investigación:
{research_content}

Brief:
{brief_summary}

Genera exactamente 5 de cada uno.

Responde en JSON:
{
  "dos": [
    "✅ Acción específica y clara que SÍ hacer"
  ],
  "donts": [
    "❌ Acción específica y clara que NO hacer"
  ]
}

Deben ser:
- Específicos (no genéricos)
- Accionables (que el equipo sepa exactamente qué hacer)
- Basados en la investigación
- Relevantes para este brief específico
```

---

## Idea Generation Prompts

### PROMPT-030: Generate Idea Concepts

**Purpose**: Generate initial campaign idea concepts

**Use in**: WF-202 (Generate Ideas) - optional assist

```
SYSTEM:
Eres un creativo senior generando conceptos de campaña. Tus ideas deben ser originales, culturalmente relevantes, y ejecutables.

USER:
Genera {num_ideas} conceptos de ideas de campaña basándote en:

Brief resumido:
{brief_summary}

Investigación clave:
{research_summary}

Para cada idea proporciona:
1. Nombre (2-4 palabras, memorable)
2. Concepto (1 oración clara)
3. Insight (la verdad humana que la soporta)
4. Ejecución (cómo se vería una pieza)
5. Por qué funciona (3 razones)

Responde en JSON:
{
  "ideas": [
    {
      "name": "Nombre de la Idea",
      "concept": "El concepto en una oración",
      "insight": "El insight que la soporta",
      "execution": {
        "format": "tipo de pieza",
        "visual": "descripción visual",
        "copy": "texto principal"
      },
      "why_it_works": [
        "Razón 1",
        "Razón 2",
        "Razón 3"
      ]
    }
  ]
}

Las ideas deben:
- Ser diversas en tono y enfoque
- Conectar con insights documentados
- Considerar el contexto cultural de {country}
- Alinearse con la voz de marca
- Variar en nivel de riesgo
```

---

### PROMPT-031: Expand Idea Concept

**Purpose**: Develop a single idea into full detail

**Use in**: Manual idea development

```
USER:
Expande este concepto de idea en una propuesta completa.

Concepto: {concept_name}
Descripción: {concept_description}

Desarrolla:
1. Ejecución detallada (2-3 piezas)
2. Posibles variantes
3. Adaptaciones por formato (social, OOH, video)
4. Riesgos y mitigaciones
5. KPIs esperados

Responde en español con el formato del template de idea.
```

---

## Quality Control Prompts

### PROMPT-040: Validate Idea Quality

**Purpose**: Check if an idea meets quality standards

**Use in**: Quality assurance

```
USER:
Evalúa esta idea de campaña contra criterios de calidad.

Idea:
{idea_content}

Evalúa en escala 1-10:
1. ¿Tiene un concepto claro y único?
2. ¿El insight es verdadero y relevante?
3. ¿La ejecución es clara y visualizable?
4. ¿Funciona para el formato requerido?
5. ¿Está alineada con la marca?

Responde en JSON:
{
  "scores": {
    "concept_clarity": 8,
    "insight_strength": 7,
    "execution_clarity": 9,
    "format_fit": 8,
    "brand_alignment": 7
  },
  "overall": 7.8,
  "strengths": ["fortaleza 1", "fortaleza 2"],
  "weaknesses": ["debilidad 1"],
  "suggestions": ["sugerencia de mejora 1"]
}
```

---

### PROMPT-041: Check Cultural Relevance

**Purpose**: Validate cultural appropriateness

**Use in**: Quality assurance for Paraguay/Latin America

```
USER:
Evalúa la relevancia cultural de esta idea para Paraguay.

Idea:
{idea_content}

Considera:
1. ¿Respeta tradiciones locales?
2. ¿Usa lenguaje apropiado (español/guaraní)?
3. ¿Evita estereotipos negativos?
4. ¿Conecta con valores locales?
5. ¿Es apropiada para el clima/temporada?

Responde en JSON:
{
  "cultural_score": 8,
  "positives": ["aspecto positivo 1"],
  "concerns": ["preocupación 1"],
  "suggestions": ["sugerencia 1"],
  "approved": true
}
```

---

## n8n Node Configuration

### Claude Node Setup

**For all Claude nodes in n8n:**

```yaml
Model: claude-sonnet-4-20250514
Temperature: 0.7  # Balance creativity/consistency
Max Tokens: 4096  # Allow full responses
Top P: 1
```

### Example n8n Claude Node

```json
{
  "parameters": {
    "model": "claude-sonnet-4-20250514",
    "prompt": {
      "messages": [
        {
          "role": "system",
          "content": "Eres un analista de investigación de mercado..."
        },
        {
          "role": "user",
          "content": "={{ $json.prompt }}"
        }
      ]
    },
    "options": {
      "temperature": 0.7,
      "maxTokensToSample": 4096
    }
  }
}
```

### Credential Configuration

In n8n Credentials:
1. **Anthropic API**
   - API Key: Your ANTHROPIC_API_KEY

2. **OpenAI API** (fallback)
   - API Key: Your OPENAI_API_KEY

---

## Prompt Testing Strategy

### Test Each Prompt

Before using in production:

1. **Test with sample data**
   - Use test project content
   - Verify JSON output parses correctly
   - Check Spanish language quality

2. **Test edge cases**
   - Very short input
   - Very long input
   - Missing sections
   - Non-Spanish content

3. **Test output quality**
   - Is it actionable?
   - Is it specific enough?
   - Does it match expected format?

### Prompt Testing Template

```python
# test_prompts.py

import anthropic
import json

def test_prompt(prompt_name: str, test_input: str):
    client = anthropic.Anthropic()

    # Load prompt template
    with open(f"config/prompts/{prompt_name}.txt") as f:
        template = f.read()

    # Fill template
    prompt = template.format(content=test_input)

    # Call Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.content[0].text

    # Validate JSON if expected
    try:
        parsed = json.loads(result)
        print(f"✅ {prompt_name}: Valid JSON")
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(f"⚠️ {prompt_name}: Not JSON (may be expected)")
        print(result)

    return result

# Test research summary
test_prompt("research_summary", """
El mercado de cerveza en Paraguay alcanzó ventas de USD 832 millones en 2024,
con un crecimiento del 5% respecto al año anterior. Pilsen lidera con 45% del
market share, seguido por Brahma con 30% y Bavaria con 15%.
""")
```

### Quality Checklist for Prompts

- [ ] Output is in Spanish
- [ ] JSON parses correctly (if JSON expected)
- [ ] Length is within limits
- [ ] Content is relevant to marketing/advertising
- [ ] Includes specific data when available
- [ ] Avoids generic/filler content
- [ ] Maintains consistent format
- [ ] Works with edge cases

---

## Prompt File Organization

Store prompts in `code/config/prompts/`:

```
prompts/
├── research/
│   ├── summary.txt
│   ├── statistics.txt
│   └── categorize.txt
│
├── brief/
│   ├── challenge.txt
│   ├── target.txt
│   ├── directions.txt
│   └── requirements.txt
│
├── synthesis/
│   ├── quick_reference.txt
│   ├── insights.txt
│   └── dos_donts.txt
│
├── ideas/
│   ├── generate.txt
│   └── expand.txt
│
└── quality/
    ├── validate.txt
    └── cultural.txt
```

---

## Prompt Versioning

Track prompt versions for A/B testing:

```yaml
# prompts/metadata.yaml

prompts:
  research_summary:
    version: "1.2"
    last_updated: "2024-01-15"
    performance:
      accuracy: 0.85
      user_satisfaction: 4.2/5

  brief_challenge:
    version: "2.0"
    last_updated: "2024-01-20"
    changes: "Added constraints extraction"
    performance:
      accuracy: 0.90
      user_satisfaction: 4.5/5
```

---

## Common Prompt Patterns

### For Structured Output
```
Responde en JSON:
{
  "field": "value"
}
```

### For Lists
```
Genera exactamente N elementos.
Responde como array JSON.
```

### For Constraints
```
Máximo X caracteres.
En español.
Enfócate en [specific aspect].
```

### For Context
```
Eres un [role] especializado en [domain].
Tu objetivo es [goal].
```

### For Quality
```
Deben ser:
- Específicos (no genéricos)
- Accionables
- Basados en los datos
```

---

## Summary

This document contains all AI prompts needed for the Campaign Research Generator:

| Category | Prompts | Purpose |
|----------|---------|---------|
| Research | 3 | Summarize, extract stats, categorize |
| Brief | 4 | Challenge, target, directions, requirements |
| Synthesis | 3 | Quick reference, insights, dos/donts |
| Ideas | 2 | Generate, expand |
| Quality | 2 | Validate, cultural check |

**Total: 14 core prompts**

All prompts are designed to:
- Output in Spanish
- Return structured JSON when possible
- Focus on actionable marketing insights
- Respect cultural context
- Be specific and avoid generic content

---

## Next Steps

With all documentation complete, you're ready to:

1. Set up the development environment
2. Create the Python API skeleton
3. Build the first n8n workflow
4. Test prompts with real content
5. Iterate and improve
