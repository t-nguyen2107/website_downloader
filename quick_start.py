#!/usr/bin/env python3
"""
Quick Start Script for Website Downloader

This script provides a simple way to test the website downloader
with a safe example website.
"""

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        import bs4
        import lxml
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False


def run_basic_example():
    """Run a basic example download"""
    print("\n=== Running Basic Example ===")
    print("Downloading httpbin.org (a safe testing website)...")
    print()
    
    # Run the basic downloader
    cmd = [
        sys.executable, "website_downloader.py",
        "https://httpbin.org",
        "--output", "quick_start_test",
        "--delay", "0.5",
        "--max-depth", "2"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Basic download completed successfully!")
            print(f"Check the 'quick_start_test' directory for downloaded files.")
            print(f"Open 'quick_start_test/index.html' in your browser.")
        else:
            print("❌ Download failed:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ Could not find website_downloader.py")
        print("Make sure you're running this from the correct directory.")
    except Exception as e:
        print(f"❌ Error running download: {e}")


def run_advanced_example():
    """Run an advanced example download"""
    print("\n=== Running Advanced Example ===")
    print("Downloading with advanced features...")
    print()
    
    # Run the advanced downloader
    cmd = [
        sys.executable, "advanced_downloader.py",
        "https://httpbin.org",
        "--output", "quick_start_advanced",
        "--delay", "0.5",
        "--max-depth", "2",
        "--workers", "2",
        "--verify-completeness"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Advanced download completed successfully!")
            print(f"Check the 'quick_start_advanced' directory for downloaded files.")
            print(f"Open 'quick_start_advanced/index.html' in your browser.")
        else:
            print("❌ Advanced download failed:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ Could not find advanced_downloader.py")
        print("Make sure you're running this from the correct directory.")
    except Exception as e:
        print(f"❌ Error running advanced download: {e}")


def show_next_steps():
    """Show what to do next"""
    print("\n=== Next Steps ===")
    print()
    print("Now that you've tested the downloader, here's what you can do:")
    print()
    print("1. Download a real website:")
    print("   python website_downloader.py https://your-target-site.com")
    print()
    print("2. Use advanced features:")
    print("   python advanced_downloader.py https://your-site.com --workers 4 --verify-completeness")
    print()
    print("3. Customize settings:")
    print("   - Edit config_example.json for your preferences")
    print("   - Use --delay to be more respectful to servers")
    print("   - Use --max-depth to limit how deep to crawl")
    print()
    print("4. Important reminders:")
    print("   - Always respect robots.txt and terms of service")
    print("   - Use appropriate delays for respectful crawling")
    print("   - Check copyright and legal requirements")
    print("   - Test with small sites first")
    print()
    print("5. For help:")
    print("   python website_downloader.py --help")
    print("   python advanced_downloader.py --help")
    print()


def main():
    """Main function"""
    print("Website Downloader - Quick Start")
    print("================================")
    print()
    print("This script will test the website downloader with a safe example.")
    print("It downloads httpbin.org, which is designed for testing HTTP tools.")
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check if scripts exist
    if not Path("website_downloader.py").exists():
        print("❌ website_downloader.py not found in current directory")
        return
        
    if not Path("advanced_downloader.py").exists():
        print("⚠️ advanced_downloader.py not found (optional)")
    
    print("\nWhich test would you like to run?")
    print("1. Basic downloader test")
    print("2. Advanced downloader test (if available)")
    print("3. Both tests")
    print("4. Skip tests and show usage examples")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        run_basic_example()
    elif choice == '2':
        if Path("advanced_downloader.py").exists():
            run_advanced_example()
        else:
            print("❌ Advanced downloader not available")
    elif choice == '3':
        run_basic_example()
        if Path("advanced_downloader.py").exists():
            run_advanced_example()
        else:
            print("\n⚠️ Skipping advanced test (file not found)")
    elif choice == '4':
        print("\nSkipping tests...")
    else:
        print("Invalid choice, skipping tests...")
    
    show_next_steps()


if __name__ == '__main__':
    main()