#!/usr/bin/env python3
"""
Verification script to check if the project is set up correctly.
Run this after installation to verify everything works.
"""
import sys
from pathlib import Path

def check_file(path, description):
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False

def check_directory(path, description):
    if path.exists() and path.is_dir():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False

def main():
    print("=== Project Verification ===\n")
    
    root = Path(__file__).parent
    all_ok = True
    
    # Check directories
    print("Checking directories...")
    all_ok &= check_directory(root / "src", "Source directory")
    all_ok &= check_directory(root / "settings", "Settings directory")
    all_ok &= check_directory(root / "logs", "Logs directory")
    print()
    
    # Check configuration files
    print("Checking configuration files...")
    all_ok &= check_file(root / "config.json", "Configuration file")
    all_ok &= check_file(root / ".env.example", "Environment template")
    all_ok &= check_file(root / "pyproject.toml", "Project configuration")
    print()
    
    # Check source modules
    print("Checking source modules...")
    all_ok &= check_file(root / "src/config.py", "Config module")
    all_ok &= check_file(root / "src/github_client.py", "GitHub client module")
    all_ok &= check_file(root / "src/exporter.py", "Exporter module")
    all_ok &= check_file(root / "src/discovery.py", "Discovery module")
    all_ok &= check_file(root / "src/comparator.py", "Comparator module")
    all_ok &= check_file(root / "src/applier.py", "Applier module")
    all_ok &= check_file(root / "src/logger.py", "Logger module")
    all_ok &= check_file(root / "src/validator.py", "Validator module")
    print()
    
    # Check CLI scripts
    print("Checking CLI scripts...")
    all_ok &= check_file(root / "export.py", "Export command")
    all_ok &= check_file(root / "discover.py", "Discover command")
    all_ok &= check_file(root / "sync.py", "Sync command")
    print()
    
    # Check documentation
    print("Checking documentation...")
    all_ok &= check_file(root / "README.md", "README")
    all_ok &= check_file(root / "QUICKSTART.md", "Quick Start Guide")
    print()
    
    # Check Python imports
    print("Checking Python dependencies...")
    try:
        import github
        print("✓ PyGithub installed")
    except ImportError:
        print("✗ PyGithub not installed (run: uv sync)")
        all_ok = False
    
    try:
        import dotenv
        print("✓ python-dotenv installed")
    except ImportError:
        print("✗ python-dotenv not installed (run: uv sync)")
        all_ok = False
    print()
    
    # Check .env file
    print("Checking environment configuration...")
    env_file = root / ".env"
    if env_file.exists():
        print(f"✓ .env file exists")
        with open(env_file) as f:
            content = f.read()
            if "GITHUB_TOKEN" in content and "your_github_token_here" not in content:
                print("✓ GITHUB_TOKEN appears to be configured")
            else:
                print("⚠ GITHUB_TOKEN may not be configured (check .env file)")
    else:
        print("⚠ .env file not found (copy .env.example to .env and add your token)")
    print()
    
    # Final summary
    print("=" * 50)
    if all_ok:
        print("✓ All checks passed!")
        print("\nNext steps:")
        print("1. Configure your GitHub token in .env file")
        print("2. Update config.json with your target topic")
        print("3. Run: python test_auth.py")
        print("4. See QUICKSTART.md for usage instructions")
    else:
        print("✗ Some checks failed. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
