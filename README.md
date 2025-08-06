# Website Downloader

A comprehensive Python tool for downloading entire websites for offline browsing. This tool recursively crawls websites, downloads all pages and assets (HTML, CSS, JS, images), and converts internal links for seamless offline navigation.

## Features

- **Recursive Crawling**: Automatically discovers and downloads all internal pages
- **Asset Collection**: Downloads images, CSS, JavaScript, fonts, and other assets
- **Link Conversion**: Converts absolute links to relative paths for offline browsing
- **Respectful Crawling**: Respects robots.txt and includes configurable delays
- **Progress Tracking**: Comprehensive logging and progress reporting
- **Resume Capability**: Skips already downloaded files
- **Error Handling**: Tracks and reports failed downloads
- **Depth Control**: Configurable maximum crawling depth

## Installation

1. **Clone or download this repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

- `requests` - HTTP library for downloading files
- `beautifulsoup4` - HTML parsing and manipulation
- `lxml` - Fast XML and HTML parser

## Usage

### Basic Usage

```bash
python website_downloader.py https://example.com
```

### Advanced Usage

```bash
# Specify output directory
python website_downloader.py https://example.com --output ./my_website

# Add delay between requests (respectful crawling)
python website_downloader.py https://example.com --delay 2.0

# Limit crawling depth
python website_downloader.py https://example.com --max-depth 5

# Combine options
python website_downloader.py https://example.com --output ./docs --delay 1.5 --max-depth 3
```

### Command Line Options

- `url` - Base URL of the website to download (required)
- `--output`, `-o` - Output directory (default: `downloaded_site`)
- `--delay`, `-d` - Delay between requests in seconds (default: 1.0)
- `--max-depth`, `-m` - Maximum crawling depth (default: 10)

## How It Works

1. **Initial Setup**: Creates output directory and checks robots.txt
2. **Recursive Crawling**: Starts from the base URL and discovers internal links
3. **Asset Download**: Downloads HTML pages, images, CSS, JavaScript, and other assets
4. **Link Conversion**: Modifies HTML files to use relative paths for offline browsing
5. **Progress Tracking**: Logs all activities and generates a final report

## Output Structure

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

## Important Considerations

### Legal and Ethical Usage

⚠️ **IMPORTANT**: Always respect website terms of service and copyright laws:

- Check the website's `robots.txt` and terms of service
- Only download content you have permission to access
- Respect copyright and intellectual property rights
- Use appropriate delays to avoid overwhelming servers
- Consider contacting website owners for permission

### Technical Limitations

- **Dynamic Content**: Single Page Applications (SPAs) and JavaScript-heavy sites may not be fully captured
- **Lazy Loading**: Content loaded dynamically may be missed
- **Authentication**: Password-protected areas cannot be accessed
- **Interactive Features**: Forms, search, and dynamic functionality won't work offline
- **External Resources**: Only internal links are converted; external resources remain as absolute URLs

### Best Practices

1. **Start Small**: Test with a small section of the website first
2. **Use Delays**: Always use appropriate delays (1-2 seconds) between requests
3. **Monitor Progress**: Check the log files for any issues
4. **Verify Results**: Test the offline site thoroughly before relying on it
5. **Regular Updates**: Re-download periodically if the source website changes

## Troubleshooting

### Common Issues

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

### Log Files

- `download.log` - Detailed download activity
- `download_report.txt` - Summary of successful and failed downloads

## Alternative Solutions

For comparison, here are other popular website downloading tools:

### Command Line Tools
- **wget**: `wget --recursive --page-requisites --html-extension --convert-links --domains example.com https://example.com`
- **HTTrack**: GUI and command-line website copier

### Python Libraries
- **scrapy**: More advanced web scraping framework
- **pywebcopy**: Another Python website copying library

### GitHub Projects
- **PKHarsimran/website-downloader**: Robust website downloader with similar features
- **internetarchive/wayback**: Internet Archive's wayback machine tools

## Contributing

Contributions are welcome! Please consider:

- Adding support for more asset types
- Improving JavaScript-heavy site handling
- Adding configuration file support
- Enhancing error recovery
- Adding unit tests

## License

This project is provided as-is for educational and personal use. Please ensure you comply with all applicable laws and website terms of service when using this tool.

## Disclaimer

This tool is for educational and personal use only. Users are responsible for ensuring their use complies with applicable laws, website terms of service, and copyright regulations. The authors are not responsible for any misuse of this tool.