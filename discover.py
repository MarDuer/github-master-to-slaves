#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from github_client import GitHubClient
from discovery import find_repos_by_topic
from config import load_config

def main():
    print("Discovering target repositories...")
    
    try:
        config = load_config()
        topic = config["target_topic"]
        print(f"Looking for repositories with topic: {topic}")
        
        client = GitHubClient()
        repos = find_repos_by_topic(client, topic)
        
        if not repos:
            print(f"✗ No repositories found with topic '{topic}' where you have admin access")
            sys.exit(1)
        
        print(f"\n✓ Found {len(repos)} repositories:")
        for repo in repos:
            print(f"  - {repo.full_name}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
