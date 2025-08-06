# Usage Examples

This document provides practical examples of using the Website Downloader for various scenarios.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Advanced Examples](#advanced-examples)
- [Configuration Examples](#configuration-examples)
- [Specialized Use Cases](#specialized-use-cases)
- [Integration Examples](#integration-examples)
- [Error Handling Examples](#error-handling-examples)

## Basic Examples

### Simple Website Download

```python
from website_downloader import WebsiteDownloader

# Download a simple website
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_example"
)

downloader.download_website()
print(f"Downloaded {len(downloader.downloaded_files)} files")
```

### Download with Custom Settings

```python
from website_downloader import WebsiteDownloader

# Download with custom delay and depth
downloader = WebsiteDownloader(
    base_url="https://docs.python.org",
    output_dir="./python_docs",
    delay=2.0,  # 2 seconds between requests
    max_depth=2,  # Only go 2 levels deep
    user_agent="Python Docs Downloader 1.0"
)

downloader.download_website()

# Generate and view report
report_path = downloader.generate_report()
print(f"Download report saved to: {report_path}")
```

### Download Specific File Types

```python
from website_downloader import WebsiteDownloader
import os

class SelectiveDownloader(WebsiteDownloader):
    """Custom downloader that only downloads specific file types."""
    
    def __init__(self, *args, allowed_extensions=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_extensions = allowed_extensions or ['.html', '.css', '.js']
    
    def should_download_file(self, url):
        """Check if file should be downloaded based on extension."""
        _, ext = os.path.splitext(url.lower())
        return ext in self.allowed_extensions
    
    def download_file(self, url, filepath):
        """Override to add file type filtering."""
        if not self.should_download_file(url):
            self.logger.info(f"Skipping {url} (file type not allowed)")
            return False
        return super().download_file(url, filepath)

# Use the selective downloader
downloader = SelectiveDownloader(
    base_url="https://example.com",
    output_dir="./html_css_js_only",
    allowed_extensions=['.html', '.css', '.js', '.png', '.jpg']
)

downloader.download_website()
```

## Advanced Examples

### Multi-threaded Download with Progress Monitoring

```python
from advanced_downloader import AdvancedWebsiteDownloader
import time
import threading

def monitor_progress(downloader, interval=5):
    """Monitor download progress in a separate thread."""
    while downloader.completed_files < downloader.total_files:
        progress = downloader.get_progress()
        print(f"Progress: {progress:.1%} ({downloader.completed_files}/{downloader.total_files})")
        time.sleep(interval)

# Create advanced downloader
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./advanced_download",
    max_workers=8,
    delay=0.5,
    max_depth=3
)

# Start progress monitoring in background
monitor_thread = threading.Thread(
    target=monitor_progress,
    args=(downloader, 2),  # Update every 2 seconds
    daemon=True
)
monitor_thread.start()

# Download website
downloader.download_website()

# Final progress
print(f"Download complete: {downloader.get_progress():.1%}")
print(f"Total time: {downloader.end_time - downloader.start_time:.2f} seconds")
```

### Download with Subdomain Support

```python
from advanced_downloader import AdvancedWebsiteDownloader

# Download including subdomains
downloader = AdvancedWebsiteDownloader(
    base_url="https://docs.example.com",
    output_dir="./docs_with_subdomains",
    include_subdomains=True,  # Include api.example.com, blog.example.com, etc.
    max_workers=6,
    delay=1.0
)

downloader.download_website()

# Check what domains were downloaded
domains = set()
for url in downloader.downloaded_files:
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    domains.add(domain)

print("Downloaded from domains:")
for domain in sorted(domains):
    print(f"  - {domain}")
```

### Download with Completeness Verification

```python
from advanced_downloader import AdvancedWebsiteDownloader

# Download with verification
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./verified_download",
    max_workers=4
)

# Initial download
downloader.download_website()

# Verify completeness and download missing files
missing_files = downloader.verify_completeness()
if missing_files:
    print(f"Found {len(missing_files)} missing files. Downloading...")
    
    # Download missing files
    for url in missing_files:
        filepath = downloader.url_to_filepath(url)
        success = downloader.download_file(url, filepath)
        if success:
            print(f"Downloaded missing file: {url}")
        else:
            print(f"Failed to download: {url}")
    
    # Verify again
    still_missing = downloader.verify_completeness()
    print(f"Still missing after retry: {len(still_missing)} files")
else:
    print("Download is complete - no missing files!")
```

## Configuration Examples

### Using Configuration Files

```python
import json
from advanced_downloader import AdvancedWebsiteDownloader

# Create configuration file
config = {
    "delay": 1.5,
    "max_depth": 4,
    "max_workers": 6,
    "verify_ssl": True,
    "include_subdomains": False,
    "force_redownload": False,
    "ignore_robots": False,
    "user_agent": "Professional Website Archiver 2.0"
}

# Save configuration
with open("archive_config.json", "w") as f:
    json.dump(config, f, indent=2)

# Use configuration
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./archived_site",
    config_file="archive_config.json"
)

downloader.download_website()
```

### Environment-Specific Configurations

```python
import os
import json
from advanced_downloader import AdvancedWebsiteDownloader

# Different configs for different environments
configs = {
    "development": {
        "delay": 0.1,
        "max_workers": 2,
        "verify_ssl": False,
        "ignore_robots": True
    },
    "production": {
        "delay": 2.0,
        "max_workers": 3,
        "verify_ssl": True,
        "ignore_robots": False
    }
}

# Get environment (default to development)
env = os.getenv("ENVIRONMENT", "development")
config = configs[env]

print(f"Using {env} configuration")

# Create downloader with environment-specific config
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir=f"./download_{env}",
    **config
)

downloader.download_website()
```

## Specialized Use Cases

### Documentation Site Archival

```python
from advanced_downloader import AdvancedWebsiteDownloader
import datetime

class DocumentationArchiver(AdvancedWebsiteDownloader):
    """Specialized downloader for documentation sites."""
    
    def __init__(self, *args, **kwargs):
        # Documentation-specific defaults
        kwargs.setdefault('delay', 0.5)  # Faster for docs
        kwargs.setdefault('max_depth', 5)  # Deeper for docs
        kwargs.setdefault('max_workers', 8)  # More workers
        kwargs.setdefault('user_agent', 'Documentation Archiver 1.0')
        super().__init__(*args, **kwargs)
    
    def generate_report(self):
        """Generate documentation-specific report."""
        report_path = super().generate_report()
        
        # Add documentation-specific metadata
        timestamp = datetime.datetime.now().isoformat()
        metadata = {
            "archive_date": timestamp,
            "base_url": self.base_url,
            "total_pages": len([url for url in self.downloaded_files if url.endswith('.html')]),
            "total_assets": len(self.downloaded_files) - len([url for url in self.downloaded_files if url.endswith('.html')]),
            "failed_downloads": list(self.failed_downloads)
        }
        
        metadata_path = self.output_dir / "archive_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return report_path

# Archive documentation
archiver = DocumentationArchiver(
    base_url="https://docs.python.org/3/",
    output_dir="./python_docs_archive"
)

archiver.download_website()
print(f"Documentation archived with {len(archiver.downloaded_files)} files")
```

### Blog Archive with Date Filtering

```python
from advanced_downloader import AdvancedWebsiteDownloader
from datetime import datetime, timedelta
import re

class BlogArchiver(AdvancedWebsiteDownloader):
    """Archive blog posts from a specific date range."""
    
    def __init__(self, *args, start_date=None, end_date=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_date = start_date
        self.end_date = end_date
    
    def should_download_url(self, url):
        """Check if URL should be downloaded based on date."""
        if not self.start_date and not self.end_date:
            return True
        
        # Extract date from URL (example pattern: /2023/12/post-title/)
        date_match = re.search(r'/(\d{4})/(\d{2})/', url)
        if not date_match:
            return True  # Download if no date found
        
        year, month = int(date_match.group(1)), int(date_match.group(2))
        post_date = datetime(year, month, 1)
        
        if self.start_date and post_date < self.start_date:
            return False
        if self.end_date and post_date > self.end_date:
            return False
        
        return True
    
    def extract_links_advanced(self, html_content, base_url):
        """Override to filter links by date."""
        all_links = super().extract_links_advanced(html_content, base_url)
        filtered_links = {url for url in all_links if self.should_download_url(url)}
        
        filtered_count = len(all_links) - len(filtered_links)
        if filtered_count > 0:
            self.logger.info(f"Filtered out {filtered_count} URLs based on date range")
        
        return filtered_links

# Archive blog posts from last 6 months
end_date = datetime.now()
start_date = end_date - timedelta(days=180)

blog_archiver = BlogArchiver(
    base_url="https://blog.example.com",
    output_dir="./blog_archive_6months",
    start_date=start_date,
    end_date=end_date,
    max_workers=4
)

blog_archiver.download_website()
print(f"Archived blog posts from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
```

### E-commerce Product Catalog

```python
from advanced_downloader import AdvancedWebsiteDownloader
import json
import re
from urllib.parse import urljoin, urlparse

class ProductCatalogDownloader(AdvancedWebsiteDownloader):
    """Download product catalog with metadata extraction."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = []
    
    def extract_product_info(self, html_content, url):
        """Extract product information from HTML."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Example product extraction (customize for specific sites)
        product = {
            'url': url,
            'title': None,
            'price': None,
            'description': None,
            'images': []
        }
        
        # Extract title
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            product['title'] = title_elem.get_text().strip()
        
        # Extract price (example patterns)
        price_patterns = [r'\$([\d,]+\.\d{2})', r'Price: \$([\d,]+)']
        for pattern in price_patterns:
            price_match = re.search(pattern, html_content)
            if price_match:
                product['price'] = price_match.group(1)
                break
        
        # Extract product images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and ('product' in src.lower() or 'item' in src.lower()):
                full_url = urljoin(url, src)
                product['images'].append(full_url)
        
        return product
    
    def download_file(self, url, filepath):
        """Override to extract product info from HTML files."""
        success = super().download_file(url, filepath)
        
        if success and filepath.suffix.lower() == '.html':
            try:
                html_content = filepath.read_text(encoding='utf-8')
                if 'product' in url.lower() or 'item' in url.lower():
                    product_info = self.extract_product_info(html_content, url)
                    self.products.append(product_info)
                    self.logger.info(f"Extracted product info: {product_info['title']}")
            except Exception as e:
                self.logger.warning(f"Failed to extract product info from {url}: {e}")
        
        return success
    
    def generate_report(self):
        """Generate report with product catalog."""
        report_path = super().generate_report()
        
        # Save product catalog
        catalog_path = self.output_dir / "product_catalog.json"
        with open(catalog_path, 'w') as f:
            json.dump(self.products, f, indent=2)
        
        print(f"Product catalog saved to: {catalog_path}")
        print(f"Total products found: {len(self.products)}")
        
        return report_path

# Download product catalog
catalog_downloader = ProductCatalogDownloader(
    base_url="https://shop.example.com",
    output_dir="./product_catalog",
    max_workers=3,
    delay=1.0
)

catalog_downloader.download_website()
catalog_downloader.generate_report()
```

## Integration Examples

### Integration with Scrapy

```python
from website_downloader import WebsiteDownloader
import scrapy
from scrapy.crawler import CrawlerProcess

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'
    
    def __init__(self, downloader, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloader = downloader
        self.start_urls = [downloader.base_url]
    
    def parse(self, response):
        # Use downloader to save the page
        filepath = self.downloader.url_to_filepath(response.url)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.body)
        
        # Extract and follow links
        links = self.downloader.extract_links(response.text, response.url)
        for link in links:
            if self.downloader.is_internal_url(link):
                yield scrapy.Request(link, callback=self.parse)

# Combine Website Downloader with Scrapy
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./scrapy_download"
)

process = CrawlerProcess({
    'USER_AGENT': downloader.user_agent,
    'DOWNLOAD_DELAY': downloader.delay,
})

process.crawl(WebsiteSpider, downloader=downloader)
process.start()
```

### Integration with Selenium

```python
from advanced_downloader import AdvancedWebsiteDownloader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class JavaScriptDownloader(AdvancedWebsiteDownloader):
    """Downloader that can handle JavaScript-heavy sites."""
    
    def __init__(self, *args, use_selenium=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_selenium = use_selenium
        self.driver = None
        
        if use_selenium:
            self.setup_selenium()
    
    def setup_selenium(self):
        """Setup Selenium WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def download_file(self, url, filepath):
        """Download file, using Selenium for HTML pages if enabled."""
        if self.use_selenium and url.endswith('.html'):
            return self.download_with_selenium(url, filepath)
        else:
            return super().download_file(url, filepath)
    
    def download_with_selenium(self, url, filepath):
        """Download HTML page using Selenium to execute JavaScript."""
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for JavaScript to execute
            
            # Get page source after JavaScript execution
            html_content = self.driver.page_source
            
            # Save to file
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(html_content, encoding='utf-8')
            
            self.downloaded_files.add(url)
            self.total_size += len(html_content.encode('utf-8'))
            
            self.logger.info(f"Downloaded with Selenium: {url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Selenium download failed for {url}: {e}")
            self.failed_downloads.add(url)
            return False
    
    def __del__(self):
        """Cleanup Selenium driver."""
        if self.driver:
            self.driver.quit()

# Use JavaScript-capable downloader
js_downloader = JavaScriptDownloader(
    base_url="https://spa-example.com",
    output_dir="./spa_download",
    use_selenium=True,
    max_workers=2  # Reduce workers when using Selenium
)

js_downloader.download_website()
```

## Error Handling Examples

### Robust Download with Retry Logic

```python
from advanced_downloader import AdvancedWebsiteDownloader
import requests
import time
import logging

class RobustDownloader(AdvancedWebsiteDownloader):
    """Downloader with enhanced error handling and retry logic."""
    
    def __init__(self, *args, max_retries=5, retry_delay=2, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_counts = {}
    
    def download_file(self, url, filepath):
        """Download with enhanced retry logic."""
        retry_count = 0
        
        while retry_count <= self.max_retries:
            try:
                # Attempt download
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Save file
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_bytes(response.content)
                
                # Update statistics
                self.downloaded_files.add(url)
                self.total_size += len(response.content)
                
                if retry_count > 0:
                    self.logger.info(f"Downloaded {url} after {retry_count} retries")
                else:
                    self.logger.info(f"Downloaded: {url}")
                
                return True
                
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout for {url}, retry {retry_count + 1}/{self.max_retries}")
            except requests.exceptions.ConnectionError:
                self.logger.warning(f"Connection error for {url}, retry {retry_count + 1}/{self.max_retries}")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code in [429, 503, 504]:  # Rate limit or server errors
                    self.logger.warning(f"Server error {e.response.status_code} for {url}, retry {retry_count + 1}/{self.max_retries}")
                else:
                    self.logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
                    break  # Don't retry for client errors
            except Exception as e:
                self.logger.error(f"Unexpected error for {url}: {e}")
                break
            
            retry_count += 1
            if retry_count <= self.max_retries:
                delay = self.retry_delay * (2 ** (retry_count - 1))  # Exponential backoff
                self.logger.info(f"Waiting {delay} seconds before retry...")
                time.sleep(delay)
        
        # All retries failed
        self.failed_downloads.add(url)
        self.retry_counts[url] = retry_count
        self.logger.error(f"Failed to download {url} after {retry_count} attempts")
        return False
    
    def generate_report(self):
        """Generate enhanced report with retry statistics."""
        report_path = super().generate_report()
        
        # Add retry statistics to report
        if self.retry_counts:
            retry_report = self.output_dir / "retry_statistics.txt"
            with open(retry_report, 'w') as f:
                f.write("Retry Statistics\n")
                f.write("================\n\n")
                
                for url, retries in self.retry_counts.items():
                    f.write(f"{url}: {retries} retries\n")
                
                avg_retries = sum(self.retry_counts.values()) / len(self.retry_counts)
                f.write(f"\nAverage retries per failed URL: {avg_retries:.2f}\n")
            
            print(f"Retry statistics saved to: {retry_report}")
        
        return report_path

# Use robust downloader
robust_downloader = RobustDownloader(
    base_url="https://unreliable-site.com",
    output_dir="./robust_download",
    max_retries=3,
    retry_delay=1,
    delay=0.5
)

robust_downloader.download_website()
```

### Graceful Degradation Example

```python
from website_downloader import WebsiteDownloader
import requests
import logging

def download_with_fallback(urls, output_dir):
    """Download from multiple URLs with fallback options."""
    
    for i, url in enumerate(urls):
        try:
            print(f"Attempting download from: {url}")
            
            downloader = WebsiteDownloader(
                base_url=url,
                output_dir=f"{output_dir}_attempt_{i+1}",
                delay=1.0,
                max_depth=2
            )
            
            downloader.download_website()
            
            if len(downloader.downloaded_files) > 0:
                print(f"Success! Downloaded {len(downloader.downloaded_files)} files from {url}")
                return downloader
            else:
                print(f"No files downloaded from {url}, trying next option...")
                
        except requests.exceptions.ConnectionError:
            print(f"Connection failed for {url}, trying next option...")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error for {url}: {e}, trying next option...")
        except Exception as e:
            print(f"Unexpected error for {url}: {e}, trying next option...")
    
    print("All download attempts failed")
    return None

# Try multiple mirror sites
mirror_urls = [
    "https://primary-site.com",
    "https://mirror1.example.com",
    "https://mirror2.example.com",
    "https://backup.example.com"
]

successful_downloader = download_with_fallback(mirror_urls, "./fallback_download")
if successful_downloader:
    successful_downloader.generate_report()
```

These examples demonstrate various ways to use the Website Downloader for different scenarios, from simple downloads to complex, specialized use cases. Choose the approach that best fits your specific requirements and customize as needed.