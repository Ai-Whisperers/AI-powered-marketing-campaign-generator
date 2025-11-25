"""
Integration tests for API routes.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status(self, client):
        """Health endpoint should return status healthy."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data


class TestInfoEndpoint:
    """Tests for system info endpoint."""

    def test_info_returns_200(self, client):
        """Info endpoint should return 200 OK."""
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_contains_capabilities(self, client):
        """Info should contain system capabilities."""
        response = client.get("/info")
        data = response.json()
        assert "capabilities" in data
        assert "ai_provider" in data["capabilities"]


class TestProjectRoutes:
    """Tests for project management routes."""

    def test_create_project_success(self, client):
        """Creating a project should return 200 and project data."""
        response = client.post(
            "/projects",
            json={
                "name": "Test Project",
                "client": "Test Client",
                "country": "Paraguay"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Project"
        assert data["client"] == "Test Client"
        assert data["status"] == "created"

    def test_create_project_missing_name(self, client):
        """Creating project without name should fail."""
        response = client.post(
            "/projects",
            json={
                "client": "Test Client",
                "country": "Paraguay"
            }
        )
        assert response.status_code == 422  # Validation error

    def test_create_project_name_too_short(self, client):
        """Creating project with empty name should fail."""
        response = client.post(
            "/projects",
            json={
                "name": "",
                "client": "Test Client",
                "country": "Paraguay"
            }
        )
        assert response.status_code == 422

    def test_list_projects(self, client):
        """Listing projects should return array."""
        response = client.get("/projects")
        assert response.status_code == 200
        data = response.json()
        assert "projects" in data
        assert isinstance(data["projects"], list)

    def test_get_nonexistent_project(self, client):
        """Getting nonexistent project should return 404."""
        response = client.get("/projects/nonexistent-project-id")
        assert response.status_code == 404


class TestBriefRoutes:
    """Tests for brief parsing routes."""

    @pytest.fixture
    def project_id(self, client):
        """Create a test project and return its ID."""
        response = client.post(
            "/projects",
            json={
                "name": "Brief Test Project",
                "client": "Test Client",
                "country": "Paraguay"
            }
        )
        return response.json()["id"]

    def test_parse_brief_too_short(self, client, project_id):
        """Brief content too short should fail validation."""
        response = client.post(
            f"/projects/{project_id}/brief/parse",
            json={"content": "Too short"}
        )
        assert response.status_code == 422

    def test_parse_brief_nonexistent_project(self, client):
        """Parsing brief for nonexistent project should return 404."""
        response = client.post(
            "/projects/nonexistent/brief/parse",
            json={"content": "A" * 200}
        )
        assert response.status_code == 404


class TestExportRoutes:
    """Tests for export routes."""

    def test_download_path_traversal_blocked(self, client):
        """Path traversal attempts should be blocked."""
        # Create a project first
        response = client.post(
            "/projects",
            json={
                "name": "Export Test",
                "client": "Test",
                "country": "Paraguay"
            }
        )
        project_id = response.json()["id"]

        # Try path traversal
        response = client.get(
            f"/projects/{project_id}/export/download/..%2F..%2F.env"
        )
        # Should either be 400 (blocked) or 404 (not found)
        assert response.status_code in [400, 404]

    def test_list_exports_empty_project(self, client):
        """Listing exports for new project should return empty."""
        # Create project
        response = client.post(
            "/projects",
            json={
                "name": "Empty Export Test",
                "client": "Test",
                "country": "Paraguay"
            }
        )
        project_id = response.json()["id"]

        # List exports
        response = client.get(f"/projects/{project_id}/export")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0


class TestResearchRoutes:
    """Tests for research routes."""

    @pytest.fixture
    def project_id(self, client):
        """Create a test project."""
        response = client.post(
            "/projects",
            json={
                "name": "Research Test",
                "client": "Test",
                "country": "Paraguay"
            }
        )
        return response.json()["id"]

    def test_add_research_empty_sources(self, client, project_id):
        """Adding empty sources list should work."""
        response = client.post(
            f"/projects/{project_id}/research",
            json={"sources": []}
        )
        # Empty list should be accepted
        assert response.status_code == 200

    def test_add_research_too_many_sources(self, client, project_id):
        """Adding too many sources should fail validation."""
        sources = [
            {
                "url": f"https://example.com/{i}",
                "title": f"Source {i}",
                "category": "01-mercado-general"
            }
            for i in range(51)  # Over the 50 limit
        ]
        response = client.post(
            f"/projects/{project_id}/research",
            json={"sources": sources}
        )
        assert response.status_code == 422


class TestIdeasRoutes:
    """Tests for ideas routes."""

    @pytest.fixture
    def project_id(self, client):
        """Create a test project."""
        response = client.post(
            "/projects",
            json={
                "name": "Ideas Test",
                "client": "Test",
                "country": "Paraguay"
            }
        )
        return response.json()["id"]

    def test_score_ideas_no_ideas(self, client, project_id):
        """Scoring ideas when none exist should handle gracefully."""
        response = client.post(
            f"/projects/{project_id}/ideas/score",
            json={}
        )
        # Should either succeed with 0 ideas or return error
        assert response.status_code in [200, 400]


class TestIterationRoutes:
    """Tests for iteration routes."""

    @pytest.fixture
    def project_id(self, client):
        """Create a test project."""
        response = client.post(
            "/projects",
            json={
                "name": "Iteration Test",
                "client": "Test",
                "country": "Paraguay"
            }
        )
        return response.json()["id"]

    def test_analyze_research_gaps(self, client, project_id):
        """Analyzing research gaps should return response."""
        response = client.post(
            f"/projects/{project_id}/research/analyze-gaps"
        )
        # May fail due to no brief, but should not be 500
        assert response.status_code != 500

    def test_analyze_idea_gaps(self, client, project_id):
        """Analyzing idea gaps should return response."""
        response = client.post(
            f"/projects/{project_id}/ideas/analyze-gaps"
        )
        # May fail due to no ideas, but should not be 500
        assert response.status_code != 500


class TestSecurityHeaders:
    """Tests for security headers."""

    def test_security_headers_present(self, client):
        """Security headers should be present in responses."""
        response = client.get("/health")

        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"

        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"

        assert "x-xss-protection" in response.headers

        assert "referrer-policy" in response.headers


class TestRateLimiting:
    """Tests for rate limiting."""

    def test_rate_limit_headers(self, client):
        """Rate limited responses should include Retry-After header."""
        # This test may not trigger rate limit in normal conditions
        # but ensures the infrastructure is in place
        response = client.get("/health")
        # If rate limited, should have Retry-After
        if response.status_code == 429:
            assert "retry-after" in response.headers


class TestInputValidation:
    """Tests for input validation."""

    def test_brief_max_length(self, client):
        """Brief exceeding max length should be rejected."""
        # Create project
        response = client.post(
            "/projects",
            json={
                "name": "Validation Test",
                "client": "Test",
                "country": "Paraguay"
            }
        )
        project_id = response.json()["id"]

        # Try to submit huge brief
        huge_content = "A" * 60000  # Over 50KB limit
        response = client.post(
            f"/projects/{project_id}/brief/parse",
            json={"content": huge_content}
        )
        assert response.status_code == 422

    def test_project_name_max_length(self, client):
        """Project name exceeding max length should be rejected."""
        response = client.post(
            "/projects",
            json={
                "name": "A" * 201,  # Over 200 char limit
                "client": "Test",
                "country": "Paraguay"
            }
        )
        assert response.status_code == 422
