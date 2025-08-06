#!/usr/bin/env python3
"""
Website Downloader - Download entire websites for offline browsing

This script recursively downloads a website including all pages, images, CSS, JS,
and other assets, then converts internal links for offline navigation.

Features:
- Recursive crawling of internal links
- Asset collection (images, CSS, JS, fonts, etc.)
- Link conversion for offline browsing
- Respectful crawling with delays
- Progress tracking and logging
- Resume capability

Usage:
    python website_downloader.py <url> [options]

Example:
    python website_downloader.py https://example.com --output ./downloaded_site
"""

import os
import sys
import re
import time
import argparse
import logging
import urllib.parse
from pathlib import Path
from collections import deque
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote


class WebsiteDownloader:
    def __init__(self, base_url, output_dir="downloaded_site", delay=1.0, max_depth=10):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.max_depth = max_depth
        
        # Track downloaded URLs and failed downloads
        self.downloaded_urls = set()
        self.failed_urls = set()
        self.url_queue = deque([(base_url, 0)])  # (url, depth)
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Setup session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Check robots.txt
        self.check_robots_txt()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.output_dir / 'download.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def check_robots_txt(self):
        """Check robots.txt for crawling permissions"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            self.robots_parser = rp
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
        """Check if URL belongs to the same domain"""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''
        
    def normalize_url(self, url):
        """Normalize URL for consistent handling"""
        # Remove fragment
        url = url.split('#')[0]
        # Decode URL encoding
        url = unquote(url)
        return url
        
    def url_to_filepath(self, url):
        """Convert URL to local file path"""
        parsed = urlparse(url)
        path = parsed.path.lstrip('/')
        
        # Handle root URL
        if not path or path.endswith('/'):
            path = path + 'index.html'
        
        # Add .html extension if no extension
        if '.' not in Path(path).name:
            path = path + '.html'
            
        # Handle query parameters
        if parsed.query:
            path = path + '_' + parsed.query.replace('&', '_').replace('=', '-')
            
        return self.output_dir / path
        
    def download_file(self, url, filepath):
        """Download a file from URL to filepath"""
        try:
            # Create directory if needed
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Skip if already exists
            if filepath.exists():
                self.logger.debug(f"File already exists: {filepath}")
                return True
                
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Write file
            if 'text' in response.headers.get('content-type', '').lower():
                filepath.write_text(response.text, encoding='utf-8')
            else:
                filepath.write_bytes(response.content)
                
            self.logger.info(f"Downloaded: {url} -> {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to download {url}: {e}")
            self.failed_urls.add(url)
            return False
            
    def extract_links(self, html_content, base_url):
        """Extract all links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        # Extract different types of links
        selectors = {
            'a': 'href',
            'link': 'href',
            'script': 'src',
            'img': 'src',
            'source': 'src',
            'iframe': 'src',
            'embed': 'src',
            'object': 'data'
        }
        
        for tag, attr in selectors.items():
            for element in soup.find_all(tag, {attr: True}):
                url = element[attr]
                if url:
                    absolute_url = urljoin(base_url, url)
                    links.add(self.normalize_url(absolute_url))
                    
        # Extract CSS @import and url() references
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                css_urls = self.extract_css_urls(style_tag.string, base_url)
                links.update(css_urls)
                
        return links
        
    def extract_css_urls(self, css_content, base_url):
        """Extract URLs from CSS content"""
        urls = set()
        
        # Find url() references
        url_pattern = r'url\(["\']?([^"\')]+)["\']?\)'
        for match in re.finditer(url_pattern, css_content):
            url = match.group(1)
            absolute_url = urljoin(base_url, url)
            urls.add(self.normalize_url(absolute_url))
            
        # Find @import references
        import_pattern = r'@import\s+["\']([^"\')]+)["\']'
        for match in re.finditer(import_pattern, css_content):
            url = match.group(1)
            absolute_url = urljoin(base_url, url)
            urls.add(self.normalize_url(absolute_url))
            
        return urls
        
    def convert_links_in_html(self, html_content, current_url):
        """Convert absolute links to relative paths for offline browsing"""
        soup = BeautifulSoup(html_content, 'html.parser')
        current_filepath = self.url_to_filepath(current_url)
        
        # Convert different types of links
        selectors = {
            'a': 'href',
            'link': 'href',
            'script': 'src',
            'img': 'src',
            'source': 'src',
            'iframe': 'src',
            'embed': 'src',
            'object': 'data'
        }
        
        for tag, attr in selectors.items():
            for element in soup.find_all(tag, {attr: True}):
                url = element[attr]
                if url and self.is_internal_url(urljoin(current_url, url)):
                    absolute_url = urljoin(current_url, url)
                    normalized_url = self.normalize_url(absolute_url)
                    target_filepath = self.url_to_filepath(normalized_url)
                    
                    # Calculate relative path
                    try:
                        relative_path = os.path.relpath(target_filepath, current_filepath.parent)
                        element[attr] = relative_path.replace('\\', '/')
                    except ValueError:
                        # Keep original if relative path calculation fails
                        pass
                        
        return str(soup)
        
    def download_website(self):
        """Main method to download the entire website"""
        self.logger.info(f"Starting download of {self.base_url}")
        self.logger.info(f"Output directory: {self.output_dir.absolute()}")
        
        while self.url_queue:
            current_url, depth = self.url_queue.popleft()
            
            # Skip if already downloaded or depth exceeded
            if current_url in self.downloaded_urls or depth > self.max_depth:
                continue
                
            # Skip if not allowed by robots.txt
            if not self.can_fetch(current_url):
                self.logger.warning(f"Robots.txt disallows: {current_url}")
                continue
                
            self.logger.info(f"Processing: {current_url} (depth: {depth})")
            
            # Download the file
            filepath = self.url_to_filepath(current_url)
            if self.download_file(current_url, filepath):
                self.downloaded_urls.add(current_url)
                
                # If it's an HTML file, extract links and convert them
                if filepath.suffix.lower() in ['.html', '.htm'] or 'html' in filepath.name:
                    try:
                        html_content = filepath.read_text(encoding='utf-8')
                        
                        # Extract links for further crawling
                        if self.is_internal_url(current_url):
                            links = self.extract_links(html_content, current_url)
                            for link in links:
                                if link not in self.downloaded_urls:
                                    if self.is_internal_url(link):
                                        # Add HTML pages to queue for crawling
                                        if self.is_likely_html(link):
                                            self.url_queue.append((link, depth + 1))
                                        else:
                                            # Add assets to queue with same depth
                                            self.url_queue.append((link, depth))
                                            
                        # Convert links for offline browsing
                        converted_html = self.convert_links_in_html(html_content, current_url)
                        filepath.write_text(converted_html, encoding='utf-8')
                        
                    except Exception as e:
                        self.logger.error(f"Error processing HTML {current_url}: {e}")
                        
                # Handle CSS files
                elif filepath.suffix.lower() == '.css':
                    try:
                        css_content = filepath.read_text(encoding='utf-8')
                        css_urls = self.extract_css_urls(css_content, current_url)
                        for url in css_urls:
                            if url not in self.downloaded_urls and self.is_internal_url(url):
                                self.url_queue.append((url, depth))
                    except Exception as e:
                        self.logger.error(f"Error processing CSS {current_url}: {e}")
                        
            # Respectful delay
            time.sleep(self.delay)
            
        self.logger.info(f"Download completed. Downloaded {len(self.downloaded_urls)} files.")
        if self.failed_urls:
            self.logger.warning(f"Failed to download {len(self.failed_urls)} files.")
            
    def is_likely_html(self, url):
        """Check if URL is likely to be an HTML page"""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Common non-HTML extensions
        non_html_extensions = {
            '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
            '.pdf', '.zip', '.tar', '.gz', '.mp4', '.mp3', '.avi', '.mov',
            '.woff', '.woff2', '.ttf', '.eot', '.xml', '.json'
        }
        
        for ext in non_html_extensions:
            if path.endswith(ext):
                return False
                
        return True
        
    def generate_report(self):
        """Generate a download report"""
        report_file = self.output_dir / 'download_report.txt'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Website Download Report\n")
            f.write(f"======================\n\n")
            f.write(f"Base URL: {self.base_url}\n")
            f.write(f"Output Directory: {self.output_dir.absolute()}\n")
            f.write(f"Total Downloaded: {len(self.downloaded_urls)}\n")
            f.write(f"Failed Downloads: {len(self.failed_urls)}\n\n")
            
            if self.failed_urls:
                f.write("Failed URLs:\n")
                for url in sorted(self.failed_urls):
                    f.write(f"  - {url}\n")
                    
        self.logger.info(f"Report generated: {report_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Download entire websites for offline browsing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python website_downloader.py https://example.com
  python website_downloader.py https://example.com --output ./my_site --delay 2
  python website_downloader.py https://example.com --max-depth 5

Note: Please respect website terms of service and copyright laws.
"""
    )
    
    parser.add_argument('url', help='Base URL of the website to download')
    parser.add_argument('--output', '-o', default='downloaded_site',
                       help='Output directory (default: downloaded_site)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--max-depth', '-m', type=int, default=10,
                       help='Maximum crawling depth (default: 10)')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)
        
    try:
        downloader = WebsiteDownloader(
            base_url=args.url,
            output_dir=args.output,
            delay=args.delay,
            max_depth=args.max_depth
        )
        
        downloader.download_website()
        downloader.generate_report()
        
        print(f"\nDownload completed! Check the '{args.output}' directory.")
        print(f"Open '{args.output}/index.html' in your browser to start browsing offline.")
        
    except KeyboardInterrupt:
        print("\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()