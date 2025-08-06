# 🌐 Website Downloader

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/t-nguyen2107/website-downloader.svg)](https://github.com/t-nguyen2107/website-downloader/issues)
[![GitHub Stars](https://img.shields.io/github/stars/t-nguyen2107/website-downloader.svg)](https://github.com/t-nguyen2107/website-downloader/stargazers)

A comprehensive Python tool for downloading entire websites for offline browsing. This tool recursively crawls websites, downloads all pages and assets (HTML, CSS, JS, images), and converts internal links for seamless offline navigation.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Command Line Options](#-command-line-options)
- [How It Works](#-how-it-works)
- [Output Structure](#-output-structure)
- [Important Considerations](#-important-considerations)
- [Troubleshooting](#-troubleshooting)
- [Alternative Solutions](#-alternative-solutions)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Recursive Crawling**: Automatically discovers and downloads all internal pages
- **Asset Collection**: Downloads images, CSS, JavaScript, fonts, and other assets
- **Link Conversion**: Converts absolute links to relative paths for offline browsing
- **Smart URL Filtering**: Automatically skips non-downloadable URLs (mailto:, tel:, javascript:, etc.)
- **Respectful Crawling**: Respects robots.txt and includes configurable delays
- **Progress Tracking**: Comprehensive logging and progress reporting
- **Resume Capability**: Skips already downloaded files
- **Error Handling**: Tracks and reports failed downloads
- **Depth Control**: Configurable maximum crawling depth
- **Multi-threading**: Advanced downloader supports concurrent downloads
- **Configuration Files**: JSON-based configuration for advanced settings
- **Completeness Verification**: Verify download integrity after completion

## 🚀 Installation

1. **Clone or download this repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 📦 Dependencies

- `requests` - HTTP library for downloading files
- `beautifulsoup4` - HTML parsing and manipulation
- `lxml` - Fast XML and HTML parser

## 🔧 Quick Start

Get started quickly with our test script:

```bash
python quick_start.py
```

This will guide you through testing both downloaders with a safe example website.

## 🎬 Demo

```bash
# Quick test with httpbin.org (safe test site)
python quick_start.py

# Download a simple website
python website_downloader.py https://httpbin.org --output test_site

# Advanced download with multi-threading
python advanced_downloader.py https://httpbin.org --workers 4 --verify-completeness
```

> **Note**: Always test with small, safe websites first before attempting larger downloads.

## 📖 Usage

### Basic Downloader

```bash
# Basic usage
python website_downloader.py https://example.com

# With options
python website_downloader.py https://example.com --output ./my_website --delay 2.0 --max-depth 5
```

### Advanced Downloader

```bash
# Basic usage
python advanced_downloader.py https://example.com

# With multi-threading and verification
python advanced_downloader.py https://example.com --workers 4 --verify-completeness

# Using configuration file
python advanced_downloader.py https://example.com --config config.json
```

## ⚙️ Configuration

### Configuration File (Advanced)

Create a JSON configuration file for advanced settings:

```json
{
    "delay": 1.0,
    "max_depth": 10,
    "max_workers": 4,
    "verify_ssl": true,
    "include_subdomains": false,
    "force_redownload": false,
    "ignore_robots": false,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

> 💡 **Tip**: Use `config_example.json` as a starting template for your configuration.

⚠️ **WARNING**: Setting `"ignore_robots": true` in configuration files carries the same legal risks as the `--ignore-robots` command-line flag. See warnings below.

### 📝 Example Commands

```bash
# Basic download
python website_downloader.py https://example.com

# Respectful crawling with delays
python website_downloader.py https://example.com --delay 2.0 --max-depth 3

# Advanced multi-threaded download
python advanced_downloader.py https://example.com --workers 4 --verify-completeness

# Using configuration file
python advanced_downloader.py https://example.com --config my_config.json

# Include subdomains (use with caution)
python advanced_downloader.py https://example.com --include-subdomains --delay 3.0
```

## 🛠️ Command Line Options

#### Basic Downloader (`website_downloader.py`)
- `url` - Base URL of the website to download (required)
- `--output`, `-o` - Output directory (default: `downloaded_site`)
- `--delay`, `-d` - Delay between requests in seconds (default: 1.0)
- `--max-depth`, `-m` - Maximum crawling depth (default: 10)
- `--ignore-robots` - **⚠️ CAUTION**: Ignore robots.txt restrictions (see warnings below)

#### Advanced Downloader (`advanced_downloader.py`)
- `url` - Base URL of the website to download (required)
- `--output`, `-o` - Output directory (default: `downloaded_site`)
- `--config`, `-c` - Configuration file (JSON)
- `--delay`, `-d` - Delay between requests in seconds (default: 1.0)
- `--max-depth`, `-m` - Maximum crawling depth (default: 10)
- `--workers`, `-w` - Number of worker threads (default: 1)
- `--verify-completeness` - Verify download completeness after completion
- `--include-subdomains` - Include subdomains in download
- `--force-redownload` - Force re-download of existing files
- `--no-ssl-verify` - Disable SSL certificate verification
- `--ignore-robots` - **⚠️ CAUTION**: Ignore robots.txt restrictions (see warnings below)

## 🔄 How It Works

1. **Initial Setup**: Creates output directory and checks robots.txt
2. **URL Discovery**: Extracts links from HTML content and CSS files
3. **Smart Filtering**: Automatically filters out non-downloadable URLs:
   - `mailto:` (email links)
   - `tel:` (telephone links) 
   - `javascript:` (JavaScript code)
   - `data:` (inline data)
   - `ftp:`, `file:` (non-HTTP protocols)
4. **Recursive Crawling**: Starts from the base URL and discovers internal links
5. **Asset Download**: Downloads HTML pages, images, CSS, JavaScript, and other assets
6. **Link Conversion**: Modifies HTML files to use relative paths for offline browsing
7. **Progress Tracking**: Logs all activities and generates a final report

## 📁 Output Structure

The downloaded website maintains the original directory structure:

```
downloaded_site/
├── index.html              # Main page
├── about/
│   └── index.html         # About page
├── css/
│   └── style.css          # Stylesheets
├── js/
│   └── script.js          # JavaScript files
├── images/
│   ├── logo.png           # Images
│   └── banner.jpg
├── download.log           # Download log
└── download_report.txt    # Summary report
```

## ⚠️ Important Considerations

### 📜 Legal and Ethical Usage

⚠️ **IMPORTANT**: Always respect website terms of service and copyright laws:

- Check the website's `robots.txt` and terms of service
- Only download content you have permission to access
- Respect copyright and intellectual property rights
- Use appropriate delays to avoid overwhelming servers
- Consider contacting website owners for permission

#### 🚨 CRITICAL WARNING: --ignore-robots Option

**The `--ignore-robots` flag is potentially ILLEGAL and UNETHICAL to use without proper authorization.**

**LEGAL RISKS**:
- Violating robots.txt may constitute unauthorized access under computer crime laws
- Could violate terms of service agreements
- May result in legal action, fines, or criminal charges
- Could be considered trespassing on digital property

**WHEN IT MIGHT BE ACCEPTABLE**:
- You own the website
- You have explicit written permission from the website owner
- You are authorized by your organization to access the content
- The content is in the public domain with no access restrictions

**BEFORE USING --ignore-robots, YOU MUST**:
1. Verify you have legal authorization to access the content
2. Check the website's terms of service
3. Consider the ethical implications
4. Understand the potential legal consequences
5. Consult with legal counsel if uncertain

**USE AT YOUR OWN RISK**: The authors of this tool are not responsible for any legal consequences resulting from misuse of the `--ignore-robots` option.

### 🔧 Technical Limitations

- **Dynamic Content**: Single Page Applications (SPAs) and JavaScript-heavy sites may not be fully captured
- **Lazy Loading**: Content loaded dynamically may be missed
- **Authentication**: Password-protected areas cannot be accessed
- **Interactive Features**: Forms, search, and dynamic functionality won't work offline
- **External Resources**: Only internal links are converted; external resources remain as absolute URLs

### 💡 Best Practices

1. **Respect robots.txt**: Never use `--ignore-robots` without proper authorization
2. **Start Small**: Test with a small section of the website first
3. **Use Delays**: Always use appropriate delays (1-2 seconds) between requests
4. **Monitor Progress**: Check the log files for any issues
5. **Verify Results**: Test the offline site thoroughly before relying on it
6. **Regular Updates**: Re-download periodically if the source website changes
7. **Legal Compliance**: Always ensure you have permission to download content

## 🔍 Troubleshooting

### 🐛 Common Issues

**403 Forbidden Errors**:
- The website may be blocking automated requests
- Try increasing the delay between requests
- Check if the site requires authentication

**Missing Assets**:
- Some assets may be loaded dynamically via JavaScript
- Check the download log for failed URLs
- Consider using browser developer tools to identify missing resources

**Broken Links**:
- Some internal links may not be converted properly
- Check the download report for failed downloads
- Manually verify critical navigation paths

### 📄 Log Files

- `download.log` - Detailed download activity
- `download_report.txt` - Summary of successful and failed downloads

## 🔗 Alternative Solutions

For comparison, here are other popular website downloading tools:

### 🖥️ Command Line Tools
- **wget**: `wget --recursive --page-requisites --html-extension --convert-links --domains example.com https://example.com`
- **HTTrack**: GUI and command-line website copier

### 🐍 Python Libraries
- **scrapy**: More advanced web scraping framework
- **pywebcopy**: Another Python website copying library

### 📚 GitHub Projects
- **PKHarsimran/website-downloader**: Robust website downloader with similar features
- **internetarchive/wayback**: Internet Archive's wayback machine tools

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### 🎯 Areas for Improvement
- [ ] Support for more asset types (WebP, AVIF, etc.)
- [ ] Better JavaScript-heavy site handling
- [ ] Enhanced error recovery mechanisms
- [ ] Unit tests and CI/CD pipeline
- [ ] Docker containerization
- [ ] GUI interface

### 🔧 Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/t-nguyen2107/website-downloader.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Test your changes: `python quick_start.py`
5. Submit a pull request

### 📋 Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test with multiple websites
- Update documentation as needed

## 📊 Project Stats

- **Languages**: Python 3.7+
- **Dependencies**: requests, beautifulsoup4, lxml
- **Features**: 15+ core features
- **License**: MIT

## 🙏 Acknowledgments

- Inspired by [PKHarsimran/website-downloader](https://github.com/PKHarsimran/website-downloader)
- Built with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) and [Requests](https://docs.python-requests.org/)
- Thanks to all contributors and testers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This tool is for educational and personal use only. Users are responsible for ensuring their use complies with applicable laws, website terms of service, and copyright regulations. The authors are not responsible for any misuse of this tool.

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[Report Bug](https://github.com/t-nguyen2107/website-downloader/issues) • [Request Feature](https://github.com/t-nguyen2107/website-downloader/issues) • [Contribute](https://github.com/t-nguyen2107/website-downloader/pulls)

</div>