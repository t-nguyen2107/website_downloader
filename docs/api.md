# API Documentation

This document provides detailed API documentation for the Website Downloader project.

## Table of Contents

- [WebsiteDownloader Class](#websitedownloader-class)
- [AdvancedWebsiteDownloader Class](#advancedwebsitedownloader-class)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Examples](#examples)

## WebsiteDownloader Class

The basic website downloader with essential functionality.

### Constructor

```python
WebsiteDownloader(
    base_url: str,
    output_dir: str,
    delay: float = 1.0,
    max_depth: int = 3,
    user_agent: str = "Website Downloader 1.0"
)
```

#### Parameters

- **base_url** (str): The base URL of the website to download
- **output_dir** (str): Directory where downloaded files will be saved
- **delay** (float, optional): Delay between requests in seconds. Default: 1.0
- **max_depth** (int, optional): Maximum depth for recursive downloading. Default: 3
- **user_agent** (str, optional): User agent string for HTTP requests

### Methods

#### `download_website()`

Downloads the entire website starting from the base URL.

```python
def download_website() -> None
```

**Returns:** None

**Raises:**
- `requests.RequestException`: If network requests fail
- `IOError`: If file operations fail

#### `download_file(url: str, filepath: Path) -> bool`

Downloads a single file from the given URL.

```python
def download_file(url: str, filepath: Path) -> bool
```

**Parameters:**
- **url** (str): URL to download from
- **filepath** (Path): Local path where file should be saved

**Returns:** bool - True if successful, False otherwise

#### `extract_links(html_content: str, base_url: str) -> set`

Extracts all valid links from HTML content.

```python
def extract_links(html_content: str, base_url: str) -> set
```

**Parameters:**
- **html_content** (str): HTML content to parse
- **base_url** (str): Base URL for resolving relative links

**Returns:** set - Set of absolute URLs found in the HTML

#### `extract_css_urls(css_content: str, base_url: str) -> set`

Extracts URLs from CSS content (url() and @import).

```python
def extract_css_urls(css_content: str, base_url: str) -> set
```

**Parameters:**
- **css_content** (str): CSS content to parse
- **base_url** (str): Base URL for resolving relative URLs

**Returns:** set - Set of absolute URLs found in the CSS

#### `is_internal_url(url: str) -> bool`

Checks if a URL belongs to the same domain as the base URL.

```python
def is_internal_url(url: str) -> bool
```

**Parameters:**
- **url** (str): URL to check

**Returns:** bool - True if URL is internal, False otherwise

#### `is_valid_url_scheme(url: str) -> bool`

Validates if a URL has a downloadable scheme (http/https).

```python
def is_valid_url_scheme(url: str) -> bool
```

**Parameters:**
- **url** (str): URL to validate

**Returns:** bool - True if scheme is valid (http/https), False otherwise

#### `normalize_url(url: str, base_url: str) -> str`

Normalizes a URL by resolving relative paths and removing fragments.

```python
def normalize_url(url: str, base_url: str) -> str
```

**Parameters:**
- **url** (str): URL to normalize
- **base_url** (str): Base URL for resolving relative paths

**Returns:** str - Normalized absolute URL

#### `can_fetch(url: str) -> bool`

Checks if a URL can be fetched according to robots.txt.

```python
def can_fetch(url: str) -> bool
```

**Parameters:**
- **url** (str): URL to check

**Returns:** bool - True if URL can be fetched, False otherwise

#### `generate_report() -> Path`

Generates a download report with statistics.

```python
def generate_report() -> Path
```

**Returns:** Path - Path to the generated report file

### Properties

- **downloaded_files** (set): Set of successfully downloaded URLs
- **failed_downloads** (set): Set of URLs that failed to download
- **total_size** (int): Total size of downloaded files in bytes
- **session** (requests.Session): HTTP session for making requests
- **rp** (RobotFileParser): Robots.txt parser instance

## AdvancedWebsiteDownloader Class

Extended downloader with advanced features like multi-threading and enhanced error handling.

### Constructor

```python
AdvancedWebsiteDownloader(
    base_url: str,
    output_dir: str,
    delay: float = 1.0,
    max_depth: int = 3,
    max_workers: int = 5,
    verify_ssl: bool = True,
    include_subdomains: bool = False,
    force_redownload: bool = False,
    ignore_robots: bool = False,
    user_agent: str = "Advanced Website Downloader 1.0",
    config_file: str = None
)
```

#### Additional Parameters

- **max_workers** (int, optional): Number of worker threads. Default: 5
- **verify_ssl** (bool, optional): Whether to verify SSL certificates. Default: True
- **include_subdomains** (bool, optional): Include subdomains in download. Default: False
- **force_redownload** (bool, optional): Redownload existing files. Default: False
- **ignore_robots** (bool, optional): Ignore robots.txt restrictions. Default: False
- **config_file** (str, optional): Path to JSON configuration file

### Additional Methods

#### `extract_links_advanced(html_content: str, base_url: str) -> set`

Advanced link extraction with support for srcset, inline styles, and meta refresh.

```python
def extract_links_advanced(html_content: str, base_url: str) -> set
```

**Parameters:**
- **html_content** (str): HTML content to parse
- **base_url** (str): Base URL for resolving relative links

**Returns:** set - Set of absolute URLs found in the HTML

#### `parse_url_attribute(attr_value: str, base_url: str) -> set`

Parses URL attributes like srcset that may contain multiple URLs.

```python
def parse_url_attribute(attr_value: str, base_url: str) -> set
```

**Parameters:**
- **attr_value** (str): Attribute value to parse
- **base_url** (str): Base URL for resolving relative URLs

**Returns:** set - Set of absolute URLs found in the attribute

#### `verify_completeness() -> set`

Verifies that all referenced files have been downloaded.

```python
def verify_completeness() -> set
```

**Returns:** set - Set of missing URLs that should be downloaded

#### `get_progress() -> float`

Returns the current download progress as a percentage.

```python
def get_progress() -> float
```

**Returns:** float - Progress percentage (0.0 to 1.0)

#### `calculate_backoff(retry_count: int) -> float`

Calculates exponential backoff delay for retries.

```python
def calculate_backoff(retry_count: int) -> float
```

**Parameters:**
- **retry_count** (int): Number of retries attempted

**Returns:** float - Delay in seconds

#### `get_asset_type(url: str) -> str`

Determines the asset type based on file extension.

```python
def get_asset_type(url: str) -> str
```

**Parameters:**
- **url** (str): URL to analyze

**Returns:** str - Asset type ('html', 'css', 'javascript', 'image', 'font', 'other')

### Additional Properties

- **total_files** (int): Total number of files to download
- **completed_files** (int): Number of files completed
- **url_aliases** (dict): URL alias mappings for redirects
- **start_time** (float): Download start timestamp
- **end_time** (float): Download end timestamp

## Configuration

### Configuration File Format

The advanced downloader supports JSON configuration files:

```json
{
  "delay": 1.0,
  "max_depth": 3,
  "max_workers": 5,
  "verify_ssl": true,
  "include_subdomains": false,
  "force_redownload": false,
  "ignore_robots": false,
  "user_agent": "Custom User Agent 1.0"
}
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| delay | float | 1.0 | Delay between requests (seconds) |
| max_depth | int | 3 | Maximum recursion depth |
| max_workers | int | 5 | Number of worker threads |
| verify_ssl | bool | true | Verify SSL certificates |
| include_subdomains | bool | false | Include subdomains in download |
| force_redownload | bool | false | Redownload existing files |
| ignore_robots | bool | false | Ignore robots.txt restrictions |
| user_agent | string | "Advanced Website Downloader 1.0" | HTTP User-Agent header |

## Error Handling

### Exception Types

The downloaders may raise the following exceptions:

- **requests.RequestException**: Network-related errors
- **requests.HTTPError**: HTTP status errors (4xx, 5xx)
- **requests.ConnectionError**: Connection failures
- **requests.Timeout**: Request timeouts
- **IOError**: File system errors
- **ValueError**: Invalid parameter values
- **json.JSONDecodeError**: Configuration file parsing errors

### Error Recovery

The advanced downloader includes automatic error recovery:

1. **Retry Logic**: Failed downloads are retried up to 3 times
2. **Exponential Backoff**: Increasing delays between retries
3. **Graceful Degradation**: Continue downloading other files if some fail
4. **Error Logging**: Detailed error information in logs

### Best Practices

1. **Handle Exceptions**: Always wrap downloader calls in try-catch blocks
2. **Check Return Values**: Verify boolean return values from methods
3. **Monitor Logs**: Check log output for warnings and errors
4. **Validate URLs**: Ensure URLs are properly formatted before downloading
5. **Respect Robots.txt**: Don't ignore robots.txt unless necessary

## Examples

### Basic Usage

```python
from website_downloader import WebsiteDownloader

# Create downloader instance
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    delay=1.0,
    max_depth=2
)

# Download the website
try:
    downloader.download_website()
    print(f"Downloaded {len(downloader.downloaded_files)} files")
    print(f"Failed to download {len(downloader.failed_downloads)} files")
except Exception as e:
    print(f"Download failed: {e}")

# Generate report
report_path = downloader.generate_report()
print(f"Report saved to: {report_path}")
```

### Advanced Usage

```python
from advanced_downloader import AdvancedWebsiteDownloader

# Create advanced downloader with configuration
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    config_file="config.json",
    max_workers=10,
    include_subdomains=True
)

# Download with progress monitoring
try:
    downloader.download_website()
    
    # Check progress
    progress = downloader.get_progress()
    print(f"Download progress: {progress:.1%}")
    
    # Verify completeness
    missing = downloader.verify_completeness()
    if missing:
        print(f"Missing files: {len(missing)}")
        # Optionally download missing files
        
except Exception as e:
    print(f"Download failed: {e}")

# Generate advanced report
report_path = downloader.generate_report()
print(f"Advanced report saved to: {report_path}")
```

### Custom Configuration

```python
import json
from advanced_downloader import AdvancedWebsiteDownloader

# Create custom configuration
config = {
    "delay": 0.5,
    "max_depth": 5,
    "max_workers": 8,
    "verify_ssl": False,
    "include_subdomains": True,
    "user_agent": "My Custom Bot 1.0"
}

# Save configuration
with open("custom_config.json", "w") as f:
    json.dump(config, f, indent=2)

# Use configuration
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    config_file="custom_config.json"
)

downloader.download_website()
```

### Error Handling Example

```python
from website_downloader import WebsiteDownloader
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site"
)

try:
    downloader.download_website()
except requests.ConnectionError:
    print("Network connection failed")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except IOError as e:
    print(f"File system error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Always generate report
    if downloader.downloaded_files or downloader.failed_downloads:
        report_path = downloader.generate_report()
        print(f"Report saved to: {report_path}")
```

## Performance Considerations

### Memory Usage

- **File Caching**: Downloaded files are written to disk immediately
- **URL Sets**: Keep track of URLs in memory (scales with site size)
- **Session Reuse**: HTTP sessions are reused for efficiency

### Network Optimization

- **Connection Pooling**: Automatic connection reuse
- **Compression**: Automatic gzip/deflate handling
- **Keep-Alive**: Persistent connections when possible
- **Timeouts**: Configurable request timeouts

### Threading Considerations

- **Thread Safety**: Advanced downloader is thread-safe
- **Worker Limits**: Adjust max_workers based on target server capacity
- **Rate Limiting**: Use delay parameter to respect server limits

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues and solutions.