"""
Unit tests for security module.
"""


import pytest
from api.security import RateLimiter, _secure_compare, validate_filename, validate_project_id
from fastapi import HTTPException


class TestValidateFilename:
    """Tests for filename validation."""

    def test_valid_filename(self):
        """Valid filenames should pass."""
        assert validate_filename("export.pdf") == "export.pdf"
        assert validate_filename("my-file.pptx") == "my-file.pptx"
        assert validate_filename("report_2024.pdf") == "report_2024.pdf"

    def test_empty_filename_rejected(self):
        """Empty filename should raise HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            validate_filename("")
        assert exc_info.value.status_code == 400
        assert "required" in exc_info.value.detail.lower()

    def test_path_traversal_double_dot(self):
        """Path traversal with .. should be rejected."""
        with pytest.raises(HTTPException) as exc_info:
            validate_filename("../../../etc/passwd")
        assert exc_info.value.status_code == 400
        assert "path traversal" in exc_info.value.detail.lower()

    def test_path_traversal_absolute_path(self):
        """Absolute paths should be rejected."""
        with pytest.raises(HTTPException) as exc_info:
            validate_filename("/etc/passwd")
        assert exc_info.value.status_code == 400

    def test_path_traversal_backslash(self):
        """Windows-style path traversal should be rejected."""
        with pytest.raises(HTTPException) as exc_info:
            validate_filename("..\\..\\windows\\system32")
        assert exc_info.value.status_code == 400

    def test_invalid_characters(self):
        """Filenames with invalid characters should be rejected."""
        invalid_names = [
            "file<name>.pdf",
            "file>name.pdf",
            "file:name.pdf",
            'file"name.pdf',
            "file|name.pdf",
            "file?name.pdf",
            "file*name.pdf"
        ]
        for name in invalid_names:
            with pytest.raises(HTTPException) as exc_info:
                validate_filename(name)
            assert exc_info.value.status_code == 400


class TestValidateProjectId:
    """Tests for project ID validation."""

    def test_valid_project_id(self):
        """Valid project IDs should pass."""
        assert validate_project_id("my-project-123") == "my-project-123"
        assert validate_project_id("cafe-central-abc123") == "cafe-central-abc123"

    def test_empty_project_id_rejected(self):
        """Empty project ID should raise HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            validate_project_id("")
        assert exc_info.value.status_code == 400

    def test_too_long_project_id(self):
        """Project ID over 100 chars should be rejected."""
        long_id = "a" * 101
        with pytest.raises(HTTPException) as exc_info:
            validate_project_id(long_id)
        assert exc_info.value.status_code == 400
        assert "too long" in exc_info.value.detail.lower()

    def test_path_traversal_in_project_id(self):
        """Path traversal in project ID should be rejected."""
        with pytest.raises(HTTPException) as exc_info:
            validate_project_id("../../../etc")
        assert exc_info.value.status_code == 400

    def test_slashes_in_project_id(self):
        """Slashes in project ID should be rejected."""
        with pytest.raises(HTTPException) as exc_info:
            validate_project_id("project/subdir")
        assert exc_info.value.status_code == 400


class TestSecureCompare:
    """Tests for constant-time string comparison."""

    def test_equal_strings(self):
        """Equal strings should return True."""
        assert _secure_compare("password123", "password123") is True

    def test_different_strings(self):
        """Different strings should return False."""
        assert _secure_compare("password123", "password456") is False

    def test_different_lengths(self):
        """Different length strings should return False."""
        assert _secure_compare("short", "longer_string") is False

    def test_empty_strings(self):
        """Empty strings should compare correctly."""
        assert _secure_compare("", "") is True
        assert _secure_compare("", "notempty") is False


class TestRateLimiter:
    """Tests for rate limiting functionality."""

    def test_allows_under_limit(self):
        """Requests under limit should be allowed."""
        limiter = RateLimiter()

        # Should allow first request
        assert limiter.is_allowed("client1", limit=5, window=60) is True

        # Should allow up to limit
        for _ in range(4):
            assert limiter.is_allowed("client1", limit=5, window=60) is True

    def test_blocks_over_limit(self):
        """Requests over limit should be blocked."""
        limiter = RateLimiter()

        # Use up the limit
        for _ in range(5):
            limiter.is_allowed("client2", limit=5, window=60)

        # Should block the 6th request
        assert limiter.is_allowed("client2", limit=5, window=60) is False

    def test_different_clients_separate(self):
        """Different clients should have separate limits."""
        limiter = RateLimiter()

        # Use up limit for client A
        for _ in range(5):
            limiter.is_allowed("clientA", limit=5, window=60)

        # Client A should be blocked
        assert limiter.is_allowed("clientA", limit=5, window=60) is False

        # Client B should still be allowed
        assert limiter.is_allowed("clientB", limit=5, window=60) is True

    def test_retry_after_calculation(self):
        """Retry after should calculate remaining window time."""
        limiter = RateLimiter()

        # Make a request
        limiter.is_allowed("client3", limit=1, window=60)

        # Should block and provide retry time
        assert limiter.is_allowed("client3", limit=1, window=60) is False

        retry_after = limiter.get_retry_after("client3", window=60)
        assert 0 < retry_after <= 60

    def test_window_expiration(self):
        """Old requests should be cleaned up after window."""
        import time

        limiter = RateLimiter()

        # Use up limit with very short window
        for _ in range(5):
            limiter.is_allowed("client4", limit=5, window=1)

        # Should be blocked
        assert limiter.is_allowed("client4", limit=5, window=1) is False

        # Wait for window to expire
        time.sleep(1.1)

        # Should be allowed again
        assert limiter.is_allowed("client4", limit=5, window=1) is True
