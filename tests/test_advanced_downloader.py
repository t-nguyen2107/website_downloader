"""Tests for advanced_downloader.py module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json
import tempfile
import requests
from concurrent.futures import ThreadPoolExecutor

# Import the module to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from advanced_downloader import AdvancedWebsiteDownloader


class TestAdvancedWebsiteDownloader:
    """Test cases for AdvancedWebsiteDownloader class."""

    @pytest.fixture
    def downloader(self, temp_dir):
        """Create an AdvancedWebsiteDownloader instance for testing."""
        config = {
            'base_url': 'https://example.com',
            'output_dir': str(temp_dir),
            'delay': 0,  # No delay for tests
            'max_depth': 2,
            'max_workers': 2,
            'verify_ssl': True,
            'ignore_robots': False
        }
        return AdvancedWebsiteDownloader(config)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create a test configuration file."""
        config = {
            "delay": 0.5,
            "max_depth": 3,
            "max_workers": 4,
            "verify_ssl": True,
            "include_subdomains": False,
            "force_redownload": False,
            "ignore_robots": False,
            "user_agent": "Test Bot 1.0"
        }
        config_path = temp_dir / "test_config.json"
        config_path.write_text(json.dumps(config, indent=2))
        return config_path

    def test_init_default(self, temp_dir):
        """Test AdvancedWebsiteDownloader initialization with defaults."""
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir)
        )
        
        assert downloader.base_url == "https://example.com"
        assert downloader.output_dir == Path(temp_dir)
        assert downloader.delay == 1.0
        assert downloader.max_depth == 3
        assert downloader.max_workers == 5
        assert downloader.verify_ssl is True
        assert downloader.include_subdomains is False
        assert downloader.force_redownload is False
        assert downloader.ignore_robots is False

    def test_init_with_config(self, temp_dir, config_file):
        """Test initialization with configuration file."""
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            config_file=str(config_file)
        )
        
        assert downloader.delay == 0.5
        assert downloader.max_depth == 3
        assert downloader.max_workers == 4
        assert downloader.verify_ssl is True
        assert downloader.user_agent == "Test Bot 1.0"

    def test_load_config_file_not_found(self, temp_dir):
        """Test configuration loading with non-existent file."""
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            config_file="nonexistent.json"
        )
        
        # Should use defaults when config file not found
        assert downloader.delay == 1.0
        assert downloader.max_depth == 3

    def test_is_valid_url_scheme(self, downloader):
        """Test URL scheme validation in advanced downloader."""
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

    def test_is_internal_url_with_subdomains(self, temp_dir):
        """Test internal URL detection with subdomain handling."""
        # Test with subdomains disabled
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            include_subdomains=False
        )
        
        assert downloader.is_internal_url("https://example.com/page.html")
        assert not downloader.is_internal_url("https://sub.example.com/page.html")
        
        # Test with subdomains enabled
        downloader.include_subdomains = True
        assert downloader.is_internal_url("https://example.com/page.html")
        assert downloader.is_internal_url("https://sub.example.com/page.html")
        assert not downloader.is_internal_url("https://other.com/page.html")

    def test_parse_url_attribute(self, downloader):
        """Test URL attribute parsing (srcset, etc.)."""
        base_url = "https://example.com/"
        
        # Test srcset parsing
        srcset = "image-320w.jpg 320w, image-480w.jpg 480w, image-800w.jpg 800w"
        urls = downloader.parse_url_attribute(srcset, base_url)
        
        expected_urls = {
            "https://example.com/image-320w.jpg",
            "https://example.com/image-480w.jpg",
            "https://example.com/image-800w.jpg"
        }
        
        assert urls == expected_urls
        
        # Test single URL
        single_url = "image.jpg"
        urls = downloader.parse_url_attribute(single_url, base_url)
        assert urls == {"https://example.com/image.jpg"}
        
        # Test with invalid schemes
        invalid_srcset = "mailto:test@example.com, tel:+123456789, image.jpg"
        urls = downloader.parse_url_attribute(invalid_srcset, base_url)
        assert urls == {"https://example.com/image.jpg"}

    def test_extract_links_advanced(self, downloader, sample_html):
        """Test advanced link extraction."""
        base_url = "https://example.com/"
        links = downloader.extract_links_advanced(sample_html, base_url)
        
        # Should extract valid internal links
        expected_links = {
            "https://example.com/page2.html",
            "https://example.com/styles.css",
            "https://example.com/favicon.ico",
            "https://example.com/image.jpg",
            "https://example.com/script.js",
            "https://example.com/bg.jpg"
        }
        
        for link in expected_links:
            assert link in links, f"Expected link {link} not found"
        
        # Should filter out invalid schemes
        invalid_schemes = ["mailto:", "tel:", "javascript:"]
        for link in links:
            for scheme in invalid_schemes:
                assert not link.startswith(scheme), f"Invalid scheme {scheme} found in {link}"

    def test_extract_css_urls_advanced(self, downloader, sample_css):
        """Test advanced CSS URL extraction."""
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

    @patch('advanced_downloader.requests.Session')
    def test_download_file_with_retry(self, mock_session_class, downloader, temp_dir, mock_response):
        """Test file download with retry mechanism."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        downloader.session = mock_session
        
        # First call fails, second succeeds
        test_content = "Test file content"
        mock_session.get.side_effect = [
            mock_response("", status_code=500),  # First attempt fails
            mock_response(test_content)  # Second attempt succeeds
        ]
        
        # Test download
        url = "https://example.com/test.txt"
        filepath = temp_dir / "test.txt"
        
        result = downloader.download_file(url, filepath)
        
        assert result is True
        assert filepath.exists()
        assert filepath.read_text() == test_content
        assert mock_session.get.call_count == 2  # Retry was attempted

    @patch('advanced_downloader.requests.Session')
    def test_download_file_max_retries(self, mock_session_class, downloader, temp_dir, mock_response):
        """Test file download with maximum retries exceeded."""
        # Setup mock
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        downloader.session = mock_session
        
        # All attempts fail
        mock_session.get.return_value = mock_response("", status_code=500)
        
        # Test download
        url = "https://example.com/test.txt"
        filepath = temp_dir / "test.txt"
        
        result = downloader.download_file(url, filepath)
        
        assert result is False
        assert not filepath.exists()
        assert mock_session.get.call_count == 3  # Initial + 2 retries

    def test_verify_completeness(self, downloader, temp_dir, create_test_files):
        """Test download completeness verification."""
        # Create test HTML file with links
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <img src="image.jpg" alt="Test">
            <a href="page2.html">Link</a>
        </body>
        </html>
        '''
        
        # Create some files
        files = {
            "index.html": html_content,
            "style.css": "body { color: red; }",
            # Missing: image.jpg, page2.html
        }
        create_test_files(files)
        
        # Add URLs to downloaded set
        downloader.downloaded_urls.add("https://example.com/")
        downloader.downloaded_urls.add("https://example.com/style.css")
        
        # Verify completeness
        missing_files = downloader.verify_completeness()
        
        # Should detect missing files
        expected_missing = {
            "https://example.com/image.jpg",
            "https://example.com/page2.html"
        }
        
        assert len(missing_files) == 2
        for missing in expected_missing:
            assert missing in missing_files

    @patch('advanced_downloader.ThreadPoolExecutor')
    @patch('advanced_downloader.requests.Session')
    def test_download_website_multithreaded(self, mock_session_class, mock_executor_class, downloader, mock_response, sample_html):
        """Test multithreaded website download."""
        # Setup mocks
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        downloader.session = mock_session
        
        mock_executor = Mock(spec=ThreadPoolExecutor)
        mock_executor_class.return_value.__enter__.return_value = mock_executor
        
        # Mock future results
        mock_future = Mock()
        mock_future.result.return_value = True
        mock_executor.submit.return_value = mock_future
        
        # Mock responses
        def mock_get(url, **kwargs):
            if url.endswith('.html') or url.endswith('/'):
                return mock_response(sample_html, url=url)
            else:
                return mock_response("Mock content", url=url)
        
        mock_session.get.side_effect = mock_get
        
        # Mock robots.txt check
        with patch.object(downloader, 'can_fetch', return_value=True):
            # Run download
            downloader.download_website()
        
        # Verify ThreadPoolExecutor was used
        mock_executor_class.assert_called_once_with(max_workers=2)
        assert mock_executor.submit.called

    def test_url_aliasing(self, downloader):
        """Test URL aliasing functionality."""
        # Add some aliases
        downloader.url_aliases["https://example.com/old-page.html"] = "https://example.com/new-page.html"
        downloader.url_aliases["https://example.com/redirect"] = "https://example.com/final-page.html"
        
        # Test alias resolution
        assert downloader.resolve_url_alias("https://example.com/old-page.html") == "https://example.com/new-page.html"
        assert downloader.resolve_url_alias("https://example.com/redirect") == "https://example.com/final-page.html"
        assert downloader.resolve_url_alias("https://example.com/normal-page.html") == "https://example.com/normal-page.html"

    def test_progress_tracking(self, downloader):
        """Test download progress tracking."""
        # Initial state
        assert downloader.total_files == 0
        assert downloader.completed_files == 0
        
        # Add some files to track
        downloader.total_files = 10
        downloader.completed_files = 3
        
        progress = downloader.get_progress()
        assert progress == 0.3  # 30%
        
        # Test with zero total
        downloader.total_files = 0
        progress = downloader.get_progress()
        assert progress == 0.0

    def test_generate_advanced_report(self, downloader, temp_dir):
        """Test advanced report generation."""
        # Add test data
        downloader.downloaded_urls.add("https://example.com/page1.html")
        downloader.downloaded_urls.add("https://example.com/style.css")
        downloader.failed_urls.add("https://example.com/missing.jpg")
        
        # Add some timing data
        downloader.start_time = 1000.0
        downloader.end_time = 1010.0  # 10 seconds
        
        # Generate report
        report_path = downloader.generate_report()
        
        assert report_path.exists()
        report_content = report_path.read_text()
        
        # Check report contains expected information
        assert "Advanced Download Report" in report_content
        assert "page1.html" in report_content
        assert "style.css" in report_content
        assert "missing.jpg" in report_content
        assert "2048" in report_content or "2.0 KB" in report_content
        assert "10.0" in report_content  # Duration
        assert "66.7%" in report_content  # Success rate


@pytest.mark.integration
class TestAdvancedDownloaderIntegration:
    """Integration tests for AdvancedWebsiteDownloader."""
    
    @pytest.mark.slow
    @patch('advanced_downloader.requests.Session')
    def test_full_advanced_workflow(self, mock_session_class, temp_dir, sample_html, mock_response):
        """Test complete advanced download workflow."""
        # Setup downloader
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            delay=0,
            max_depth=1,
            max_workers=2
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
        
        # Mock robots.txt and threading
        with patch.object(downloader, 'can_fetch', return_value=True), \
             patch('advanced_downloader.ThreadPoolExecutor') as mock_executor_class:
            
            # Setup executor mock
            mock_executor = Mock()
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            
            mock_future = Mock()
            mock_future.result.return_value = True
            mock_executor.submit.return_value = mock_future
            
            # Run download
            downloader.download_website()
        
        # Verify files were "downloaded"
        assert len(downloader.downloaded_urls) > 0
        
        # Verify advanced features were used
        mock_executor_class.assert_called_once()
        
        # Verify report generation
        report_files = list(temp_dir.glob("*_advanced_report.txt"))
        assert len(report_files) == 1

    def test_config_file_integration(self, temp_dir):
        """Test configuration file integration."""
        # Create config file
        config = {
            "delay": 0.1,
            "max_depth": 2,
            "max_workers": 3,
            "verify_ssl": False,
            "include_subdomains": True,
            "user_agent": "Integration Test Bot"
        }
        
        config_path = temp_dir / "integration_config.json"
        config_path.write_text(json.dumps(config, indent=2))
        
        # Create downloader with config
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir),
            config_file=str(config_path)
        )
        
        # Verify config was loaded
        assert downloader.delay == 0.1
        assert downloader.max_depth == 2
        assert downloader.max_workers == 3
        assert downloader.verify_ssl is False
        assert downloader.include_subdomains is True
        assert downloader.user_agent == "Integration Test Bot"


@pytest.mark.unit
class TestAdvancedFeatures:
    """Unit tests for advanced features."""
    
    def test_error_recovery_backoff(self, temp_dir):
        """Test exponential backoff in error recovery."""
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir)
        )
        
        # Test backoff calculation
        assert downloader.calculate_backoff(0) == 1.0  # First retry
        assert downloader.calculate_backoff(1) == 2.0  # Second retry
        assert downloader.calculate_backoff(2) == 4.0  # Third retry
        
        # Test with custom base delay
        downloader.delay = 0.5
        assert downloader.calculate_backoff(0) == 0.5
        assert downloader.calculate_backoff(1) == 1.0
        assert downloader.calculate_backoff(2) == 2.0

    def test_asset_type_detection(self, temp_dir):
        """Test enhanced asset type detection."""
        downloader = AdvancedWebsiteDownloader(
            base_url="https://example.com",
            output_dir=str(temp_dir)
        )
        
        # Test various file types
        assert downloader.get_asset_type("page.html") == "html"
        assert downloader.get_asset_type("style.css") == "css"
        assert downloader.get_asset_type("script.js") == "javascript"
        assert downloader.get_asset_type("image.jpg") == "image"
        assert downloader.get_asset_type("image.png") == "image"
        assert downloader.get_asset_type("image.gif") == "image"
        assert downloader.get_asset_type("image.svg") == "image"
        assert downloader.get_asset_type("font.woff") == "font"
        assert downloader.get_asset_type("font.woff2") == "font"
        assert downloader.get_asset_type("font.ttf") == "font"
        assert downloader.get_asset_type("unknown.xyz") == "other"