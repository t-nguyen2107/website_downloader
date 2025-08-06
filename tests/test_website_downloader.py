"""Tests for website_downloader.py module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import requests
from urllib.robotparser import RobotFileParser

# Import the module to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from website_downloader import WebsiteDownloader


class TestWebsiteDownloader:
    """Test cases for WebsiteDownloader class."""

    @pytest.fixture
    def downloader(self, temp_dir):
        """Create a WebsiteDownloader instance for testing."""
        return WebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            delay=0,  # No delay for tests
            max_depth=2
        )

    def test_init(self, temp_dir):
        """Test WebsiteDownloader initialization."""
        downloader = WebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            delay=1,
            max_depth=3
        )
        
        assert downloader.base_url == "https://example.com"
        assert downloader.output_dir == Path(temp_dir)
        assert downloader.delay == 1
        assert downloader.max_depth == 3
        assert downloader.downloaded_urls == set()
        assert downloader.failed_urls == set()

    def test_is_valid_url_scheme(self, downloader):
        """Test URL scheme validation."""
        # Valid schemes
        assert downloader.is_valid_url_scheme("https://example.com")
        assert downloader.is_valid_url_scheme("http://example.com")
        
        # Invalid schemes
        assert not downloader.is_valid_url_scheme("mailto:test@example.com")
        assert not downloader.is_valid_url_scheme("tel:+1234567890")
        assert not downloader.is_valid_url_scheme("javascript:void(0)")
        assert not downloader.is_valid_url_scheme("data:text/plain;base64,SGVsbG8=")
        assert not downloader.is_valid_url_scheme("ftp://ftp.example.com")
        assert not downloader.is_valid_url_scheme("file:///local/file.txt")
        
        # Edge cases
        assert not downloader.is_valid_url_scheme("")
        assert not downloader.is_valid_url_scheme("not-a-url")
        assert not downloader.is_valid_url_scheme("://missing-scheme")

    def test_normalize_url(self, downloader):
        """Test URL normalization."""
        base_url = "https://example.com/path/"
        
        # Absolute URLs
        assert downloader.normalize_url("https://other.com/page.html", base_url) == "https://other.com/page.html"
        
        # Relative URLs
        assert downloader.normalize_url("page.html", base_url) == "https://example.com/path/page.html"
        assert downloader.normalize_url("../other.html", base_url) == "https://example.com/other.html"
        assert downloader.normalize_url("/root.html", base_url) == "https://example.com/root.html"
        
        # URLs with fragments and queries
        assert downloader.normalize_url("page.html#section", base_url) == "https://example.com/path/page.html"
        assert downloader.normalize_url("page.html?param=value", base_url) == "https://example.com/path/page.html?param=value"

    def test_is_internal_url(self, downloader):
        """Test internal URL detection."""
        # Internal URLs
        assert downloader.is_internal_url("https://example.com/page.html")
        assert downloader.is_internal_url("https://example.com/")
        assert downloader.is_internal_url("https://example.com/path/file.css")
        
        # External URLs
        assert not downloader.is_internal_url("https://other.com/page.html")
        assert not downloader.is_internal_url("https://sub.example.com/page.html")
        assert not downloader.is_internal_url("http://example.com/page.html")  # Different scheme

    def test_url_to_filepath(self, downloader):
        """Test URL to filepath conversion."""
        # Basic conversion
        filepath = downloader.url_to_filepath("https://example.com/page.html")
        assert filepath.name == "page.html"
        
        # Root URL
        filepath = downloader.url_to_filepath("https://example.com/")
        assert filepath.name == "index.html"
        
        # URL with query parameters
        filepath = downloader.url_to_filepath("https://example.com/page.html?param=value")
        assert filepath.name == "page.html"
        
        # Nested paths
        filepath = downloader.url_to_filepath("https://example.com/path/to/file.css")
        assert "path" in str(filepath)
        assert "to" in str(filepath)
        assert filepath.name == "file.css"

    @patch('website_downloader.requests.Session')
    def test_check_robots_txt(self, mock_session_class, downloader, sample_robots_txt):
        """Test robots.txt checking."""
        # Mock session and response
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.text = sample_robots_txt
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response
        
        # Test robots.txt loading
        downloader.check_robots_txt()
        
        # Verify session was called correctly
        mock_session.get.assert_called_once_with("https://example.com/robots.txt", timeout=10)
        
        # Test URL checking
        assert downloader.can_fetch("https://example.com/public/page.html")
        assert not downloader.can_fetch("https://example.com/private/page.html")
        assert not downloader.can_fetch("https://example.com/admin/page.html")

    @patch('website_downloader.requests.Session')
    def test_check_robots_txt_not_found(self, mock_session_class, downloader):
        """Test robots.txt handling when file not found."""
        # Mock session and response
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_session.get.return_value = mock_response
        
        # Test robots.txt loading with 404
        downloader.check_robots_txt()
        
        # Should allow all URLs when robots.txt not found
        assert downloader.can_fetch("https://example.com/any/page.html")

    def test_extract_links(self, downloader, sample_html):
        """Test link extraction from HTML."""
        base_url = "https://example.com/"
        links = downloader.extract_links(sample_html, base_url)
        
        # Should extract valid internal links
        expected_links = {
            "https://example.com/page2.html",
            "https://example.com/styles.css",
            "https://example.com/favicon.ico",
            "https://example.com/image.jpg",
            "https://example.com/script.js",
            "https://example.com/bg.jpg"
        }
        
        # Check that valid links are extracted
        for link in expected_links:
            assert link in links, f"Expected link {link} not found in extracted links"
        
        # Check that invalid schemes are filtered out
        invalid_links = {
            "mailto:test@example.com",
            "tel:+1234567890",
            "https://external.com"  # External link should be excluded
        }
        
        for link in invalid_links:
            assert link not in links, f"Invalid link {link} should not be in extracted links"

    def test_extract_css_urls(self, downloader, sample_css):
        """Test URL extraction from CSS."""
        base_url = "https://example.com/styles/"
        urls = downloader.extract_css_urls(sample_css, base_url)
        
        # Should extract valid CSS URLs
        expected_urls = {
            "https://example.com/styles/background.jpg",
            "https://example.com/styles/header-bg.png",
            "https://example.com/styles/fonts.css",
            "https://example.com/styles/reset.css"
        }
        
        for url in expected_urls:
            assert url in urls, f"Expected CSS URL {url} not found"
        
        # Data URLs should be filtered out
        assert not any("data:" in url for url in urls)

    def test_is_likely_html(self, downloader):
        """Test HTML content detection."""
        # HTML content
        html_content = "<!DOCTYPE html><html><head><title>Test</title></head><body></body></html>"
        assert downloader.is_likely_html(html_content)
        
        # Non-HTML content
        css_content = "body { color: red; }"
        assert not downloader.is_likely_html(css_content)
        
        js_content = "function test() { return true; }"
        assert not downloader.is_likely_html(js_content)
        
        # Empty content
        assert not downloader.is_likely_html("")

    @patch('website_downloader.requests.Session')
    def test_download_file_success(self, mock_session_class, downloader, temp_dir, mock_response):
        """Test successful file download."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        downloader.session = mock_session
        
        test_content = "Test file content"
        mock_session.get.return_value = mock_response(test_content)
        
        # Test download
        url = "https://example.com/test.txt"
        filepath = temp_dir / "test.txt"
        
        result = downloader.download_file(url, filepath)
        
        assert result is True
        assert filepath.exists()
        assert filepath.read_text() == test_content
        assert url in downloader.downloaded_urls

    @patch('website_downloader.requests.Session')
    def test_download_file_failure(self, mock_session_class, downloader, temp_dir, mock_response):
        """Test failed file download."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        downloader.session = mock_session
        
        mock_session.get.return_value = mock_response("", status_code=404)
        
        # Test download
        url = "https://example.com/notfound.txt"
        filepath = temp_dir / "notfound.txt"
        
        result = downloader.download_file(url, filepath)
        
        assert result is False
        assert not filepath.exists()
        assert url in downloader.failed_urls

    def test_generate_report(self, downloader, temp_dir):
        """Test download report generation."""
        # Add some test data
        downloader.downloaded_urls.add("https://example.com/page1.html")
        downloader.downloaded_urls.add("https://example.com/style.css")
        downloader.failed_urls.add("https://example.com/missing.jpg")
        # Note: WebsiteDownloader doesn't track total_size
        
        # Generate report
        report_path = downloader.generate_report()
        
        assert report_path.exists()
        report_content = report_path.read_text()
        
        # Check report contains expected information
        assert "Download Report" in report_content
        assert "page1.html" in report_content
        assert "style.css" in report_content
        assert "missing.jpg" in report_content
        assert "1024" in report_content or "1.0 KB" in report_content


@pytest.mark.unit
class TestURLValidation:
    """Unit tests for URL validation functions."""
    
    def test_url_scheme_validation(self):
        """Test various URL schemes."""
        downloader = WebsiteDownloader("https://example.com", "/tmp")
        
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://sub.example.com/path",
            "http://localhost:8000"
        ]
        
        invalid_urls = [
            "mailto:user@example.com",
            "tel:+1-555-123-4567",
            "javascript:alert('test')",
            "data:text/plain;base64,SGVsbG8gV29ybGQ=",
            "ftp://ftp.example.com/file.txt",
            "file:///home/user/file.txt",
            "about:blank",
            "chrome://settings",
            "#anchor",
            "",
            "not-a-url"
        ]
        
        for url in valid_urls:
            assert downloader.is_valid_url_scheme(url), f"URL {url} should be valid"
        
        for url in invalid_urls:
            assert not downloader.is_valid_url_scheme(url), f"URL {url} should be invalid"


@pytest.mark.integration
class TestWebsiteDownloaderIntegration:
    """Integration tests for WebsiteDownloader."""
    
    @pytest.mark.slow
    @patch('website_downloader.requests.Session')
    def test_full_download_workflow(self, mock_session_class, temp_dir, sample_html, mock_response):
        """Test complete download workflow."""
        # Setup downloader
        downloader = WebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            delay=0,
            max_depth=1
        )
        
        # Setup mock session
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        downloader.session = mock_session
        
        # Mock responses
        def mock_get(url, **kwargs):
            if url.endswith('.html') or url.endswith('/'):
                return mock_response(sample_html, url=url)
            else:
                return mock_response("Mock file content", url=url)
        
        mock_session.get.side_effect = mock_get
        
        # Mock robots.txt check
        with patch.object(downloader, 'can_fetch', return_value=True):
            # Run download
            downloader.download_website()
        
        # Verify files were "downloaded"
        assert len(downloader.downloaded_urls) > 0
        
        # Verify report generation
        report_files = list(temp_dir.glob("*_report.txt"))
        assert len(report_files) == 1