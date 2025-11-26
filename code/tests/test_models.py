"""
Unit tests for Pydantic models and validation.
"""

import pytest
from api.models import (
    BriefUpload,
    ExportRequest,
    IdeaGenerateRequest,
    IdeaScores,
    ProjectCreate,
    ResearchAddRequest,
    ResearchSource,
)
from pydantic import ValidationError


class TestProjectCreate:
    """Tests for ProjectCreate model."""

    def test_valid_project(self):
        """Valid project should be created."""
        project = ProjectCreate(
            name="Test Project",
            client="Test Client",
            country="Paraguay"
        )
        assert project.name == "Test Project"
        assert project.client == "Test Client"
        assert project.country == "Paraguay"

    def test_name_min_length(self):
        """Name must have at least 1 character."""
        with pytest.raises(ValidationError):
            ProjectCreate(
                name="",
                client="Test Client",
                country="Paraguay"
            )

    def test_name_max_length(self):
        """Name must not exceed 200 characters."""
        with pytest.raises(ValidationError):
            ProjectCreate(
                name="A" * 201,
                client="Test Client",
                country="Paraguay"
            )

    def test_client_max_length(self):
        """Client must not exceed 100 characters."""
        with pytest.raises(ValidationError):
            ProjectCreate(
                name="Test",
                client="A" * 101,
                country="Paraguay"
            )

    def test_default_language(self):
        """Default language should be Spanish."""
        project = ProjectCreate(
            name="Test",
            client="Test",
            country="Paraguay"
        )
        assert project.language == "es"


class TestBriefUpload:
    """Tests for BriefUpload model."""

    def test_valid_brief(self):
        """Valid brief should be created."""
        content = "A" * 200
        brief = BriefUpload(content=content)
        assert len(brief.content) == 200

    def test_min_length(self):
        """Brief must have at least 100 characters."""
        with pytest.raises(ValidationError):
            BriefUpload(content="Short")

    def test_max_length(self):
        """Brief must not exceed 50000 characters."""
        with pytest.raises(ValidationError):
            BriefUpload(content="A" * 50001)

    def test_exactly_min_length(self):
        """Brief with exactly 100 chars should pass."""
        brief = BriefUpload(content="A" * 100)
        assert len(brief.content) == 100


class TestResearchSource:
    """Tests for ResearchSource model."""

    def test_valid_source(self):
        """Valid source should be created."""
        source = ResearchSource(
            url="https://example.com",
            title="Test Source",
            category="01-mercado-general"
        )
        assert source.title == "Test Source"

    def test_title_max_length(self):
        """Title must not exceed 500 characters."""
        with pytest.raises(ValidationError):
            ResearchSource(
                url="https://example.com",
                title="A" * 501,
                category="01-mercado-general"
            )

    def test_content_max_length(self):
        """Content must not exceed 100000 characters."""
        with pytest.raises(ValidationError):
            ResearchSource(
                url="https://example.com",
                title="Test",
                content="A" * 100001,
                category="01-mercado-general"
            )

    def test_invalid_url(self):
        """Invalid URL should fail validation."""
        with pytest.raises(ValidationError):
            ResearchSource(
                url="not-a-url",
                title="Test",
                category="01-mercado-general"
            )

    def test_optional_url(self):
        """URL is optional."""
        source = ResearchSource(
            title="Test",
            category="01-mercado-general"
        )
        assert source.url is None


class TestResearchAddRequest:
    """Tests for ResearchAddRequest model."""

    def test_valid_request(self):
        """Valid request should be created."""
        request = ResearchAddRequest(
            sources=[
                ResearchSource(
                    title="Test",
                    category="01-mercado-general"
                )
            ]
        )
        assert len(request.sources) == 1

    def test_empty_sources(self):
        """Empty sources list should be valid."""
        request = ResearchAddRequest(sources=[])
        assert len(request.sources) == 0

    def test_max_sources(self):
        """Sources must not exceed 50 items."""
        sources = [
            ResearchSource(
                title=f"Source {i}",
                category="01-mercado-general"
            )
            for i in range(51)
        ]
        with pytest.raises(ValidationError):
            ResearchAddRequest(sources=sources)


class TestExportRequest:
    """Tests for ExportRequest model."""

    def test_valid_pdf_request(self):
        """Valid PDF export request."""
        request = ExportRequest(format="pdf")
        assert request.format == "pdf"
        assert request.include_research is True
        assert request.top_ideas_count == 10

    def test_valid_pptx_request(self):
        """Valid PPTX export request."""
        request = ExportRequest(format="pptx")
        assert request.format == "pptx"

    def test_invalid_format(self):
        """Invalid format should fail."""
        with pytest.raises(ValidationError):
            ExportRequest(format="docx")

    def test_top_ideas_min(self):
        """Top ideas count must be at least 1."""
        with pytest.raises(ValidationError):
            ExportRequest(format="pdf", top_ideas_count=0)

    def test_top_ideas_max(self):
        """Top ideas count must not exceed 50."""
        with pytest.raises(ValidationError):
            ExportRequest(format="pdf", top_ideas_count=51)


class TestIdeaGenerateRequest:
    """Tests for IdeaGenerateRequest model."""

    def test_default_values(self):
        """Default values should be set."""
        request = IdeaGenerateRequest()
        assert request.num_ideas == 25
        assert request.batch_size == 5

    def test_custom_values(self):
        """Custom values should be accepted."""
        request = IdeaGenerateRequest(num_ideas=10, batch_size=3)
        assert request.num_ideas == 10
        assert request.batch_size == 3


class TestIdeaScores:
    """Tests for IdeaScores model."""

    def test_valid_scores(self):
        """Valid scores should be accepted."""
        scores = IdeaScores(
            diferenciacion=8,
            relevancia_cultural=9,
            claridad_insight=7,
            ejecutabilidad=8,
            potencial_viral=6,
            memorabilidad=7,
            versatilidad=8,
            alineacion_marca=9,
            potencial_pr=5,
            escalabilidad=7
        )
        assert scores.diferenciacion == 8

    def test_score_min(self):
        """Score must be at least 1."""
        with pytest.raises(ValidationError):
            IdeaScores(
                diferenciacion=0,  # Invalid
                relevancia_cultural=5,
                claridad_insight=5,
                ejecutabilidad=5,
                potencial_viral=5,
                memorabilidad=5,
                versatilidad=5,
                alineacion_marca=5,
                potencial_pr=5,
                escalabilidad=5
            )

    def test_score_max(self):
        """Score must not exceed 10."""
        with pytest.raises(ValidationError):
            IdeaScores(
                diferenciacion=11,  # Invalid
                relevancia_cultural=5,
                claridad_insight=5,
                ejecutabilidad=5,
                potencial_viral=5,
                memorabilidad=5,
                versatilidad=5,
                alineacion_marca=5,
                potencial_pr=5,
                escalabilidad=5
            )
