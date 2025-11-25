"""
Pytest configuration and fixtures for Campaign Generator tests.
"""

import os
import json
import pytest
from pathlib import Path


# =============================================================================
# Path Fixtures
# =============================================================================

@pytest.fixture
def fixtures_path() -> Path:
    """Return the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_project_path(fixtures_path) -> Path:
    """Return the path to sample project fixture."""
    return fixtures_path / "sample-project"


@pytest.fixture
def config_path() -> Path:
    """Return the path to configuration directory."""
    return Path(__file__).parent.parent / "config"


@pytest.fixture
def prompts_path(config_path) -> Path:
    """Return the path to AI prompts directory."""
    return config_path / "prompts"


@pytest.fixture
def templates_path(config_path) -> Path:
    """Return the path to Jinja2 templates directory."""
    return config_path / "templates"


# =============================================================================
# Sample Data Fixtures
# =============================================================================

@pytest.fixture
def sample_brief(sample_project_path) -> str:
    """Load sample brief content."""
    brief_path = sample_project_path / "brief.md"
    return brief_path.read_text(encoding="utf-8")


@pytest.fixture
def sample_research(sample_project_path) -> str:
    """Load sample research content."""
    research_path = sample_project_path / "01-mercado-general" / "panorama-mercado.md"
    return research_path.read_text(encoding="utf-8")


@pytest.fixture
def sample_idea(sample_project_path) -> str:
    """Load sample idea content."""
    idea_path = sample_project_path / "ideas" / "idea-001.md"
    return idea_path.read_text(encoding="utf-8")


@pytest.fixture
def sample_sources(sample_project_path) -> dict:
    """Load sample sources JSON."""
    sources_path = sample_project_path / "sources.json"
    return json.loads(sources_path.read_text(encoding="utf-8"))


# =============================================================================
# Configuration Fixtures
# =============================================================================

@pytest.fixture
def default_config() -> dict:
    """Return default configuration for testing."""
    return {
        "project": {
            "default_country": "Paraguay",
            "default_language": "es",
            "default_type": "integrated",
            "num_ideas": 25,
            "ideas_per_batch": 5
        },
        "scoring": {
            "criteria": [
                {"name": "Diferenciación", "weight": 1.0},
                {"name": "Relevancia cultural", "weight": 1.0},
                {"name": "Claridad del insight", "weight": 1.0},
                {"name": "Ejecutabilidad", "weight": 0.8},
                {"name": "Potencial viral", "weight": 0.7}
            ],
            "thresholds": {
                "very_high": 90,
                "high": 80,
                "medium": 70,
                "low": 60
            }
        },
        "ai": {
            "primary": "anthropic",
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.7,
            "max_tokens": 4096
        }
    }


@pytest.fixture
def mock_ai_response() -> dict:
    """Return mock AI response for testing without API calls."""
    return {
        "main_challenge": "Rejuvenecer la marca sin perder consumidores actuales",
        "context": "La marca tiene fuerte heritage pero es percibida como anticuada por el target joven.",
        "constraints": [
            "Mantener el azul institucional",
            "No comparaciones directas",
            "Presupuesto limitado a USD 150K"
        ],
        "success_looks_like": "Aumentar consideración +15 puntos en target 25-35 años"
    }


# =============================================================================
# Idea Scoring Fixtures
# =============================================================================

@pytest.fixture
def sample_scores() -> dict:
    """Return sample idea scores for testing calculations."""
    return {
        "diferenciacion": 8,
        "relevancia_cultural": 9,
        "claridad_insight": 8,
        "ejecutabilidad": 7,
        "potencial_viral": 6,
        "memorabilidad": 7,
        "versatilidad": 8,
        "alineacion_marca": 8,
        "potencial_pr": 5,
        "escalabilidad": 8
    }


@pytest.fixture
def expected_weighted_score() -> float:
    """Expected weighted score for sample_scores fixture."""
    # Based on default weights and sample scores
    return 7.4


# =============================================================================
# API Testing Fixtures
# =============================================================================

@pytest.fixture
def test_client():
    """Create test client for FastAPI testing."""
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)


# =============================================================================
# Environment Fixtures
# =============================================================================

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set mock environment variables for testing."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "true")


@pytest.fixture
def temp_project_dir(tmp_path) -> Path:
    """Create temporary project directory for output testing."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()

    # Create subdirectories
    (project_dir / "ideas").mkdir()
    (project_dir / "01-mercado-general").mkdir()

    return project_dir
