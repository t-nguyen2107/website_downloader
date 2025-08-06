"""Pytest configuration and fixtures for Website Downloader tests."""

import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock
import pytest
import requests
from bs4 import BeautifulSoup


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Page</title>
        <link rel="stylesheet" href="styles.css">
        <link rel="icon" href="favicon.ico">
    </head>
    <body>
        <h1>Test Page</h1>
        <p>This is a test page.</p>
        <a href="page2.html">Internal Link</a>
        <a href="https://external.com">External Link</a>
        <a href="mailto:test@example.com">Email Link</a>
        <a href="tel:+1234567890">Phone Link</a>
        <img src="image.jpg" alt="Test Image">
        <script src="script.js"></script>
        <style>
            body { background: url('bg.jpg'); }
        </style>
    </body>
    </html>
    """


@pytest.fixture
def sample_css():
    """Sample CSS content for testing."""
    return """
    body {
        font-family: Arial, sans-serif;
        background-image: url('background.jpg');
        background-color: #ffffff;
    }
    
    .header {
        background: url("header-bg.png");
    }
    
    @import url('fonts.css');
    @import "reset.css";
    
    .icon {
        background: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPC9zdmc+);
    }
    """


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    def _mock_response(content="", status_code=200, headers=None, url="http://example.com"):
        response = Mock(spec=requests.Response)
        response.content = content.encode('utf-8') if isinstance(content, str) else content
        response.text = content if isinstance(content, str) else content.decode('utf-8')
        response.status_code = status_code
        response.headers = headers or {'content-type': 'text/html'}
        response.url = url
        response.raise_for_status = Mock()
        if status_code >= 400:
            response.raise_for_status.side_effect = requests.HTTPError(f"{status_code} Error")
        return response
    return _mock_response


@pytest.fixture
def mock_session(mock_response):
    """Create a mock requests session."""
    session = Mock(spec=requests.Session)
    session.get.return_value = mock_response()
    session.head.return_value = mock_response()
    return session


@pytest.fixture
def sample_robots_txt():
    """Sample robots.txt content."""
    return """
    User-agent: *
    Disallow: /private/
    Disallow: /admin/
    Allow: /public/
    
    User-agent: BadBot
    Disallow: /
    
    Sitemap: https://example.com/sitemap.xml
    """


@pytest.fixture
def test_urls():
    """Common test URLs for testing."""
    return {
        'base': 'https://example.com',
        'internal': 'https://example.com/page.html',
        'external': 'https://other.com/page.html',
        'subdomain': 'https://sub.example.com/page.html',
        'relative': '/relative/path.html',
        'absolute': 'https://example.com/absolute/path.html',
        'mailto': 'mailto:test@example.com',
        'tel': 'tel:+1234567890',
        'javascript': 'javascript:void(0)',
        'data': 'data:text/plain;base64,SGVsbG8gV29ybGQ=',
        'ftp': 'ftp://ftp.example.com/file.txt',
        'file': 'file:///local/file.txt'
    }


@pytest.fixture
def create_test_files(temp_dir):
    """Create test files in temporary directory."""
    def _create_files(files_dict):
        """Create files from dictionary {filename: content}."""
        created_files = []
        for filename, content in files_dict.items():
            file_path = temp_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            created_files.append(file_path)
        return created_files
    return _create_files


# Pytest markers for test categorization
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "network: marks tests that require network access"
    )