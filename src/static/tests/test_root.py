"""Tests for GET / endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestRootRedirect:
    """Test suite for the GET / root redirect endpoint."""

    def test_root_returns_redirect(self, client):
        """
        AAA Test: Verify GET / returns a redirect response.
        
        Arrange: Client is ready
        Act: Make GET request to root endpoint
        Assert: Verify status code is 307 (temporary redirect) or 302
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        # FastAPI RedirectResponse returns 307 by default
        assert response.status_code in [307, 302]

    def test_root_redirects_to_static_index(self, client):
        """
        AAA Test: Verify GET / redirects to /static/index.html.
        
        Arrange: Client is ready
        Act: Make GET request to root endpoint and capture location
        Assert: Verify redirect location is /static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)
        redirect_location = response.headers.get("location")
        
        # Assert
        assert redirect_location == "/static/index.html"

    def test_root_follows_redirect_successfully(self, client):
        """
        AAA Test: Verify following redirect leads to static content.
        
        Arrange: Client is ready
        Act: Make GET request to root with follow_redirects=True
        Assert: Verify final response is successful (200)
        """
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
