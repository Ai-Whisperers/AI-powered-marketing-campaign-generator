# Additional Preparation Requirements

Items that need to be prepared before starting development that weren't covered in previous documents.

---

## Table of Contents

1. [n8n Workflow Templates](#n8n-workflow-templates)
2. [Sample Data & Test Fixtures](#sample-data--test-fixtures)
3. [Error Handling & Logging](#error-handling--logging)
4. [Security Considerations](#security-considerations)
5. [Monitoring & Observability](#monitoring--observability)
6. [Backup & Recovery](#backup--recovery)
7. [Cost Estimation](#cost-estimation)
8. [Rate Limiting Strategy](#rate-limiting-strategy)
9. [Internationalization](#internationalization)
10. [Documentation for End Users](#documentation-for-end-users)
11. [CI/CD Pipeline](#cicd-pipeline)
12. [Development Standards](#development-standards)

---

## 1. n8n Workflow Templates

### Workflow Export Format

Before building, prepare empty workflow templates:

#### Base Workflow Structure
```json
{
  "name": "WF-001: Create New Project",
  "nodes": [],
  "connections": {},
  "settings": {
    "executionOrder": "v1",
    "saveManualExecutions": true,
    "callerPolicy": "workflowsFromSameOwner"
  },
  "staticData": null,
  "tags": [
    {"name": "campaign-generator"},
    {"name": "core"}
  ]
}
```

### Workflow Naming Convention
```
WF-0XX: Campaign management
WF-1XX: Research management
WF-2XX: AI-powered features
WF-3XX: Scoring & reporting
WF-4XX: Export features
WF-9XX: Utility/maintenance
```

### Workflow Documentation Template

Create for each workflow:
```markdown
# WF-XXX: Workflow Name

## Purpose
[What this workflow does]

## Trigger
- Type: [Webhook/Manual/Schedule]
- Endpoint: [if webhook]

## Input
```json
{
  "field": "type and description"
}
```

## Output
```json
{
  "field": "type and description"
}
```

## Nodes
1. [Node name] - [Purpose]
2. [Node name] - [Purpose]

## Error Handling
- [Error case] → [How handled]

## Dependencies
- Requires: [Other workflows or services]

## Testing
- [Test case 1]
- [Test case 2]
```

---

## 2. Sample Data & Test Fixtures

### Test Project Structure

Create `code/tests/fixtures/sample-project/`:

```
sample-project/
├── campana-testbrand-2025/
│   ├── README.md
│   ├── investigacion-testbrand-paraguay/
│   │   ├── README.md
│   │   ├── 01-mercado-general/
│   │   │   └── resumen-mercado.md
│   │   ├── 04-consumidor/
│   │   │   └── perfil.md
│   │   ├── 08-referencias/
│   │   │   └── fuentes-completas.md
│   │   ├── BRIEF-CAMPANA.md
│   │   └── QUICK-REFERENCE.md
│   └── ideas/
│       ├── 00-RESUMEN-IDEAS.md
│       ├── idea-01-complete.md    # Full scoring
│       ├── idea-02-partial.md     # Partial scoring
│       └── idea-03-empty.md       # No scoring
```

### Sample Research Content

**resumen-mercado.md:**
```markdown
# Resumen del Mercado

## Resumen Ejecutivo

El mercado de [industria] en Paraguay alcanzó USD 500M en 2024, con un crecimiento del 5% anual. TestBrand lidera con 40% del market share.

## Datos Clave

| Métrica | Valor |
|---------|-------|
| Tamaño del mercado | USD 500M |
| Crecimiento anual | 5% |
| Market share TestBrand | 40% |
| Principal competidor | CompetidorX (30%) |

## Referencias

- Fuente Test 1 (2024)
- Fuente Test 2 (2024)
```

### Sample Idea with Full Scoring

**idea-01-complete.md:**
```markdown
# Idea 01: "Test Idea Completa"

## Concepto Central

Esta es una idea de prueba con puntuación completa para testing.

## Insight Clave

> "Los consumidores paraguayos valoran la autenticidad sobre todo."

## Ejecución

### Pieza 1: Post Social

**Visual**: Imagen de producto con fondo cultural paraguayo

**Copy**: "Lo auténtico siempre gana"

## Tono

Auténtico, cercano, orgulloso

## Por Qué Funciona

✅ Conecta con el valor de autenticidad
✅ Simple y memorable
✅ Adaptable a múltiples formatos
✅ Diferenciado de competencia

## Puntuación

| Criterio | Puntaje (1-10) | Justificación |
|----------|----------------|---------------|
| Diferenciación | 8/10 | Único en el mercado |
| Autenticidad | 9/10 | Muy cultural |
| Potencial Viral | 7/10 | Compartible |
| Conexión Emocional | 8/10 | Genera orgullo |
| Ejecutabilidad | 9/10 | Fácil de producir |
| Esencia de Marca | 8/10 | Alineado |
| Target Connection | 8/10 | Relevante |
| Formato Digital | 8/10 | Social-first |
| Memorable | 7/10 | Pegajoso |
| Valor al Consumidor | 8/10 | Claro beneficio |
| **TOTAL** | **80/100** | |
```

### Sample Sources File

**fuentes-completas.md:**
```markdown
# Fuentes Completas

## Resumen

| Categoría | Cantidad |
|-----------|----------|
| Medios | 2 |
| Corporativas | 1 |
| Estudios | 1 |
| Institucionales | 1 |
| **Total** | **5** |

## Medios de Comunicación

- [Artículo Test 1](https://example.com/test1) - Mercado general (2024)
- [Artículo Test 2](https://example.com/test2) - Competencia (2024)

## Fuentes Corporativas

- [Reporte Anual TestBrand](https://example.com/report) - Resultados 2024

## Estudios e Informes

- [Estudio de Mercado](https://example.com/study) - Tendencias 2024

## Fuentes Institucionales

- [Datos Gobierno](https://example.com/gov) - Estadísticas oficiales
```

### API Test Fixtures

**conftest.py:**
```python
import pytest
from pathlib import Path
import shutil
import tempfile

@pytest.fixture
def sample_project_path():
    """Path to sample test project."""
    return Path(__file__).parent / "fixtures" / "sample-project" / "campana-testbrand-2025"

@pytest.fixture
def temp_project(sample_project_path):
    """Create temporary copy of sample project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir) / "campana-testbrand-2025"
        shutil.copytree(sample_project_path, dest)
        yield dest

@pytest.fixture
def sample_brief():
    """Sample brief content for testing."""
    return """
    # Brief de Campaña - TestBrand

    ## Desafío
    Aumentar awareness en el segmento joven (18-35).

    ## Target
    Jóvenes urbanos, NSE ABC1, digitales.

    ## Tono
    Fresco, auténtico, divertido.
    """

@pytest.fixture
def sample_research():
    """Sample research content for testing."""
    return """
    El mercado alcanzó USD 500M con 5% de crecimiento.
    TestBrand lidera con 40% del market share.
    Los consumidores valoran autenticidad y precio.
    """
```

---

## 3. Error Handling & Logging

### Error Categories

```python
# code/api/exceptions.py

from fastapi import HTTPException

class CampaignGeneratorError(Exception):
    """Base exception for all custom errors."""
    pass

class ProjectNotFoundError(CampaignGeneratorError):
    """Project does not exist."""
    def __init__(self, project_id: str):
        self.project_id = project_id
        super().__init__(f"Project not found: {project_id}")

class ProjectExistsError(CampaignGeneratorError):
    """Project already exists."""
    def __init__(self, project_id: str):
        self.project_id = project_id
        super().__init__(f"Project already exists: {project_id}")

class InvalidSourceError(CampaignGeneratorError):
    """Source URL is invalid or inaccessible."""
    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(f"Invalid source {url}: {reason}")

class ScoringError(CampaignGeneratorError):
    """Error in scoring calculation."""
    def __init__(self, idea: str, reason: str):
        self.idea = idea
        self.reason = reason
        super().__init__(f"Scoring error for {idea}: {reason}")

class AIServiceError(CampaignGeneratorError):
    """Error from AI service."""
    def __init__(self, provider: str, reason: str):
        self.provider = provider
        self.reason = reason
        super().__init__(f"AI error ({provider}): {reason}")

class TemplateError(CampaignGeneratorError):
    """Error rendering template."""
    def __init__(self, template: str, reason: str):
        self.template = template
        self.reason = reason
        super().__init__(f"Template error {template}: {reason}")

class ExportError(CampaignGeneratorError):
    """Error exporting to PDF/PPTX."""
    def __init__(self, format: str, reason: str):
        self.format = format
        self.reason = reason
        super().__init__(f"Export error ({format}): {reason}")
```

### Logging Configuration

```python
# code/api/logging_config.py

import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: Path = None):
    """Configure logging for the application."""

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File handler (if specified)
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=handlers
    )

    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging.getLogger("campaign_generator")
```

### Logging Usage

```python
# In API endpoints
import logging

logger = logging.getLogger("campaign_generator")

@app.post("/api/projects")
async def create_project(data: ProjectCreate):
    logger.info(f"Creating project: {data.brand}")

    try:
        result = creator.create(...)
        logger.info(f"Project created: {result.path}")
        return result
    except Exception as e:
        logger.error(f"Failed to create project: {e}", exc_info=True)
        raise
```

### n8n Error Workflow

Create a global error handler workflow:

```yaml
name: "Error Handler"
nodes:
  - type: Error Trigger

  - type: Set
    values:
      error_workflow: "={{ $workflow.name }}"
      error_node: "={{ $execution.error.node }}"
      error_message: "={{ $execution.error.message }}"
      timestamp: "={{ new Date().toISOString() }}"

  - type: IF
    condition: "={{ $json.error_message.includes('rate limit') }}"
    true: Retry Logic
    false: Notification

  - type: Wait
    name: Retry Logic
    amount: 60
    unit: seconds
    then: Execute Workflow

  - type: HTTP Request
    name: Notification
    url: "{{ $env.SLACK_WEBHOOK }}"  # Or email
    body:
      text: "Error in {{ $json.error_workflow }}: {{ $json.error_message }}"
```

---

## 4. Security Considerations

### API Key Management

```python
# Never hardcode keys
import os

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set")

# Validate key format
if not ANTHROPIC_KEY.startswith("sk-ant-"):
    raise ValueError("Invalid Anthropic API key format")
```

### Input Validation

```python
from pydantic import BaseModel, validator, HttpUrl
import re

class ProjectCreate(BaseModel):
    brand: str
    country: str = "Paraguay"

    @validator("brand")
    def validate_brand(cls, v):
        # Only alphanumeric and spaces
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", v):
            raise ValueError("Brand name contains invalid characters")
        if len(v) > 50:
            raise ValueError("Brand name too long (max 50)")
        return v.strip()

class SourceCreate(BaseModel):
    url: HttpUrl  # Validates URL format
    title: str

    @validator("title")
    def validate_title(cls, v):
        if len(v) > 200:
            raise ValueError("Title too long (max 200)")
        return v.strip()
```

### File Path Safety

```python
from pathlib import Path

def safe_path(base: Path, user_input: str) -> Path:
    """Prevent directory traversal attacks."""
    # Resolve to absolute paths
    base = base.resolve()
    target = (base / user_input).resolve()

    # Ensure target is under base
    if not str(target).startswith(str(base)):
        raise ValueError("Invalid path: directory traversal detected")

    return target
```

### n8n Security

```yaml
# In n8n environment
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=strong-password-here

# Restrict webhook access
N8N_ENDPOINT_WEBHOOK_AUTHORIZED=true
```

---

## 5. Monitoring & Observability

### Health Check Endpoint

```python
from datetime import datetime

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "checks": {
            "api": "ok",
            "projects_dir": Path(PROJECTS_DIR).exists(),
            "templates": Path(TEMPLATES_DIR).exists()
        }
    }

@app.get("/health/detailed")
async def health_detailed():
    # Check AI connectivity
    ai_status = await check_ai_connectivity()

    return {
        "status": "healthy" if ai_status else "degraded",
        "services": {
            "anthropic": ai_status,
            "filesystem": True,
            "templates": True
        },
        "stats": {
            "projects_count": len(list(PROJECTS_DIR.iterdir())),
            "uptime": get_uptime()
        }
    }
```

### Metrics to Track

```python
# Simple metrics tracking
from collections import defaultdict
from datetime import datetime

metrics = defaultdict(int)
timings = defaultdict(list)

def track_metric(name: str, value: int = 1):
    metrics[name] += value

def track_timing(name: str, duration_ms: float):
    timings[name].append(duration_ms)

@app.get("/metrics")
async def get_metrics():
    return {
        "counters": dict(metrics),
        "timings": {
            name: {
                "avg": sum(times) / len(times),
                "min": min(times),
                "max": max(times),
                "count": len(times)
            }
            for name, times in timings.items()
        }
    }
```

### Key Metrics

| Metric | Type | Purpose |
|--------|------|---------|
| projects_created | Counter | Track usage |
| sources_added | Counter | Research activity |
| ai_calls_total | Counter | API usage |
| ai_calls_failed | Counter | Error rate |
| scoring_calculations | Counter | Feature usage |
| exports_generated | Counter | Output usage |
| api_latency_ms | Timing | Performance |
| ai_latency_ms | Timing | AI response time |

---

## 6. Backup & Recovery

### Project Backup Strategy

```python
import shutil
from datetime import datetime

def backup_project(project_path: Path, backup_dir: Path):
    """Create timestamped backup of project."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{project_path.name}_{timestamp}"
    backup_path = backup_dir / backup_name

    shutil.copytree(project_path, backup_path)

    return backup_path

def restore_project(backup_path: Path, projects_dir: Path):
    """Restore project from backup."""
    # Extract original name (remove timestamp)
    original_name = "_".join(backup_path.name.split("_")[:-2])
    target_path = projects_dir / original_name

    if target_path.exists():
        shutil.rmtree(target_path)

    shutil.copytree(backup_path, target_path)

    return target_path
```

### n8n Workflow Backup

```bash
# Export all workflows
n8n export:workflow --all --output=./backups/workflows.json

# Export credentials (encrypted)
n8n export:credentials --all --output=./backups/credentials.json
```

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="./backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Backup projects
cp -r ./projects "$BACKUP_DIR/projects"

# Backup n8n workflows
n8n export:workflow --all --output="$BACKUP_DIR/workflows.json"

# Backup config
cp -r ./code/config "$BACKUP_DIR/config"

# Compress
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Backup created: $BACKUP_DIR.tar.gz"
```

---

## 7. Cost Estimation

### AI API Costs

**Anthropic Claude (claude-sonnet-4-20250514):**
- Input: $3 / 1M tokens
- Output: $15 / 1M tokens

**Estimated per campaign:**

| Operation | Input Tokens | Output Tokens | Cost |
|-----------|-------------|---------------|------|
| Research summaries (10x) | 50,000 | 5,000 | $0.23 |
| Brief analysis | 5,000 | 2,000 | $0.05 |
| Quick reference | 20,000 | 3,000 | $0.11 |
| Idea generation (optional) | 10,000 | 10,000 | $0.18 |
| **Total per campaign** | **85,000** | **20,000** | **~$0.57** |

**Monthly estimate (10 campaigns):** ~$6

### Infrastructure Costs

| Service | Self-Hosted | Cloud |
|---------|-------------|-------|
| n8n | Free | $20/mo (starter) |
| Python API | Free | $5-20/mo (small VPS) |
| Storage | Local | $1-5/mo |
| **Total** | **$0** | **$26-45/mo** |

---

## 8. Rate Limiting Strategy

### AI API Rate Limits

**Anthropic:**
- Requests per minute: 60 (starter)
- Tokens per minute: 100,000

### Implementation

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(3)
)
async def call_claude(prompt: str):
    """Call Claude with automatic retry on rate limit."""
    try:
        return await client.messages.create(...)
    except anthropic.RateLimitError:
        logger.warning("Rate limited, retrying...")
        raise  # Will retry
```

### n8n Rate Limiting

In Claude node settings:
```yaml
options:
  timeout: 120000  # 2 minutes
  retry:
    maxAttempts: 3
    waitBetween: 5000  # 5 seconds
```

---

## 9. Internationalization

### Current Scope

**Primary language**: Spanish (Latin America)
**Secondary**: Guaraní phrases (Paraguay-specific)

### String Externalization

```yaml
# code/config/strings/es.yaml

messages:
  project_created: "Proyecto creado exitosamente"
  source_added: "Fuente agregada"
  invalid_url: "URL inválida"
  scoring_complete: "Puntuación calculada"

errors:
  project_not_found: "Proyecto no encontrado: {project_id}"
  source_invalid: "No se pudo validar la fuente: {url}"

labels:
  market_size: "Tamaño del mercado"
  growth_rate: "Tasa de crecimiento"
  market_share: "Participación de mercado"
```

### Usage

```python
import yaml

def load_strings(lang: str = "es"):
    with open(f"config/strings/{lang}.yaml") as f:
        return yaml.safe_load(f)

strings = load_strings()
message = strings["messages"]["project_created"]
```

---

## 10. Documentation for End Users

### User Guide Outline

Create `code/docs/USER-GUIDE.md`:

```markdown
# Guía del Usuario

## Introducción
- Qué es el Campaign Generator
- Para quién es

## Inicio Rápido
- Crear primer proyecto
- Agregar fuentes
- Generar ideas

## Flujos de Trabajo
- Campaña completa paso a paso
- Agregar fuentes rápidamente
- Calcular puntajes

## Referencia de Comandos
- Lista de todos los endpoints/workflows
- Parámetros y ejemplos

## Solución de Problemas
- Errores comunes
- Preguntas frecuentes

## Mejores Prácticas
- Cuántas fuentes agregar
- Cómo puntuar ideas
- Qué incluir en research
```

### Video Tutorials (Future)

Plan for:
1. Overview (5 min)
2. Creating a project (3 min)
3. Research workflow (10 min)
4. Scoring ideas (5 min)
5. Exporting deliverables (3 min)

---

## 11. CI/CD Pipeline

### GitHub Actions (if using GitHub)

```yaml
# .github/workflows/test.yml

name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run tests
        run: pytest code/tests/ -v

      - name: Check formatting
        run: |
          pip install black
          black --check code/
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml

repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

Install:
```bash
pip install pre-commit
pre-commit install
```

---

## 12. Development Standards

### Code Style

```python
# Use Black defaults
line_length = 88
target_version = "py311"

# Type hints required
def create_project(brand: str, country: str) -> Path:
    ...

# Docstrings required (Google style)
def calculate_score(scores: dict[str, int]) -> int:
    """Calculate weighted total score.

    Args:
        scores: Dictionary of criterion name to score (1-10)

    Returns:
        Total score (0-100)

    Raises:
        ValueError: If score is out of range
    """
    ...
```

### Git Commit Messages

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat(generator): add project creation endpoint
fix(scoring): handle missing scores gracefully
docs(api): add endpoint documentation
test(research): add source validation tests
```

### Pull Request Template

```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guide
- [ ] Self-reviewed
- [ ] Documentation updated
- [ ] No console.log/print statements
```

---

## Summary Checklist

### Before Starting Development

#### Infrastructure
- [ ] n8n running and accessible
- [ ] Python environment ready
- [ ] API keys obtained and tested
- [ ] Docker setup (if production)

#### Code Foundation
- [ ] Directory structure created
- [ ] Empty `__init__.py` files
- [ ] Exception classes defined
- [ ] Logging configured
- [ ] Configuration loader ready

#### Templates & Data
- [ ] All Jinja2 templates created
- [ ] AI prompts written and tested
- [ ] Sample project with test data
- [ ] Test fixtures ready

#### Documentation
- [ ] All 6 docs reviewed
- [ ] User guide outline ready
- [ ] API documentation format decided

#### DevOps
- [ ] .gitignore complete
- [ ] pre-commit hooks installed
- [ ] CI/CD pipeline configured
- [ ] Backup strategy defined

#### Security
- [ ] Input validation planned
- [ ] Path safety implemented
- [ ] API keys secured
- [ ] n8n auth enabled

#### Monitoring
- [ ] Health endpoints defined
- [ ] Metrics to track identified
- [ ] Error notification setup

---

## What's Still Missing?

After this document, you should also consider:

1. **API Documentation Format** - OpenAPI/Swagger setup
2. **Postman/Insomnia Collection** - For API testing
3. **Load Testing Plan** - How many concurrent users?
4. **Accessibility** - If building any UI
5. **Analytics** - Track feature usage
6. **Feedback Mechanism** - How users report issues

---

## Recommended Order of Implementation

1. **Week 0 (Preparation)**
   - Complete all checklist items above
   - Create all config files
   - Set up test fixtures
   - Configure logging and errors

2. **Week 1 (Foundation)**
   - FastAPI skeleton with health check
   - First n8n workflow (Create Project)
   - Basic error handling
   - First passing tests

3. **Week 2+ (Features)**
   - Continue per original timeline

---

This completes the additional preparation requirements. With documents 01-06, you have comprehensive coverage of everything needed before starting development.
