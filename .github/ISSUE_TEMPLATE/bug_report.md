---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
A clear and concise description of what actually happened.

**Screenshots/Logs**
If applicable, add screenshots or log output to help explain your problem.

```
# Paste any relevant log output here
```

**Environment (please complete the following information):**
 - OS: [e.g. Windows 10, Ubuntu 20.04, macOS 12.0]
 - Python version: [e.g. 3.9.7]
 - Website Downloader version: [e.g. 1.0.0]
 - Target website: [e.g. https://example.com]

**Configuration**
If you're using a custom configuration, please share the relevant parts:

```json
{
  "delay": 1.0,
  "max_depth": 3,
  // ... other config options
}
```

**Code snippet**
If applicable, provide a minimal code snippet that reproduces the issue:

```python
from website_downloader import WebsiteDownloader

# Your code here
downloader = WebsiteDownloader(
    base_url="https://example.com",
    output_dir="./test"
)
downloader.download_website()
```

**Additional context**
Add any other context about the problem here.

**Checklist**
- [ ] I have searched existing issues to make sure this is not a duplicate
- [ ] I have provided all the requested information
- [ ] I have tested with the latest version
- [ ] I have included a minimal reproducible example