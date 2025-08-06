# Contributing to Website Downloader

Thank you for your interest in contributing to Website Downloader! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style and Standards](#code-style-and-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)
- [Areas for Contribution](#areas-for-contribution)

## 🤝 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone has different skill levels
- **Be professional**: Keep discussions focused and on-topic

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic understanding of web scraping concepts
- Familiarity with Python libraries: requests, BeautifulSoup, lxml

### First-time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/website-downloader.git
   cd website-downloader
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/website-downloader.git
   ```

## 🛠️ Development Setup

### Environment Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   # Core dependencies
   pip install -r requirements.txt
   
   # Development dependencies
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Verify Installation

```bash
# Test the basic downloader
python quick_start.py

# Run code quality checks
pre-commit run --all-files
```

## 📝 Code Style and Standards

### Code Formatting

We use several tools to maintain code quality:

- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting
- **Flake8**: Linting and style checking
- **MyPy**: Type checking (optional but encouraged)
- **Pylint**: Additional code analysis

### Running Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Check linting
flake8 .

# Type checking
mypy website_downloader.py advanced_downloader.py

# Run all pre-commit hooks
pre-commit run --all-files
```

### Code Standards

1. **Docstrings**: Use Google-style docstrings for all public functions and classes
2. **Type Hints**: Add type hints where possible (Python 3.7+ compatible)
3. **Error Handling**: Include proper exception handling with informative messages
4. **Logging**: Use the logging module instead of print statements
5. **Constants**: Use UPPER_CASE for constants
6. **Variable Names**: Use descriptive, snake_case variable names

### Example Code Style

```python
def download_file(self, url: str, filepath: Path) -> bool:
    """Download a file from URL to local filepath.
    
    Args:
        url: The URL to download from
        filepath: Local path where file should be saved
        
    Returns:
        True if download successful, False otherwise
        
    Raises:
        requests.RequestException: If download fails
    """
    try:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.content)
        
        self.logger.info(f"Downloaded: {url} -> {filepath}")
        return True
        
    except requests.RequestException as e:
        self.logger.error(f"Failed to download {url}: {e}")
        return False
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_downloader.py

# Run tests with specific markers
pytest -m "not slow"
```

### Writing Tests

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test complete workflows
3. **Mock External Calls**: Use `unittest.mock` for HTTP requests
4. **Test Edge Cases**: Include error conditions and edge cases

### Test Structure

```
tests/
├── __init__.py
├── test_website_downloader.py
├── test_advanced_downloader.py
├── test_utils.py
├── fixtures/
│   ├── sample.html
│   └── sample.css
└── conftest.py
```

## 📤 Submitting Changes

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following the code standards

4. **Test your changes**:
   ```bash
   # Run tests
   pytest
   
   # Run code quality checks
   pre-commit run --all-files
   
   # Test with real websites (use safe test sites)
   python quick_start.py
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Format

Use conventional commit format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add support for JavaScript-heavy websites
fix: handle SSL certificate errors gracefully
docs: update installation instructions
refactor: improve URL validation logic
```

## 🐛 Issue Guidelines

### Reporting Bugs

When reporting bugs, include:

1. **Environment**: Python version, OS, dependencies
2. **Steps to reproduce**: Exact commands and URLs used
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Error messages**: Full error output and logs
6. **Sample code**: Minimal code to reproduce the issue

### Feature Requests

For feature requests, include:

1. **Use case**: Why is this feature needed?
2. **Proposed solution**: How should it work?
3. **Alternatives**: Other ways to achieve the same goal
4. **Implementation ideas**: Technical approach (if known)

## 🔄 Pull Request Process

1. **Create a pull request** from your feature branch
2. **Fill out the PR template** with all required information
3. **Ensure all checks pass**: Tests, linting, and code coverage
4. **Request review** from maintainers
5. **Address feedback** promptly and professionally
6. **Keep PR updated** with main branch if needed

### PR Requirements

- [ ] All tests pass
- [ ] Code coverage maintained or improved
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] No merge conflicts with main branch
- [ ] Pre-commit hooks pass

## 📁 Project Structure

```
website-downloader/
├── website_downloader.py      # Basic downloader
├── advanced_downloader.py     # Advanced downloader with threading
├── quick_start.py            # User onboarding script
├── demo.py                   # Demo script
├── requirements.txt          # Core dependencies
├── pyproject.toml           # Project configuration
├── setup.cfg                # Tool configurations
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── CONTRIBUTING.md         # This file
├── CHANGELOG.md            # Version history
├── LICENSE                 # License file
├── config_example.json     # Configuration example
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_*.py
│   └── fixtures/
└── docs/                   # Additional documentation
    ├── api.md
    ├── examples.md
    └── troubleshooting.md
```

## 🎯 Areas for Contribution

### High Priority

1. **Test Coverage**: Improve test coverage, especially for edge cases
2. **Error Handling**: Better error recovery and user feedback
3. **Performance**: Optimize download speed and memory usage
4. **Documentation**: API documentation and usage examples

### Medium Priority

1. **JavaScript Support**: Handle JavaScript-heavy websites
2. **Async Downloads**: Implement async/await for better performance
3. **Progress Bars**: Visual progress indicators
4. **Configuration**: More flexible configuration options

### Low Priority

1. **GUI Interface**: Desktop application interface
2. **Plugin System**: Extensible plugin architecture
3. **Cloud Storage**: Support for cloud storage backends
4. **Database Support**: Store metadata in databases

### Good First Issues

- Fix typos in documentation
- Add more test cases
- Improve error messages
- Add configuration validation
- Enhance logging output

## 📚 Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## 💬 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: Ask for feedback on your changes

## 🙏 Recognition

All contributors will be recognized in:

- README.md contributors section
- CHANGELOG.md for significant contributions
- GitHub contributors page

Thank you for contributing to Website Downloader! 🎉