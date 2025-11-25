# Campaign Generator - Development Roadmap

Este directorio contiene el código para automatizar el workflow completo de generación de campañas publicitarias.

---

## Arquitectura del Sistema

```
code/
├── README.md                    # Este archivo
├── src/                         # Código fuente
│   ├── __init__.py
│   ├── generator/               # Generación de proyectos
│   ├── research/                # Automatización de research
│   ├── scoring/                 # Sistema de puntuación
│   ├── synthesis/               # Compilación y síntesis
│   └── export/                  # Exportación (PDF, PPTX)
├── tests/                       # Tests unitarios
├── config/                      # Configuraciones
└── cli.py                       # Interfaz de línea de comandos
```

---

## Módulos a Desarrollar

### 1. Generator Module (`src/generator/`)

**Propósito**: Crear estructura de proyectos con templates

**Componentes**:
```python
# project_creator.py
- create_project_structure()      # Crea carpetas y archivos
- generate_readme()               # README principal
- generate_research_structure()   # Carpetas 01-10

# template_engine.py
- load_template()                 # Cargar template base
- render_template()               # Llenar variables
- save_rendered()                 # Guardar archivo

# idea_generator.py
- create_idea_templates()         # Templates de ideas
- create_summary_template()       # 00-RESUMEN-IDEAS.md
```

**Estado**: Parcialmente implementado en `tools/campaign_generator.py`

---

### 2. Research Module (`src/research/`)

**Propósito**: Asistir en la recopilación de información

**Componentes**:
```python
# source_manager.py
- add_source()                    # Agregar nueva fuente
- format_citation()               # Formatear cita
- validate_url()                  # Verificar URL activa
- generate_sources_file()         # Crear fuentes-completas.md

# data_extractor.py
- extract_from_url()              # Extraer datos de URL
- summarize_content()             # Resumir contenido (AI)
- categorize_source()             # Clasificar tipo de fuente

# research_tracker.py
- get_research_status()           # Estado por categoría
- mark_complete()                 # Marcar completado
- list_pending()                  # Listar pendientes
- generate_status_report()        # Reporte de progreso
```

**Funcionalidades clave**:
- Tracking de fuentes con validación de URLs
- Generación automática de citas formateadas
- Dashboard de progreso de investigación
- Integración con AI para resumir contenido

---

### 3. Scoring Module (`src/scoring/`)

**Propósito**: Sistema de evaluación de ideas

**Componentes**:
```python
# score_calculator.py
- calculate_total_score()         # Suma ponderada
- get_tier()                      # Clasificar tier
- compare_ideas()                 # Comparar múltiples ideas
- generate_ranking()              # Ranking completo

# criteria_manager.py
- get_criteria()                  # Lista de criterios
- add_custom_criteria()           # Agregar criterio
- set_weights()                   # Pesos personalizados
- validate_scores()               # Validar rangos

# report_generator.py
- generate_summary()              # 00-RESUMEN-IDEAS.md
- generate_comparison_table()     # Tabla comparativa
- generate_top_10()               # Análisis Top 10
- generate_recommendations()      # Opciones A, B, C
```

**Funcionalidades clave**:
- Cálculo automático de puntajes
- Clasificación en tiers (Muy Alto, Alto, Medio, etc.)
- Generación de reportes comparativos
- Recomendaciones basadas en scores

---

### 4. Synthesis Module (`src/synthesis/`)

**Propósito**: Compilar y sintetizar información

**Componentes**:
```python
# quick_reference_generator.py
- extract_key_data()              # Extraer datos clave
- compile_quick_reference()       # Generar QR completo
- update_on_change()              # Actualizar cuando cambia source

# brief_analyzer.py
- parse_brief()                   # Parsear brief original
- extract_challenges()            # Extraer desafíos
- identify_opportunities()        # Identificar oportunidades
- generate_directions()           # Direcciones creativas

# cross_referencer.py
- find_references()               # Buscar referencias cruzadas
- validate_links()                # Validar links internos
- generate_index()                # Generar índice
- check_consistency()             # Verificar consistencia
```

**Funcionalidades clave**:
- Generación automática de Quick Reference
- Análisis de brief con extracción de insights
- Validación de cross-references
- Índices automáticos

---

### 5. Export Module (`src/export/`)

**Propósito**: Exportar a diferentes formatos

**Componentes**:
```python
# pdf_exporter.py
- export_idea_to_pdf()            # Idea individual a PDF
- export_all_ideas()              # Batch export
- export_summary_pdf()            # Resumen ejecutivo
- apply_styles()                  # Aplicar estilos

# presentation_generator.py
- generate_pitch_deck()           # Presentación de campaña
- add_slide()                     # Agregar slide
- export_to_pptx()                # Exportar a PowerPoint
- export_to_google_slides()       # Exportar a Google Slides

# report_exporter.py
- export_research_report()        # Reporte de investigación
- export_competitive_analysis()   # Análisis competitivo
- export_executive_summary()      # Resumen ejecutivo
```

**Funcionalidades clave**:
- Export a PDF con estilos consistentes
- Generación de presentaciones
- Reportes ejecutivos automáticos

---

## CLI Interface (`cli.py`)

**Propósito**: Interfaz unificada de línea de comandos

```bash
# Generar nuevo proyecto
campaign new --brand "Nike" --country "Argentina"

# Ver estado de research
campaign status --project campana-nike-2025

# Agregar fuente
campaign source add --url "https://..." --category "media"

# Calcular scores
campaign score --project campana-nike-2025

# Generar quick reference
campaign synthesize --project campana-nike-2025

# Exportar a PDF
campaign export pdf --project campana-nike-2025

# Generar presentación
campaign export pptx --project campana-nike-2025
```

---

## Configuración (`config/`)

### settings.yaml
```yaml
# Configuración global
defaults:
  country: "Paraguay"
  campaign_type: "digital"
  num_ideas: 25
  year: 2025

# Criterios de scoring
scoring:
  criteria:
    - name: "Diferenciación"
      weight: 1.0
      description: "¿Se destaca de la competencia?"
    - name: "Autenticidad"
      weight: 1.0
      description: "¿Es genuinamente cultural?"
    # ... más criterios

  thresholds:
    very_high: 90
    high: 80
    medium: 70
    needs_work: 60

# Templates
templates:
  ideas_per_project: 25
  research_categories: 10

# Export
export:
  pdf_style: "professional"
  include_cover: true
  include_toc: true
```

### templates/
```
config/templates/
├── idea.md.j2                   # Template Jinja2 para ideas
├── quick-reference.md.j2        # Template para QR
├── brief-analysis.md.j2         # Template para brief
├── research-file.md.j2          # Template para research
└── summary.md.j2                # Template para resumen
```

---

## Orden de Desarrollo Recomendado

### Fase 1: Core Infrastructure (Semana 1)
1. **CLI básico** - Estructura de comandos
2. **Config loader** - Cargar configuraciones
3. **Template engine** - Motor de templates Jinja2
4. **Refactor generator** - Migrar código existente

### Fase 2: Research Tools (Semana 2)
5. **Source manager** - CRUD de fuentes
6. **Research tracker** - Status de investigación
7. **URL validator** - Verificar links activos

### Fase 3: Scoring System (Semana 3)
8. **Score calculator** - Cálculo de puntajes
9. **Tier classifier** - Clasificación automática
10. **Report generator** - Generar resúmenes

### Fase 4: Synthesis (Semana 4)
11. **Quick reference generator** - Compilar QR
12. **Brief analyzer** - Parsear briefs
13. **Cross referencer** - Validar links

### Fase 5: Export (Semana 5)
14. **PDF exporter** - Mejorar export existente
15. **Presentation generator** - Crear slides
16. **Executive reports** - Reportes finales

### Fase 6: Polish (Semana 6)
17. **Tests** - Unit tests para todo
18. **Documentation** - Docs completos
19. **Examples** - Ejemplos de uso

---

## Dependencias Adicionales

```txt
# requirements.txt (actualizado)

# Core
click>=8.0.0              # CLI framework
pyyaml>=6.0               # Config files
jinja2>=3.0.0             # Template engine

# Research
requests>=2.28.0          # HTTP requests
beautifulsoup4>=4.11.0    # HTML parsing
validators>=0.20.0        # URL validation

# Export
reportlab>=4.0.0          # PDF generation
markdown2>=2.4.0          # Markdown parsing
python-pptx>=0.6.21       # PowerPoint generation

# Optional AI
openai>=1.0.0             # GPT integration
anthropic>=0.5.0          # Claude integration

# Development
pytest>=7.0.0             # Testing
black>=23.0.0             # Formatting
mypy>=1.0.0               # Type checking
```

---

## Ejemplo de Uso Final

```bash
# 1. Crear nuevo proyecto
$ campaign new --brand "Coca-Cola" --country "Paraguay" --type "digital"
✅ Proyecto creado: campana-coca-cola-2025/

# 2. Durante investigación, agregar fuentes
$ campaign source add \
    --url "https://ultimahora.com/coca-cola-paraguay" \
    --category "media" \
    --topic "market-share"
✅ Fuente agregada a 08-referencias/

# 3. Ver progreso
$ campaign status
📊 Progreso de Investigación:
   01-mercado-general    ████████░░ 80%
   02-marca              ██████████ 100%
   03-competencia        ██████░░░░ 60%
   ...
   Total: 65% completado

# 4. Calcular scores después de ideación
$ campaign score
📈 Ranking de Ideas:
   #1 idea-07 "El Sabor de Casa"     92/100 🏆
   #2 idea-12 "Momentos Compartidos" 88/100 🥇
   #3 idea-03 "Refrescante Verdad"   85/100 🥈
   ...

# 5. Generar Quick Reference
$ campaign synthesize
✅ QUICK-REFERENCE.md actualizado

# 6. Exportar presentación final
$ campaign export pptx --template "pitch-deck"
✅ Presentación generada: output/coca-cola-pitch.pptx

# 7. Exportar PDFs de ideas
$ campaign export pdf --top 10
✅ 10 PDFs generados en output/ideas/
```

---

## Beneficios del Sistema Completo

### Para el Usuario
- **Ahorro de tiempo**: De 11 días a 5-7 días
- **Consistencia**: Misma calidad en cada proyecto
- **Trazabilidad**: Todo documentado automáticamente
- **Profesionalismo**: Outputs pulidos

### Para el Negocio
- **Escalabilidad**: Múltiples proyectos en paralelo
- **Onboarding**: Nuevos usuarios productivos rápido
- **Calidad**: Metodología probada replicada
- **Diferenciación**: Herramienta única en el mercado

---

## Próximos Pasos Inmediatos

1. **Crear estructura base** de `src/`
2. **Implementar CLI** con Click
3. **Migrar** `campaign_generator.py` a nuevo sistema
4. **Agregar** sistema de configuración YAML
5. **Crear** primeros tests

---

¿Por dónde quieres que empecemos?
