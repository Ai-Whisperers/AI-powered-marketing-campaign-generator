# Campaign Research Generator System

Sistema de generación automatizada de proyectos de investigación para campañas publicitarias.

---

## Descripción

Este repositorio contiene:
1. **Campañas completadas** - Ejemplos de investigación profesional (Pilsen, Subway)
2. **Herramientas de automatización** - Generadores de estructura y templates
3. **Metodología documentada** - Framework replicable para cualquier marca

---

## Estructura del Repositorio

```
maga/
├── requirements.txt               # Dependencias Python unificadas
├── code/                          # Código fuente principal
│   ├── api/                       # Servicios y lógica de negocio
│   └── cli.py                     # CLI unificada (Entry Point)
├── docs/                          # Documentación
├── archive/                       # Scripts legacy (referencia)
└── campanas-completadas/          # Campañas finalizadas
```

---

## Inicio Rápido

### Instalación

```bash
# Clonar repositorio
git clone [url-del-repo]
cd maga

# Instalar dependencias
pip install -r requirements.txt
```

### Uso de la CLI

La nueva herramienta unificada se encuentra en `code/cli.py`.

#### 1. Ver Información del Sistema
```bash
python code/cli.py info
```

#### 2. Generar Ideas
```bash
python code/cli.py generate --project-id "brand-country-2025" --num-ideas 15
```

#### 3. Puntuar Ideas
```bash
python code/cli.py score --project-id "brand-country-2025"
```

#### 4. Generar Prompts de Video (Veo 3)
```bash
python code/cli.py video-prompts --project-id "brand-country-2025"
```

#### 5. Generar Videos (Costoso)
```bash
# Requiere configuración de Google Cloud Vertex AI
python code/cli.py generate-videos --project-id "brand-country-2025"
```

---

## Metodología

### Fases del Proyecto

| Fase | Días | Entregables |
|------|------|-------------|
| 1. Setup | 1 | Estructura de carpetas |
| 2. Investigación | 2-4 | Archivos 01-08 completados |
| 3. Análisis | 1 | BRIEF-CAMPANA.md |
| 4. Research Creativo | 2 | Carpetas 09-10 |
| 5. Síntesis | 1 | QUICK-REFERENCE.md |
| 6. Ideación | 2 | 20-25 ideas puntuadas |
| 7. Recomendación | 1 | Top 10 + opciones finales |

### Criterios de Evaluación de Ideas

| Criterio | Descripción |
|----------|-------------|
| Diferenciación | ¿Se destaca de la competencia? |
| Autenticidad | ¿Es genuinamente cultural? |
| Potencial Viral | ¿La gente lo compartirá? |
| Conexión Emocional | ¿Genera engagement? |
| Ejecutabilidad | ¿Es viable de producir? |

**Escala**: 1-10 por criterio | **Mínimo aceptable**: 60/100 | **Ideal**: 90+/100

---

## Configuración

La configuración del proyecto se maneja a través de variables de entorno en `code/.env` y el archivo `tools/config.yaml` (legacy, migrando a `code/config.yaml`).

### Variables de Entorno (.env)
- `OPENAI_API_KEY`: Para generación de texto e ideas.
- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: JSON de cuenta de servicio para Vertex AI (Veo 3).
- `ANTHROPIC_API_KEY`: Opcional, para modelos Claude.

---

## Contacto

Proyecto desarrollado para competencia Jóvenes Talentos 2025.

