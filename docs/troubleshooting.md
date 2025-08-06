# Troubleshooting Guide

This guide helps you resolve common issues when using the Website Downloader.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Download Problems](#download-problems)
- [Performance Issues](#performance-issues)
- [SSL/TLS Issues](#ssltls-issues)
- [File System Issues](#file-system-issues)
- [Network Issues](#network-issues)
- [Configuration Problems](#configuration-problems)
- [Common Error Messages](#common-error-messages)
- [Debugging Tips](#debugging-tips)

## Installation Issues

### Problem: Module not found errors

**Error:**
```
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'beautifulsoup4'
```

**Solution:**
```bash
# Install required dependencies
pip install -r requirements.txt

# Or install individually
pip install requests beautifulsoup4 lxml
```

### Problem: Permission denied during installation

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Use --user flag to install for current user only
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: Python version compatibility

**Error:**
```
SyntaxError: invalid syntax
```

**Solution:**
- Ensure you're using Python 3.7 or higher
- Check your Python version: `python --version`
- Use `python3` instead of `python` if needed

## Download Problems

### Problem: No files downloaded

**Possible Causes:**
1. **Robots.txt blocking**: The website's robots.txt file may be blocking the downloader
2. **Invalid URL**: The base URL might be incorrect or inaccessible
3. **Network connectivity**: Internet connection issues
4. **SSL certificate problems**: HTTPS sites with invalid certificates

**Solutions:**
```python
# Check if robots.txt is blocking
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site"
)
print(f"Can fetch: {downloader.can_fetch('https://example.com/')}")

# Ignore robots.txt (use responsibly)
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    ignore_robots=True
)

# Disable SSL verification (not recommended for production)
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    verify_ssl=False
)
```

### Problem: Partial downloads

**Symptoms:**
- Some files downloaded, others failed
- Missing CSS, images, or other assets

**Solutions:**
```python
# Increase max_depth to get more files
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    max_depth=5  # Default is 3
)

# Include subdomains
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    include_subdomains=True
)

# Check for missing files
missing = downloader.verify_completeness()
print(f"Missing files: {len(missing)}")
for url in missing:
    print(f"  - {url}")
```

### Problem: Download stops unexpectedly

**Possible Causes:**
1. **Rate limiting**: Server is blocking requests due to high frequency
2. **Memory issues**: Large websites consuming too much memory
3. **Network timeouts**: Slow or unstable connection

**Solutions:**
```python
# Increase delay between requests
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    delay=3.0  # 3 seconds between requests
)

# Reduce concurrent workers
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    max_workers=2  # Reduce from default 5
)

# Use custom user agent
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    user_agent="Mozilla/5.0 (compatible; MyBot/1.0)"
)
```

## Performance Issues

### Problem: Downloads are very slow

**Solutions:**
```python
# Increase concurrent workers (advanced downloader only)
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    max_workers=10  # Increase from default 5
)

# Reduce delay between requests (be respectful)
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    delay=0.5  # Reduce from default 1.0
)

# Disable SSL verification if not needed
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    verify_ssl=False
)
```

### Problem: High memory usage

**Solutions:**
```python
# Limit download depth
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    max_depth=2  # Reduce from default 3
)

# Reduce concurrent workers
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    max_workers=2
)
```

## SSL/TLS Issues

### Problem: SSL certificate verification failed

**Error:**
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Solutions:**
```python
# Disable SSL verification (not recommended for production)
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    verify_ssl=False
)

# Or update certificates
# On macOS: /Applications/Python\ 3.x/Install\ Certificates.command
# On Linux: sudo apt-get update && sudo apt-get install ca-certificates
```

### Problem: Mixed content (HTTP/HTTPS)

**Solution:**
```python
# The downloader automatically handles protocol differences
# No special configuration needed
```

## File System Issues

### Problem: Permission denied when creating files

**Error:**
```
PermissionError: [Errno 13] Permission denied: './downloaded_site/index.html'
```

**Solutions:**
```bash
# Ensure output directory is writable
chmod 755 ./downloaded_site

# Or use a different output directory
```

```python
# Use absolute path
import os
output_dir = os.path.expanduser("~/Downloads/website")
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir=output_dir
)
```

### Problem: Filename too long

**Error:**
```
OSError: [Errno 36] File name too long
```

**Solution:**
The downloader automatically truncates long filenames, but you can customize this behavior by modifying the `url_to_filepath` method.

### Problem: Invalid characters in filenames

**Solution:**
The downloader automatically sanitizes filenames, replacing invalid characters with underscores.

## Network Issues

### Problem: Connection timeouts

**Error:**
```
ConnectTimeout: HTTPSConnectionPool(host='example.com', port=443): Read timed out.
```

**Solution:**
```python
# Increase timeout (modify session configuration)
import requests

downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site"
)

# Customize session timeout
downloader.session.timeout = 30  # 30 seconds
```

### Problem: DNS resolution failures

**Error:**
```
ConnectionError: Failed to establish a new connection: [Errno -2] Name or service not known
```

**Solutions:**
1. Check internet connectivity
2. Verify the URL is correct
3. Try accessing the website in a browser first
4. Check if the website is temporarily down

### Problem: Rate limiting (429 errors)

**Error:**
```
HTTPError: 429 Client Error: Too Many Requests
```

**Solution:**
```python
# Increase delay between requests
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    delay=5.0  # 5 seconds between requests
)

# Reduce concurrent workers
downloader = AdvancedWebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site",
    max_workers=1  # Sequential downloads
)
```

## Configuration Problems

### Problem: Configuration file not found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'config.json'
```

**Solution:**
```python
# Check if config file exists
import os
config_path = "config.json"
if not os.path.exists(config_path):
    print(f"Config file not found: {config_path}")
    # Use default configuration or create config file

# Or use absolute path
config_path = os.path.abspath("config.json")
```

### Problem: Invalid JSON in configuration

**Error:**
```
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 5 column 3
```

**Solution:**
1. Validate JSON syntax using an online JSON validator
2. Check for missing commas, quotes, or brackets
3. Use the provided `config_example.json` as a template

## Common Error Messages

### `requests.exceptions.ConnectionError`

**Cause:** Network connectivity issues

**Solutions:**
- Check internet connection
- Verify the URL is accessible
- Try again later if the server is temporarily down

### `requests.exceptions.HTTPError: 403 Forbidden`

**Cause:** Server is blocking the request

**Solutions:**
- Check robots.txt compliance
- Use a different user agent
- Respect the website's terms of service

### `requests.exceptions.HTTPError: 404 Not Found`

**Cause:** The requested URL doesn't exist

**Solutions:**
- Verify the URL is correct
- Check if the page has moved
- This is normal for some broken links

### `UnicodeDecodeError`

**Cause:** Character encoding issues

**Solution:**
The downloader handles most encoding issues automatically, but you can force UTF-8 encoding if needed.

### `MemoryError`

**Cause:** Insufficient memory for large downloads

**Solutions:**
- Reduce `max_depth`
- Reduce `max_workers`
- Download smaller sections of the website

## Debugging Tips

### Enable Detailed Logging

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Run your downloader
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site"
)
downloader.download_website()
```

### Check Download Statistics

```python
# After download, check statistics
print(f"Downloaded files: {len(downloader.downloaded_files)}")
print(f"Failed downloads: {len(downloader.failed_downloads)}")
print(f"Total size: {downloader.total_size} bytes")

# List failed downloads
for url in downloader.failed_downloads:
    print(f"Failed: {url}")
```

### Test with Simple Websites

```python
# Test with a simple, known-working website
downloader = WebsiteDownloader(
    base_url="https://httpbin.org",
    output_dir="./test_download",
    max_depth=1
)
downloader.download_website()
```

### Verify Network Connectivity

```python
import requests

# Test basic connectivity
try:
    response = requests.get("https://httpbin.org/get", timeout=10)
    print(f"Network test successful: {response.status_code}")
except Exception as e:
    print(f"Network test failed: {e}")
```

### Check Robots.txt

```python
# Manually check robots.txt
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site"
)

# Check specific URLs
test_urls = [
    "https://example.com/",
    "https://example.com/page.html",
    "https://example.com/admin/"
]

for url in test_urls:
    can_fetch = downloader.can_fetch(url)
    print(f"{url}: {'✓' if can_fetch else '✗'}")
```

### Monitor Resource Usage

```python
import psutil
import time

# Monitor memory usage during download
process = psutil.Process()
start_memory = process.memory_info().rss / 1024 / 1024  # MB

downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./downloaded_site"
)

start_time = time.time()
downloader.download_website()
end_time = time.time()

end_memory = process.memory_info().rss / 1024 / 1024  # MB

print(f"Download time: {end_time - start_time:.2f} seconds")
print(f"Memory usage: {end_memory - start_memory:.2f} MB")
```

## Getting Help

If you're still experiencing issues:

1. **Check the logs**: Enable debug logging to see detailed error messages
2. **Search existing issues**: Look for similar problems in the project's issue tracker
3. **Create a minimal example**: Reproduce the issue with the simplest possible code
4. **Provide details**: Include error messages, Python version, OS, and website URL (if public)
5. **Test with different websites**: Verify if the issue is website-specific

### Information to Include in Bug Reports

- Python version (`python --version`)
- Operating system
- Package versions (`pip list | grep -E "requests|beautifulsoup4|lxml"`)
- Complete error message and stack trace
- Minimal code to reproduce the issue
- Website URL (if public and relevant)
- Configuration file (if used)

### Performance Optimization Checklist

- [ ] Appropriate `delay` setting for the target website
- [ ] Optimal `max_workers` for your system and network
- [ ] Reasonable `max_depth` to avoid downloading too much
- [ ] SSL verification disabled only if necessary
- [ ] Robots.txt compliance enabled unless specifically needed
- [ ] Sufficient disk space for downloaded files
- [ ] Stable network connection
- [ ] Updated dependencies

Remember to always respect website terms of service and robots.txt files when downloading content.