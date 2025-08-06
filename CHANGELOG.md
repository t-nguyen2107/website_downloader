# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Smart URL filtering to skip non-downloadable schemes (mailto:, tel:, javascript:, data:, ftp:, file:)
- Comprehensive project configuration with pyproject.toml
- Code quality tools setup (Black, isort, Flake8, MyPy, Pylint)
- Pre-commit hooks for automated code quality checks
- Contributing guidelines and development setup documentation
- Enhanced .gitignore with comprehensive exclusions
- Project structure improvements for better maintainability

### Changed
- Updated README.md with Smart URL Filtering feature documentation
- Improved "How It Works" section with detailed URL discovery and filtering steps

### Fixed
- URL extraction now properly filters out non-HTTP/HTTPS schemes
- Both basic and advanced downloaders handle invalid URL schemes gracefully

## [1.0.0] - Initial Release

### Added
- Basic website downloader (`website_downloader.py`)
  - Single-threaded downloading
  - Robots.txt compliance
  - Internal URL detection
  - HTML and CSS asset extraction
  - Configurable download depth
  - Download reports and statistics

- Advanced website downloader (`advanced_downloader.py`)
  - Multi-threaded downloading for improved performance
  - Enhanced asset type detection
  - Error recovery mechanisms
  - URL aliasing support
  - Completeness verification
  - Configuration file support
  - Progress tracking

- Quick start script (`quick_start.py`)
  - Dependency checking
  - Basic usage examples
  - User onboarding

- Demo script (`demo.py`)
  - Comprehensive demonstration
  - Multiple website examples
  - Feature showcasing

- Configuration support
  - JSON configuration files
  - Example configuration (`config_example.json`)
  - Flexible parameter settings

- Documentation
  - Comprehensive README.md
  - Feature descriptions
  - Usage examples
  - Installation instructions
  - Troubleshooting guide

### Features

#### Core Functionality
- **Recursive Website Downloading**: Download entire websites with configurable depth
- **Asset Preservation**: Download and link HTML, CSS, JavaScript, images, and other assets
- **Robots.txt Compliance**: Respect website robots.txt files
- **Internal URL Detection**: Automatically identify and download internal links
- **URL Normalization**: Handle relative and absolute URLs correctly
- **File Organization**: Maintain website structure in local filesystem

#### Advanced Features
- **Multi-threading**: Parallel downloads for improved performance
- **Error Recovery**: Retry failed downloads with exponential backoff
- **Progress Tracking**: Real-time download progress and statistics
- **Completeness Verification**: Ensure all assets are properly downloaded
- **URL Aliasing**: Handle URL redirects and aliases
- **Configurable Delays**: Respect server load with configurable delays
- **SSL Verification**: Optional SSL certificate verification
- **Custom User Agents**: Configurable user agent strings

#### Quality of Life
- **Detailed Logging**: Comprehensive logging with multiple levels
- **Download Reports**: Generate detailed download statistics
- **Force Redownload**: Option to redownload existing files
- **Subdomain Handling**: Include or exclude subdomains
- **File Type Detection**: Smart detection of HTML and other file types
- **Path Sanitization**: Safe filename generation for cross-platform compatibility

### Dependencies
- requests >= 2.25.0
- beautifulsoup4 >= 4.9.0
- lxml >= 4.6.0
- selenium (optional, for JavaScript-heavy sites)
- aiohttp (optional, for async operations)
- tqdm (optional, for progress bars)

### Supported Python Versions
- Python 3.7+
- Tested on Windows, macOS, and Linux

### Known Limitations
- Limited JavaScript support (requires Selenium for JS-heavy sites)
- No support for authentication-protected content
- Single-session downloads (no resume capability)
- Memory usage scales with website size

---

## Version History Notes

### Versioning Strategy
This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

### Release Process
1. Update version in `pyproject.toml`
2. Update this CHANGELOG.md
3. Create git tag with version number
4. Create GitHub release with release notes

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.