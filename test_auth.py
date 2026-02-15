#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from github_client import GitHubClient

if __name__ == "__main__":
    print("Testing GitHub API connection...")
    
    try:
        client = GitHubClient()
        username = client.get_authenticated_user()
        print(f"✓ Connected to GitHub as: {username}")
        print("\n✓ Authentication successful!")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease create a .env file with your GITHUB_TOKEN")
        print("Copy .env.example to .env and add your token")
        sys.exit(1)
    except ConnectionError as e:
        print(f"✗ Connection error: {e}")
        sys.exit(1)
