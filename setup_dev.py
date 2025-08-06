#!/usr/bin/env python3
"""
Development Environment Setup Script

This script helps contributors set up their development environment quickly.
It installs dependencies, sets up pre-commit hooks, and runs initial tests.

Usage:
    python setup_dev.py [--skip-tests] [--skip-hooks]
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors gracefully."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        if result.stderr and result.returncode != 0:
            print("Error:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        if e.stdout:
            print("Output:")
            print(e.stdout)
        if e.stderr:
            print("Error:")
            print(e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print(f"Error: Python 3.8+ is required. You have {sys.version}")
        return False
    
    print(f"✓ Python {sys.version} is compatible")
    return True


def check_git():
    """Check if git is available."""
    print("Checking Git availability...")
    
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Git is not available. Please install Git first.")
        return False


def install_dependencies():
    """Install project dependencies."""
    print("\nInstalling dependencies...")
    
    # Upgrade pip first
    success = run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    if not success:
        print("Warning: Failed to upgrade pip, continuing anyway...")
    
    # Install main dependencies
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing main dependencies"
    )
    
    if not success:
        print("Error: Failed to install main dependencies")
        return False
    
    # Install development dependencies
    dev_packages = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=23.0.0",
        "isort>=5.12.0",
        "flake8>=6.0.0",
        "mypy>=1.0.0",
        "pre-commit>=3.0.0",
        "bandit>=1.7.0",
        "pytest-mock>=3.10.0",
        "responses>=0.23.0"
    ]
    
    for package in dev_packages:
        success = run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {package.split('>=')[0]}",
            check=False
        )
        
        if not success:
            print(f"Warning: Failed to install {package}")
    
    print("\n✓ Dependencies installation completed")
    return True


def setup_pre_commit_hooks():
    """Set up pre-commit hooks."""
    print("\nSetting up pre-commit hooks...")
    
    if not Path(".pre-commit-config.yaml").exists():
        print("Warning: .pre-commit-config.yaml not found, skipping pre-commit setup")
        return True
    
    success = run_command(
        "pre-commit install",
        "Installing pre-commit hooks"
    )
    
    if not success:
        print("Warning: Failed to install pre-commit hooks")
        return False
    
    # Run pre-commit on all files to ensure everything works
    success = run_command(
        "pre-commit run --all-files",
        "Running pre-commit on all files",
        check=False  # Don't fail if there are formatting issues
    )
    
    if not success:
        print("Note: Pre-commit found some issues. This is normal for initial setup.")
        print("The issues have been automatically fixed where possible.")
    
    print("✓ Pre-commit hooks setup completed")
    return True


def run_tests():
    """Run the test suite."""
    print("\nRunning tests...")
    
    if not Path("tests").exists():
        print("Warning: tests directory not found, skipping tests")
        return True
    
    # Run tests with coverage
    success = run_command(
        f"{sys.executable} -m pytest tests/ -v --cov=. --cov-report=term-missing",
        "Running test suite with coverage",
        check=False
    )
    
    if success:
        print("✓ All tests passed")
    else:
        print("⚠ Some tests failed. This might be expected for a new setup.")
        print("Please review the test output above.")
    
    return True


def run_code_quality_checks():
    """Run code quality checks."""
    print("\nRunning code quality checks...")
    
    checks = [
        ("black --check .", "Black code formatting check"),
        ("isort --check-only .", "Import sorting check"),
        ("flake8 .", "Flake8 linting"),
        ("mypy .", "MyPy type checking"),
        ("bandit -r . -f json", "Bandit security check")
    ]
    
    all_passed = True
    
    for command, description in checks:
        success = run_command(command, description, check=False)
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n✓ All code quality checks passed")
    else:
        print("\n⚠ Some code quality checks failed.")
        print("Run the individual tools to see detailed output and fix issues.")
    
    return all_passed


def create_sample_config():
    """Create a sample configuration for development."""
    print("\nCreating development configuration...")
    
    dev_config = {
        "delay": 0.1,
        "max_depth": 2,
        "max_workers": 2,
        "verify_ssl": False,
        "include_subdomains": False,
        "force_redownload": False,
        "ignore_robots": True,
        "user_agent": "Website Downloader Development"
    }
    
    import json
    
    config_path = Path("dev_config.json")
    with open(config_path, 'w') as f:
        json.dump(dev_config, f, indent=2)
    
    print(f"✓ Development configuration created: {config_path}")
    return True


def print_next_steps():
    """Print next steps for the developer."""
    print("\n" + "="*60)
    print("🎉 DEVELOPMENT ENVIRONMENT SETUP COMPLETE!")
    print("="*60)
    
    print("\nNext steps:")
    print("1. Read CONTRIBUTING.md for contribution guidelines")
    print("2. Check out the examples in docs/examples.md")
    print("3. Run 'python quick_start.py' to test the basic functionality")
    print("4. Create a new branch for your feature: git checkout -b feature/your-feature")
    print("5. Make your changes and run tests: pytest")
    print("6. Run code quality checks: pre-commit run --all-files")
    print("7. Commit your changes: git commit -m 'Your commit message'")
    
    print("\nUseful commands:")
    print("- Run tests: pytest")
    print("- Run tests with coverage: pytest --cov")
    print("- Format code: black .")
    print("- Sort imports: isort .")
    print("- Lint code: flake8 .")
    print("- Type check: mypy .")
    print("- Security check: bandit -r .")
    print("- Run all pre-commit hooks: pre-commit run --all-files")
    
    print("\nFor help, check:")
    print("- README.md - Project overview")
    print("- CONTRIBUTING.md - Contribution guidelines")
    print("- docs/api.md - API documentation")
    print("- docs/troubleshooting.md - Common issues")
    
    print("\nHappy coding! 🚀")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(
        description="Set up development environment for Website Downloader"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests during setup"
    )
    parser.add_argument(
        "--skip-hooks",
        action="store_true",
        help="Skip setting up pre-commit hooks"
    )
    parser.add_argument(
        "--skip-quality-checks",
        action="store_true",
        help="Skip code quality checks"
    )
    
    args = parser.parse_args()
    
    print("Website Downloader - Development Environment Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_git():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nError: Failed to install dependencies")
        sys.exit(1)
    
    # Set up pre-commit hooks
    if not args.skip_hooks:
        setup_pre_commit_hooks()
    else:
        print("\nSkipping pre-commit hooks setup")
    
    # Create development configuration
    create_sample_config()
    
    # Run tests
    if not args.skip_tests:
        run_tests()
    else:
        print("\nSkipping tests")
    
    # Run code quality checks
    if not args.skip_quality_checks:
        run_code_quality_checks()
    else:
        print("\nSkipping code quality checks")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()