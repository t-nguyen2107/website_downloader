#!/usr/bin/env python3
"""
Demo script for Website Downloader

This script demonstrates how to use the website downloader with a simple example.
It downloads a small test website to show the functionality.
"""

import os
import sys
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from website_downloader import WebsiteDownloader


def demo_basic_downloader():
    """Demonstrate basic website downloader"""
    print("=== Basic Website Downloader Demo ===")
    print()
    
    # Example with a simple, publicly available website
    test_url = "https://httpbin.org"  # Simple HTTP testing service
    output_dir = "demo_basic_download"
    
    print(f"Downloading: {test_url}")
    print(f"Output directory: {output_dir}")
    print()
    
    try:
        downloader = WebsiteDownloader(
            base_url=test_url,
            output_dir=output_dir,
            delay=0.5,  # Faster for demo
            max_depth=2  # Limited depth for demo
        )
        
        downloader.download_website()
        downloader.generate_report()
        
        print(f"\n✓ Basic download completed!")
        print(f"Check the '{output_dir}' directory for downloaded files.")
        
    except Exception as e:
        print(f"Error in basic demo: {e}")


def demo_advanced_downloader():
    """Demonstrate advanced website downloader"""
    print("\n=== Advanced Website Downloader Demo ===")
    print()
    
    try:
        from advanced_downloader import AdvancedWebsiteDownloader, load_config
        
        # Example with a simple website
        test_url = "https://httpbin.org"
        output_dir = "demo_advanced_download"
        
        print(f"Downloading: {test_url}")
        print(f"Output directory: {output_dir}")
        print()
        
        # Load configuration
        config = load_config(
            base_url=test_url,
            output_dir=output_dir,
            delay=0.5,
            max_depth=2,
            max_workers=2,  # Use threading for demo
            verify_ssl=True
        )
        
        downloader = AdvancedWebsiteDownloader(config)
        downloader.download_website()
        
        # Verify completeness
        is_complete = downloader.verify_completeness()
        if is_complete:
            print("\n✓ Download verification passed!")
        else:
            print("\n⚠ Download verification found some issues.")
            
        downloader.generate_advanced_report()
        
        print(f"\n✓ Advanced download completed!")
        print(f"Check the '{output_dir}' directory for downloaded files.")
        
    except ImportError:
        print("Advanced downloader requires additional dependencies.")
        print("Make sure you have installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error in advanced demo: {e}")


def show_usage_examples():
    """Show usage examples"""
    print("\n=== Usage Examples ===")
    print()
    
    examples = [
        {
            "title": "Basic Usage",
            "command": "python website_downloader.py https://example.com",
            "description": "Download a website with default settings"
        },
        {
            "title": "Custom Output Directory",
            "command": "python website_downloader.py https://example.com --output ./my_site",
            "description": "Specify a custom output directory"
        },
        {
            "title": "Respectful Crawling",
            "command": "python website_downloader.py https://example.com --delay 2.0",
            "description": "Add 2-second delay between requests"
        },
        {
            "title": "Limited Depth",
            "command": "python website_downloader.py https://example.com --max-depth 3",
            "description": "Limit crawling to 3 levels deep"
        },
        {
            "title": "Advanced with Threading",
            "command": "python advanced_downloader.py https://example.com --workers 4",
            "description": "Use 4 worker threads for faster downloading"
        },
        {
            "title": "With Configuration File",
            "command": "python advanced_downloader.py https://example.com --config config_example.json",
            "description": "Use a configuration file for settings"
        },
        {
            "title": "Verify Completeness",
            "command": "python advanced_downloader.py https://example.com --verify-completeness",
            "description": "Check for missing files and broken links after download"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['title']}")
        print(f"   Command: {example['command']}")
        print(f"   Description: {example['description']}")
        print()


def show_important_notes():
    """Show important usage notes"""
    print("=== Important Notes ===")
    print()
    
    notes = [
        "🚨 Legal Compliance: Always respect website terms of service and copyright laws",
        "🤖 Robots.txt: The downloader checks and respects robots.txt files",
        "⏱️ Rate Limiting: Use appropriate delays to avoid overwhelming servers",
        "🔒 SSL: HTTPS sites are supported with SSL verification",
        "📱 Dynamic Content: JavaScript-heavy sites may not be fully captured",
        "🔗 Link Conversion: Internal links are converted for offline browsing",
        "📊 Reporting: Detailed logs and reports are generated for each download",
        "🧵 Threading: Advanced version supports multi-threaded downloading",
        "✅ Verification: Advanced version can verify download completeness"
    ]
    
    for note in notes:
        print(f"  {note}")
    print()


def main():
    """Main demo function"""
    print("Website Downloader Demo")
    print("=======================")
    print()
    print("This demo shows how to use the website downloader tools.")
    print("The demo uses httpbin.org as a test site (safe for testing).")
    print()
    
    # Show important notes first
    show_important_notes()
    
    # Ask user what they want to do
    while True:
        print("What would you like to do?")
        print("1. Run basic downloader demo")
        print("2. Run advanced downloader demo")
        print("3. Show usage examples")
        print("4. Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            demo_basic_downloader()
        elif choice == '2':
            demo_advanced_downloader()
        elif choice == '3':
            show_usage_examples()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            
        print("\n" + "="*50 + "\n")


if __name__ == '__main__':
    main()