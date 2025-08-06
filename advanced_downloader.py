#!/usr/bin/env python3
"""
Advanced Website Downloader - Enhanced version with additional features

This is an enhanced version inspired by robust open-source projects like
PKHarsimran/website-downloader, with additional features for better
reliability and completeness checking.

Additional Features:
- Completeness verification
- Better asset type detection
- Improved error recovery
- URL aliasing for better offline navigation
- Multi-threaded downloading (optional)
- Configuration file support
"""

import os
import sys
import re
import time
import json
import argparse
import logging
import urllib.parse
import mimetypes
import threading
from pathlib import Path
from collections import deque, defaultdict
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote


class AdvancedWebsiteDownloader:
    def __init__(self, config):
        self.config = config
        self.base_url = config['base_url'].rstrip('/')
        self.domain = urlparse(self.base_url).netloc
        self.output_dir = Path(config['output_dir'])
        self.delay = config.get('delay', 1.0)
        self.max_depth = config.get('max_depth', 10)
        self.max_workers = config.get('max_workers', 1)
        self.verify_ssl = config.get('verify_ssl', True)
        
        # Asset type configuration
        self.asset_types = {
            'html': ['.html', '.htm', '.php', '.asp', '.aspx', '.jsp'],
            'css': ['.css'],
            'js': ['.js'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp', '.bmp'],
            'fonts': ['.woff', '.woff2', '.ttf', '.eot', '.otf'],
            'documents': ['.pdf', '.doc', '.docx', '.txt'],
            'media': ['.mp4', '.mp3', '.avi', '.mov', '.wav', '.ogg'],
            'archives': ['.zip', '.tar', '.gz', '.rar']
        }
        
        # Track downloads and statistics
        self.downloaded_urls = set()
        self.failed_urls = set()
        self.url_queue = deque([(self.base_url, 0)])
        self.url_aliases = {}  # For better offline navigation
        self.download_stats = defaultdict(int)
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Setup session
        self.setup_session()
        
        # Check robots.txt
        self.check_robots_txt()
        
    def setup_logging(self):
        """Enhanced logging setup"""
        log_file = self.output_dir / 'advanced_download.log'
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def setup_session(self):
        """Setup HTTP session with enhanced configuration"""
        self.session = requests.Session()
        
        # Headers
        self.session.headers.update({
            'User-Agent': self.config.get('user_agent', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # SSL verification
        self.session.verify = self.verify_ssl
        
        # Timeout configuration
        self.session.timeout = (10, 30)  # (connect, read)
        
    def check_robots_txt(self):
        """Enhanced robots.txt checking"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            self.robots_parser = rp
            
            # Check crawl delay
            crawl_delay = rp.crawl_delay('*')
            if crawl_delay and crawl_delay > self.delay:
                self.delay = crawl_delay
                self.logger.info(f"Updated delay to {self.delay}s based on robots.txt")
                
            self.logger.info(f"Loaded robots.txt from {robots_url}")
        except Exception as e:
            self.logger.warning(f"Could not load robots.txt: {e}")
            self.robots_parser = None
            
    def can_fetch(self, url):
        """Check if URL can be fetched according to robots.txt"""
        if self.robots_parser:
            return self.robots_parser.can_fetch('*', url)
        return True
        
    def is_internal_url(self, url):
        """Enhanced internal URL detection"""
        parsed = urlparse(url)
        
        # Same domain
        if parsed.netloc == self.domain:
            return True
            
        # Relative URL
        if parsed.netloc == '':
            return True
            
        # Subdomain check (optional)
        if self.config.get('include_subdomains', False):
            if parsed.netloc.endswith('.' + self.domain):
                return True
                
        return False
        
    def normalize_url(self, url):
        """Enhanced URL normalization"""
        # Remove fragment
        url = url.split('#')[0]
        
        # Decode URL encoding
        url = unquote(url)
        
        # Remove trailing slash for directories (except root)
        parsed = urlparse(url)
        if parsed.path.endswith('/') and parsed.path != '/':
            url = url.rstrip('/')
            
        return url
        
    def get_asset_type(self, url):
        """Determine asset type from URL"""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Get file extension
        ext = Path(path).suffix
        
        # Check against known types
        for asset_type, extensions in self.asset_types.items():
            if ext in extensions:
                return asset_type
                
        # Default to html for extensionless URLs
        if not ext or ext == '.':
            return 'html'
            
        return 'other'
        
    def url_to_filepath(self, url):
        """Enhanced URL to filepath conversion with aliasing"""
        parsed = urlparse(url)
        path = parsed.path.lstrip('/')
        
        # Handle root URL
        if not path or path == '':
            path = 'index.html'
        elif path.endswith('/'):
            path = path + 'index.html'
            
        # Handle extensionless URLs that should be HTML
        if '.' not in Path(path).name and self.get_asset_type(url) == 'html':
            path = path + '.html'
            
        # Handle query parameters
        if parsed.query:
            query_part = parsed.query.replace('&', '_').replace('=', '-').replace('?', '_')
            path_obj = Path(path)
            path = str(path_obj.with_name(path_obj.stem + '_' + query_part + path_obj.suffix))
            
        filepath = self.output_dir / path
        
        # Store alias for better navigation
        self.url_aliases[url] = filepath
        
        return filepath
        
    def download_file_with_retry(self, url, filepath, max_retries=3):
        """Download file with retry logic"""
        for attempt in range(max_retries):
            try:
                return self.download_file(url, filepath)
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to download {url} after {max_retries} attempts: {e}")
                    with self.lock:
                        self.failed_urls.add(url)
                    return False
                else:
                    self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}. Retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
        return False
        
    def download_file(self, url, filepath):
        """Enhanced file download with better error handling"""
        # Create directory if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Skip if already exists and not forcing re-download
        if filepath.exists() and not self.config.get('force_redownload', False):
            self.logger.debug(f"File already exists: {filepath}")
            with self.lock:
                self.downloaded_urls.add(url)
            return True
            
        try:
            # Make request with streaming for large files
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            
            # Write file
            if 'text' in content_type or 'html' in content_type or 'css' in content_type or 'javascript' in content_type:
                # Text-based files
                content = response.text
                filepath.write_text(content, encoding='utf-8')
            else:
                # Binary files
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
            # Update statistics
            with self.lock:
                self.downloaded_urls.add(url)
                asset_type = self.get_asset_type(url)
                self.download_stats[asset_type] += 1
                
            self.logger.info(f"Downloaded: {url} -> {filepath}")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error downloading {url}: {e}")
            raise
            
    def extract_links_advanced(self, html_content, base_url):
        """Advanced link extraction with better parsing"""
        soup = BeautifulSoup(html_content, 'lxml')
        links = set()
        
        # Standard link extraction
        selectors = {
            'a': ['href'],
            'link': ['href'],
            'script': ['src'],
            'img': ['src', 'data-src', 'data-lazy-src'],  # Include lazy loading
            'source': ['src', 'srcset'],
            'iframe': ['src'],
            'embed': ['src'],
            'object': ['data'],
            'video': ['src', 'poster'],
            'audio': ['src'],
            'track': ['src']
        }
        
        for tag, attrs in selectors.items():
            for element in soup.find_all(tag):
                for attr in attrs:
                    if element.get(attr):
                        urls = self.parse_url_attribute(element[attr], base_url)
                        links.update(urls)
                        
        # Extract from inline styles
        for element in soup.find_all(style=True):
            css_urls = self.extract_css_urls(element['style'], base_url)
            links.update(css_urls)
            
        # Extract from style tags
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                css_urls = self.extract_css_urls(style_tag.string, base_url)
                links.update(css_urls)
                
        # Extract from meta refresh
        for meta in soup.find_all('meta', {'http-equiv': 'refresh'}):
            content = meta.get('content', '')
            if 'url=' in content.lower():
                url = content.split('url=', 1)[1].strip()
                absolute_url = urljoin(base_url, url)
                links.add(self.normalize_url(absolute_url))
                
        return links
        
    def parse_url_attribute(self, attr_value, base_url):
        """Parse URL attribute that might contain multiple URLs (like srcset)"""
        urls = set()
        
        # Handle srcset attribute
        if ',' in attr_value and ('w' in attr_value or 'x' in attr_value):
            # This looks like a srcset
            for part in attr_value.split(','):
                url = part.strip().split()[0]  # Take URL part, ignore descriptor
                if url:
                    absolute_url = urljoin(base_url, url)
                    urls.add(self.normalize_url(absolute_url))
        else:
            # Single URL
            if attr_value.strip():
                absolute_url = urljoin(base_url, attr_value.strip())
                urls.add(self.normalize_url(absolute_url))
                
        return urls
        
    def extract_css_urls(self, css_content, base_url):
        """Enhanced CSS URL extraction"""
        urls = set()
        
        # Find url() references
        url_pattern = r'url\s*\(\s*["\']?([^"\')\s]+)["\']?\s*\)'
        for match in re.finditer(url_pattern, css_content, re.IGNORECASE):
            url = match.group(1).strip()
            if url and not url.startswith('data:'):
                absolute_url = urljoin(base_url, url)
                urls.add(self.normalize_url(absolute_url))
                
        # Find @import references
        import_pattern = r'@import\s+(?:url\s*\(\s*)?["\']?([^"\')\s]+)["\']?(?:\s*\))?'
        for match in re.finditer(import_pattern, css_content, re.IGNORECASE):
            url = match.group(1).strip()
            if url and not url.startswith('data:'):
                absolute_url = urljoin(base_url, url)
                urls.add(self.normalize_url(absolute_url))
                
        return urls
        
    def convert_links_advanced(self, content, current_url, content_type='html'):
        """Advanced link conversion for different content types"""
        if content_type == 'html':
            return self.convert_html_links(content, current_url)
        elif content_type == 'css':
            return self.convert_css_links(content, current_url)
        else:
            return content
            
    def convert_html_links(self, html_content, current_url):
        """Convert HTML links with enhanced handling"""
        soup = BeautifulSoup(html_content, 'lxml')
        current_filepath = self.url_to_filepath(current_url)
        
        # Convert different types of links
        selectors = {
            'a': ['href'],
            'link': ['href'],
            'script': ['src'],
            'img': ['src', 'data-src'],
            'source': ['src'],
            'iframe': ['src'],
            'embed': ['src'],
            'object': ['data'],
            'video': ['src', 'poster'],
            'audio': ['src']
        }
        
        for tag, attrs in selectors.items():
            for element in soup.find_all(tag):
                for attr in attrs:
                    if element.get(attr):
                        original_url = element[attr]
                        converted_url = self.convert_single_url(original_url, current_url, current_filepath)
                        if converted_url != original_url:
                            element[attr] = converted_url
                            
        # Convert inline styles
        for element in soup.find_all(style=True):
            element['style'] = self.convert_css_links(element['style'], current_url)
            
        # Convert style tags
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                style_tag.string = self.convert_css_links(style_tag.string, current_url)
                
        return str(soup)
        
    def convert_css_links(self, css_content, current_url):
        """Convert URLs in CSS content"""
        current_filepath = self.url_to_filepath(current_url)
        
        def replace_url(match):
            url = match.group(1).strip()
            if url and not url.startswith('data:'):
                converted = self.convert_single_url(url, current_url, current_filepath)
                return f'url("{converted}")'
            return match.group(0)
            
        # Replace url() references
        css_content = re.sub(
            r'url\s*\(\s*["\']?([^"\')\s]+)["\']?\s*\)',
            replace_url,
            css_content,
            flags=re.IGNORECASE
        )
        
        # Replace @import references
        def replace_import(match):
            url = match.group(1).strip()
            if url and not url.startswith('data:'):
                converted = self.convert_single_url(url, current_url, current_filepath)
                return f'@import "{converted}"'
            return match.group(0)
            
        css_content = re.sub(
            r'@import\s+["\']([^"\')]+)["\']',
            replace_import,
            css_content,
            flags=re.IGNORECASE
        )
        
        return css_content
        
    def convert_single_url(self, url, current_url, current_filepath):
        """Convert a single URL to relative path if internal"""
        try:
            absolute_url = urljoin(current_url, url)
            normalized_url = self.normalize_url(absolute_url)
            
            if self.is_internal_url(normalized_url):
                target_filepath = self.url_to_filepath(normalized_url)
                relative_path = os.path.relpath(target_filepath, current_filepath.parent)
                return relative_path.replace('\\', '/')
        except Exception as e:
            self.logger.debug(f"Could not convert URL {url}: {e}")
            
        return url
        
    def download_worker(self, url_depth_pair):
        """Worker function for threaded downloading"""
        url, depth = url_depth_pair
        
        # Skip if already processed
        if url in self.downloaded_urls or depth > self.max_depth:
            return []
            
        # Skip if not allowed by robots.txt
        if not self.can_fetch(url):
            self.logger.warning(f"Robots.txt disallows: {url}")
            return []
            
        self.logger.info(f"Processing: {url} (depth: {depth})")
        
        # Download the file
        filepath = self.url_to_filepath(url)
        new_urls = []
        
        if self.download_file_with_retry(url, filepath):
            # Process content for link extraction and conversion
            try:
                asset_type = self.get_asset_type(url)
                
                if asset_type in ['html']:
                    content = filepath.read_text(encoding='utf-8')
                    
                    # Extract links
                    if self.is_internal_url(url):
                        links = self.extract_links_advanced(content, url)
                        for link in links:
                            if link not in self.downloaded_urls:
                                if self.is_internal_url(link):
                                    link_asset_type = self.get_asset_type(link)
                                    if link_asset_type == 'html':
                                        new_urls.append((link, depth + 1))
                                    else:
                                        new_urls.append((link, depth))
                                        
                    # Convert links
                    converted_content = self.convert_links_advanced(content, url, 'html')
                    filepath.write_text(converted_content, encoding='utf-8')
                    
                elif asset_type == 'css':
                    content = filepath.read_text(encoding='utf-8')
                    
                    # Extract CSS URLs
                    css_urls = self.extract_css_urls(content, url)
                    for css_url in css_urls:
                        if css_url not in self.downloaded_urls and self.is_internal_url(css_url):
                            new_urls.append((css_url, depth))
                            
                    # Convert CSS links
                    converted_content = self.convert_links_advanced(content, url, 'css')
                    filepath.write_text(converted_content, encoding='utf-8')
                    
            except Exception as e:
                self.logger.error(f"Error processing {url}: {e}")
                
        # Respectful delay
        if self.delay > 0:
            time.sleep(self.delay)
            
        return new_urls
        
    def download_website(self):
        """Main download method with optional threading"""
        self.logger.info(f"Starting download of {self.base_url}")
        self.logger.info(f"Output directory: {self.output_dir.absolute()}")
        self.logger.info(f"Max workers: {self.max_workers}")
        
        if self.max_workers > 1:
            self.download_threaded()
        else:
            self.download_sequential()
            
        self.logger.info(f"Download completed. Downloaded {len(self.downloaded_urls)} files.")
        if self.failed_urls:
            self.logger.warning(f"Failed to download {len(self.failed_urls)} files.")
            
    def download_sequential(self):
        """Sequential downloading (single-threaded)"""
        while self.url_queue:
            url_depth_pair = self.url_queue.popleft()
            new_urls = self.download_worker(url_depth_pair)
            self.url_queue.extend(new_urls)
            
    def download_threaded(self):
        """Multi-threaded downloading"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while self.url_queue:
                # Submit batch of URLs
                batch_size = min(len(self.url_queue), self.max_workers * 2)
                batch = [self.url_queue.popleft() for _ in range(batch_size)]
                
                # Submit tasks
                future_to_url = {executor.submit(self.download_worker, url_pair): url_pair for url_pair in batch}
                
                # Collect results
                for future in as_completed(future_to_url):
                    try:
                        new_urls = future.result()
                        self.url_queue.extend(new_urls)
                    except Exception as e:
                        url_pair = future_to_url[future]
                        self.logger.error(f"Error processing {url_pair[0]}: {e}")
                        
    def verify_completeness(self):
        """Verify download completeness"""
        self.logger.info("Verifying download completeness...")
        
        missing_files = []
        broken_links = []
        
        for url in self.downloaded_urls:
            filepath = self.url_aliases.get(url)
            if filepath and not filepath.exists():
                missing_files.append(url)
                
        # Check for broken internal links in HTML files
        html_files = [f for f in self.output_dir.rglob('*.html')]
        for html_file in html_files:
            try:
                content = html_file.read_text(encoding='utf-8')
                soup = BeautifulSoup(content, 'lxml')
                
                for link in soup.find_all(['a', 'link'], href=True):
                    href = link['href']
                    if not href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                        target_file = html_file.parent / href
                        if not target_file.exists():
                            broken_links.append((str(html_file), href))
                            
            except Exception as e:
                self.logger.error(f"Error checking {html_file}: {e}")
                
        # Report results
        if missing_files:
            self.logger.warning(f"Missing files: {len(missing_files)}")
            for url in missing_files[:10]:  # Show first 10
                self.logger.warning(f"  Missing: {url}")
                
        if broken_links:
            self.logger.warning(f"Broken links: {len(broken_links)}")
            for file_path, link in broken_links[:10]:  # Show first 10
                self.logger.warning(f"  Broken link in {file_path}: {link}")
                
        return len(missing_files) == 0 and len(broken_links) == 0
        
    def generate_advanced_report(self):
        """Generate comprehensive download report"""
        report_file = self.output_dir / 'advanced_download_report.json'
        
        report = {
            'base_url': self.base_url,
            'output_directory': str(self.output_dir.absolute()),
            'download_stats': dict(self.download_stats),
            'total_downloaded': len(self.downloaded_urls),
            'total_failed': len(self.failed_urls),
            'failed_urls': list(self.failed_urls),
            'config': self.config,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Also create text report
        text_report_file = self.output_dir / 'advanced_download_report.txt'
        with open(text_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Advanced Website Download Report\n")
            f.write(f"================================\n\n")
            f.write(f"Base URL: {self.base_url}\n")
            f.write(f"Output Directory: {self.output_dir.absolute()}\n")
            f.write(f"Download Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Download Statistics:\n")
            f.write(f"-------------------\n")
            for asset_type, count in self.download_stats.items():
                f.write(f"  {asset_type.capitalize()}: {count}\n")
            f.write(f"  Total Downloaded: {len(self.downloaded_urls)}\n")
            f.write(f"  Total Failed: {len(self.failed_urls)}\n\n")
            
            if self.failed_urls:
                f.write(f"Failed URLs:\n")
                f.write(f"------------\n")
                for url in sorted(self.failed_urls):
                    f.write(f"  - {url}\n")
                    
        self.logger.info(f"Advanced report generated: {report_file}")


def load_config(config_file=None, **kwargs):
    """Load configuration from file or command line arguments"""
    config = {
        'delay': 1.0,
        'max_depth': 10,
        'max_workers': 1,
        'verify_ssl': True,
        'include_subdomains': False,
        'force_redownload': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Load from config file if provided
    if config_file and Path(config_file).exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            file_config = json.load(f)
            config.update(file_config)
            
    # Override with command line arguments
    config.update({k: v for k, v in kwargs.items() if v is not None})
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Website Downloader with enhanced features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python advanced_downloader.py https://example.com
  python advanced_downloader.py https://example.com --output ./site --workers 4
  python advanced_downloader.py https://example.com --config config.json
  python advanced_downloader.py https://example.com --verify-completeness

Note: Please respect website terms of service and copyright laws.
"""
    )
    
    parser.add_argument('url', help='Base URL of the website to download')
    parser.add_argument('--output', '-o', default='downloaded_site',
                       help='Output directory (default: downloaded_site)')
    parser.add_argument('--config', '-c', help='Configuration file (JSON)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--max-depth', '-m', type=int, default=10,
                       help='Maximum crawling depth (default: 10)')
    parser.add_argument('--workers', '-w', type=int, default=1,
                       help='Number of worker threads (default: 1)')
    parser.add_argument('--verify-completeness', action='store_true',
                       help='Verify download completeness after completion')
    parser.add_argument('--include-subdomains', action='store_true',
                       help='Include subdomains in download')
    parser.add_argument('--force-redownload', action='store_true',
                       help='Force re-download of existing files')
    parser.add_argument('--no-ssl-verify', action='store_true',
                       help='Disable SSL certificate verification')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)
        
    try:
        # Load configuration
        config = load_config(
            config_file=args.config,
            base_url=args.url,
            output_dir=args.output,
            delay=args.delay,
            max_depth=args.max_depth,
            max_workers=args.workers,
            verify_ssl=not args.no_ssl_verify,
            include_subdomains=args.include_subdomains,
            force_redownload=args.force_redownload
        )
        
        # Create downloader and start
        downloader = AdvancedWebsiteDownloader(config)
        downloader.download_website()
        
        # Verify completeness if requested
        if args.verify_completeness:
            is_complete = downloader.verify_completeness()
            if is_complete:
                print("\n✓ Download verification passed!")
            else:
                print("\n⚠ Download verification found issues. Check the log for details.")
                
        # Generate report
        downloader.generate_advanced_report()
        
        print(f"\nAdvanced download completed! Check the '{args.output}' directory.")
        print(f"Open '{args.output}/index.html' in your browser to start browsing offline.")
        
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()