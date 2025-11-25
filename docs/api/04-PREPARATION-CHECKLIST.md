# Preparation Checklist

Everything you need to prepare before starting development on the Campaign Research Generator.

---

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [API Keys & Credentials](#api-keys--credentials)
3. [Software Installation](#software-installation)
4. [Project Structure](#project-structure)
5. [Configuration Files](#configuration-files)
6. [Templates to Create](#templates-to-create)
7. [Test Data](#test-data)
8. [Learning Resources](#learning-resources)
9. [Development Workflow](#development-workflow)
10. [Pre-Flight Checklist](#pre-flight-checklist)

---

## Environment Setup

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| Python | 3.11+ | API backend | python.org |
| Node.js | 18+ | n8n runtime | nodejs.org |
| n8n | Latest | Workflow automation | npm or Docker |
| Git | Latest | Version control | git-scm.com |
| Docker | Latest | Container deployment | docker.com |
| VS Code | Latest | Code editor | code.visualstudio.com |

### Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### n8n Installation Options

**Option 1: npm (Development)**
```bash
npm install n8n -g
n8n start
```

**Option 2: Docker (Production)**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option 3: Docker Compose (Recommended)**
```bash
# Will set up in project structure
docker-compose up -d
```

---

## API Keys & Credentials

### Required API Keys

| Service | Key Name | Get From | Cost |
|---------|----------|----------|------|
| Anthropic | ANTHROPIC_API_KEY | console.anthropic.com | Pay per use |
| OpenAI | OPENAI_API_KEY | platform.openai.com | Pay per use |

### Environment Variables File

Create `.env` in project root:

```bash
# .env

# AI Providers
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
OPENAI_API_KEY=sk-xxxxx

# API Configuration
PYTHON_API_URL=http://localhost:8000
PROJECTS_DIR=./projects

# n8n Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Optional
LOG_LEVEL=INFO
DEBUG=false
```

### n8n Credentials Setup

After n8n is running:
1. Go to **Credentials** in sidebar
2. Add **Anthropic** credential with API key
3. Add **OpenAI** credential with API key
4. Add **HTTP Header Auth** for Python API (if needed)

---

## Software Installation

### Python Dependencies

Create `requirements.txt`:

```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2

# Templates & Markdown
jinja2==3.1.2
markdown2==2.4.12

# File Operations
aiofiles==23.2.1
python-multipart==0.0.6
pyyaml==6.0.1

# HTTP & Validation
httpx==0.25.2
validators==0.22.0
beautifulsoup4==4.12.2

# PDF Generation
reportlab==4.0.7

# PowerPoint
python-pptx==0.6.23

# AI SDKs (for direct calls if needed)
anthropic==0.8.1
openai==1.6.1

# Development
pytest==7.4.3
pytest-asyncio==0.23.2
black==23.12.1
mypy==1.7.1
ruff==0.1.9
```

Install:
```bash
pip install -r requirements.txt
```

### VS Code Extensions

Recommended extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- YAML (redhat.vscode-yaml)
- REST Client (humao.rest-client)
- Docker (ms-azuretools.vscode-docker)
- GitLens (eamodio.gitlens)

---

## Project Structure

### Create Directory Structure

```bash
# Run from project root
mkdir -p code/api/services
mkdir -p code/api/templates
mkdir -p code/config/prompts
mkdir -p code/config/templates
mkdir -p code/tests
mkdir -p code/docs
mkdir -p projects
```

### Full Structure

```
code/
├── api/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── generator.py        # Project creation
│   │   ├── research.py         # Source management
│   │   ├── scoring.py          # Score calculation
│   │   ├── synthesis.py        # Content generation
│   │   └── export.py           # PDF/PPTX export
│   └── templates/
│       └── ... (Jinja2 templates)
│
├── config/
│   ├── default.yaml            # Default settings
│   ├── prompts/
│   │   ├── research_summary.txt
│   │   ├── brief_analysis.txt
│   │   ├── idea_generation.txt
│   │   └── quick_reference.txt
│   └── templates/
│       ├── idea.md.j2
│       ├── quick_reference.md.j2
│       ├── brief.md.j2
│       └── ...
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_generator.py
│   ├── test_scoring.py
│   └── ...
│
├── docs/
│   ├── 01-TECHNOLOGY-EVALUATION.md
│   ├── 02-FEATURE-SPECIFICATION.md
│   ├── 03-ARCHITECTURE.md
│   ├── 04-PREPARATION-CHECKLIST.md
│   └── 05-AI-PROMPTS.md
│
├── n8n/
│   └── workflows/              # Exported workflow JSONs
│
├── .env                        # Environment variables
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
└── pyproject.toml
```

---

## Configuration Files

### default.yaml

```yaml
# code/config/default.yaml

# Project defaults
project:
  default_country: "Paraguay"
  default_type: "digital"
  default_year: 2025
  num_ideas: 25

# Research categories
research:
  categories:
    - id: "01-mercado-general"
      name: "Mercado General"
      files: ["resumen-mercado.md", "tendencias.md"]
    - id: "02-marca"
      name: "Análisis de Marca"
      files: ["historia.md", "posicionamiento.md"]
    - id: "03-competencia"
      name: "Competencia"
      files: ["directa.md", "indirecta.md"]
    - id: "04-consumidor"
      name: "Consumidor"
      files: ["perfil.md", "comportamiento.md"]
    - id: "05-cultura"
      name: "Cultura"
      files: ["local.md", "tradiciones.md"]
    - id: "06-tendencias"
      name: "Tendencias"
      files: ["industria.md", "digital.md"]
    - id: "07-estadisticas"
      name: "Estadísticas"
      files: ["datos-clave.md"]
    - id: "08-referencias"
      name: "Referencias"
      files: ["fuentes-completas.md"]
    - id: "09-nuevos-hallazgos"
      name: "Nuevos Hallazgos"
      files: ["resumen.md"]
    - id: "10-investigacion-creativa"
      name: "Investigación Creativa"
      files:
        - "campanas-ganadoras.md"
        - "contenido-viral.md"
        - "comportamiento-digital.md"

# Scoring configuration
scoring:
  criteria:
    - name: "Diferenciación"
      weight: 1.0
      description: "¿Se destaca de la competencia?"
    - name: "Autenticidad"
      weight: 1.0
      description: "¿Es genuinamente cultural?"
    - name: "Potencial Viral"
      weight: 1.0
      description: "¿La gente lo compartirá?"
    - name: "Conexión Emocional"
      weight: 1.0
      description: "¿Genera engagement?"
    - name: "Ejecutabilidad"
      weight: 1.0
      description: "¿Es viable de producir?"
    - name: "Esencia de Marca"
      weight: 1.0
      description: "¿Mantiene identidad de marca?"
    - name: "Target Connection"
      weight: 1.0
      description: "¿Conecta con la audiencia?"
    - name: "Formato Digital"
      weight: 1.0
      description: "¿Funciona en redes sociales?"
    - name: "Memorable"
      weight: 1.0
      description: "¿Será recordado?"
    - name: "Valor al Consumidor"
      weight: 1.0
      description: "¿Agrega valor?"

  thresholds:
    very_high: 90
    high: 80
    medium: 70
    needs_work: 60

# AI configuration
ai:
  primary: "anthropic"
  fallback: "openai"

  anthropic:
    model: "claude-sonnet-4-20250514"
    max_tokens: 4096
    temperature: 0.7

  openai:
    model: "gpt-4-turbo"
    max_tokens: 4096
    temperature: 0.7

# Export settings
export:
  pdf:
    font_family: "Helvetica"
    font_size: 11
    margin: 72
    include_cover: true

  pptx:
    template: "default"
    include_notes: true
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    container_name: campaign-n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD:-changeme}
      - GENERIC_TIMEZONE=America/Asuncion
      - PYTHON_API_URL=http://api:8000
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - api
    networks:
      - campaign-network

  api:
    build:
      context: ./code/api
      dockerfile: Dockerfile
    container_name: campaign-api
    ports:
      - "8000:8000"
    environment:
      - PROJECTS_DIR=/data/projects
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - projects:/data/projects
      - ./code/config:/app/config:ro
    networks:
      - campaign-network

volumes:
  n8n_data:
  projects:

networks:
  campaign-network:
    driver: bridge
```

### Dockerfile for API

```dockerfile
# code/api/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.venv/
*.egg-info/

# Environment
.env
.env.local

# IDE
.idea/
.vscode/
*.swp

# n8n
.n8n/

# Output
projects/*/output/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Cache
.mypy_cache/
.pytest_cache/
```

---

## Templates to Create

### Jinja2 Templates

Create these in `code/config/templates/`:

#### idea.md.j2
```jinja2
# Idea {{ "%02d"|format(number) }}: "{{ name | default('[Nombre de la Idea]') }}"

## Concepto Central

{{ concept | default('[Una oración que describe la idea central]') }}

---

## Insight Clave

> "{{ insight | default('[Cita del research o brief que inspira esta idea]') }}"

---

## Ejecución

### Pieza 1: {{ piece1_name | default('[Nombre]') }}

**Visual**: {{ piece1_visual | default('[Descripción detallada de lo que se ve]') }}

**Copy**: "{{ piece1_copy | default('[Texto exacto del copy]') }}"

### Pieza 2: {{ piece2_name | default('[Nombre]') }}

**Visual**: {{ piece2_visual | default('[Descripción detallada de lo que se ve]') }}

**Copy**: "{{ piece2_copy | default('[Texto exacto del copy]') }}"

---

## Tono

{{ tone | default('[Adjetivos que describen el tono]') }}

---

## Por Qué Funciona

{% for reason in reasons | default(['[Razón 1]', '[Razón 2]', '[Razón 3]', '[Razón 4]']) %}
✅ {{ reason }}
{% endfor %}

---

## Potencial Viral

**{{ viral_potential | default('[ALTO/MEDIO/BAJO]') }}** - {{ viral_explanation | default('[Explicación]') }}

---

## KPIs Esperados

| Métrica | Proyección | Justificación |
|---------|------------|---------------|
| Alcance | {{ kpi_reach | default('[Alto/Medio/Bajo]') }} | {{ kpi_reach_why | default('[Por qué]') }} |
| Engagement | {{ kpi_engagement | default('[Alto/Medio/Bajo]') }} | {{ kpi_engagement_why | default('[Por qué]') }} |
| Viralidad | {{ kpi_viral | default('[Alto/Medio/Bajo]') }} | {{ kpi_viral_why | default('[Por qué]') }} |

---

## Posibles Variantes

{% for variant in variants | default(['[Variante A]', '[Variante B]', '[Variante C]']) %}
- **Variante {{ loop.index | string | upper }}**: {{ variant }}
{% endfor %}

---

## Puntuación

| Criterio | Puntaje (1-10) | Justificación |
|----------|----------------|---------------|
{% for criterion in criteria %}
| {{ criterion.name }} | /10 | |
{% endfor %}
| **TOTAL** | **/100** | |

---

**Fecha de creación**: {{ created_at | default('Noviembre 2024') }}
```

#### quick_reference.md.j2
```jinja2
# Quick Reference - {{ brand }}

> **{{ challenge | default('[Escribir el desafío principal en una frase]') }}**

---

## El Desafío en 1 Frase

> "{{ challenge_detail | default('[El challenge central de la campaña]') }}"

---

## Datos Clave del Mercado

| Métrica | Valor |
|---------|-------|
| Tamaño de mercado | {{ market_size | default('[Valor]') }} |
| Crecimiento | {{ market_growth | default('[%]') }} |
| Market share {{ brand }} | {{ market_share | default('[%]') }} |
| Principal competidor | {{ main_competitor | default('[Nombre]') }} |

---

## Target en 30 Segundos

- **Quién**: {{ target_who | default('[Descripción corta]') }}
- **Edad**: {{ target_age | default('[Rango]') }}
- **Motivación**: {{ target_motivation | default('[Principal driver]') }}
- **Barrera**: {{ target_barrier | default('[Principal obstáculo]') }}
- **Medios**: {{ target_media | default('[Dónde están]') }}

---

## Insights Clave

| Problema | Realidad | Oportunidad |
|----------|----------|-------------|
{% for insight in insights | default([]) %}
| {{ insight.problem }} | {{ insight.reality }} | {{ insight.opportunity }} |
{% endfor %}

---

## ❌ Qué NO Hacer

{% for dont in donts | default(['[No hacer 1]', '[No hacer 2]', '[No hacer 3]']) %}
{{ loop.index }}. ❌ {{ dont }}
{% endfor %}

---

## ✅ Qué SÍ Hacer

{% for do in dos | default(['[Sí hacer 1]', '[Sí hacer 2]', '[Sí hacer 3]']) %}
{{ loop.index }}. ✅ {{ do }}
{% endfor %}

---

## Direcciones Creativas

{% for direction in directions | default([]) %}
### {{ loop.index }}. "{{ direction.name }}"
{{ direction.description }}

{% endfor %}

---

## Preguntas para Brainstorming

{% for question in questions | default(['[Pregunta 1]', '[Pregunta 2]', '[Pregunta 3]']) %}
{{ loop.index }}. {{ question }}
{% endfor %}

---

**Última actualización**: {{ updated_at | default('Noviembre 2024') }}
```

---

## Test Data

### Sample Project for Testing

Create test data in `code/tests/fixtures/`:

#### test_project/
```
test_project/
├── README.md
├── investigacion-test-paraguay/
│   ├── 01-mercado-general/
│   │   └── resumen-mercado.md (with sample content)
│   ├── 08-referencias/
│   │   └── fuentes-completas.md (with 5 test sources)
│   └── BRIEF-CAMPANA.md
└── ideas/
    ├── 00-RESUMEN-IDEAS.md
    ├── idea-01-test.md (with complete scores)
    ├── idea-02-test.md (with complete scores)
    └── idea-03-test.md (with partial scores)
```

#### Sample idea-01-test.md
```markdown
# Idea 01: "Test Idea One"

## Concepto Central
This is a test idea for development.

## Puntuación

| Criterio | Puntaje (1-10) | Justificación |
|----------|----------------|---------------|
| Diferenciación | 8/10 | Unique approach |
| Autenticidad | 7/10 | Culturally relevant |
| Potencial Viral | 9/10 | High shareability |
| Conexión Emocional | 8/10 | Strong emotional hook |
| Ejecutabilidad | 6/10 | Complex but feasible |
| Esencia de Marca | 8/10 | On brand |
| Target Connection | 9/10 | Perfect for audience |
| Formato Digital | 8/10 | Social-first |
| Memorable | 7/10 | Sticky concept |
| Valor al Consumidor | 8/10 | Clear benefit |
| **TOTAL** | **78/100** | |
```

---

## Learning Resources

### n8n
- [n8n Documentation](https://docs.n8n.io/)
- [n8n Course](https://docs.n8n.io/courses/)
- [n8n Community](https://community.n8n.io/)
- [Claude Node Documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatanthropic/)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Claude API
- [Anthropic Documentation](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/en/api/getting-started)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

### Jinja2
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Jinja2 Template Designer](https://jinja.palletsprojects.com/en/3.1.x/templates/)

### ReportLab
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [ReportLab Reference](https://docs.reportlab.com/)

---

## Development Workflow

### Daily Workflow

1. **Start services**
   ```bash
   # Terminal 1: Start n8n
   n8n start

   # Terminal 2: Start Python API
   cd code/api
   uvicorn main:app --reload
   ```

2. **Develop**
   - Write code in VS Code
   - Test endpoints with REST Client or curl
   - Build/test n8n workflows

3. **Test**
   ```bash
   pytest code/tests/ -v
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: description"
   ```

### Git Workflow

- `main` - Production ready
- `develop` - Integration branch
- `feature/*` - Feature branches
- `fix/*` - Bug fix branches

Commit format:
```
type: description

- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Adding tests
```

---

## Pre-Flight Checklist

### Before Writing Any Code

#### Environment
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] All Python dependencies installed
- [ ] n8n installed and running
- [ ] Docker installed (for production)

#### API Keys
- [ ] Anthropic API key obtained
- [ ] OpenAI API key obtained
- [ ] Keys added to .env file
- [ ] Keys tested with simple API call

#### Configuration
- [ ] .env file created with all variables
- [ ] default.yaml created with settings
- [ ] docker-compose.yml ready

#### Project Structure
- [ ] All directories created
- [ ] __init__.py files in place
- [ ] .gitignore configured

#### Templates
- [ ] Jinja2 templates created
- [ ] AI prompts written
- [ ] Test data prepared

#### Documentation
- [ ] All 5 docs reviewed
- [ ] Architecture understood
- [ ] Features clear

#### n8n Setup
- [ ] n8n running and accessible
- [ ] Anthropic credential added
- [ ] OpenAI credential added
- [ ] Test workflow working

#### First Test
- [ ] FastAPI app starts without errors
- [ ] Health endpoint returns 200
- [ ] n8n can call Python API

---

## Quick Start Commands

### Full Setup Script

```bash
#!/bin/bash
# setup.sh - Run from project root

# Create directories
mkdir -p code/api/services
mkdir -p code/config/prompts
mkdir -p code/config/templates
mkdir -p code/tests/fixtures
mkdir -p projects

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
echo "Edit .env with your API keys"

# Initialize empty files
touch code/api/__init__.py
touch code/api/services/__init__.py
touch code/tests/__init__.py

# Done
echo "Setup complete! Edit .env and run: uvicorn code.api.main:app --reload"
```

### Development Start Script

```bash
#!/bin/bash
# dev.sh - Start development environment

# Start n8n in background
n8n start &

# Wait for n8n
sleep 5

# Start FastAPI with reload
cd code/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Next: AI Prompts Document

The final document will cover all AI prompts needed for the system.
