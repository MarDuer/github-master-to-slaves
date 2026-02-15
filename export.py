#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from github_client import GitHubClient
from exporter import export_branch_protection, save_branch_protection
from config import get_settings_dir

def main():
    parser = argparse.ArgumentParser(description="Export GitHub repository settings")
    parser.add_argument("--repo", required=True, help="Repository in format owner/name")
    args = parser.parse_args()
    
    print(f"Exporting settings from {args.repo}...")
    
    try:
        client = GitHubClient()
        repo = client.get_repo(args.repo)
        
        print(f"✓ Repository found: {repo.full_name}")
        
        branches_data = export_branch_protection(repo)
        print(f"✓ Exported {len(branches_data)} branches")
        
        settings_dir = get_settings_dir()
        settings_dir.mkdir(exist_ok=True)
        output_file = save_branch_protection(branches_data, settings_dir)
        
        print(f"✓ Saved to: {output_file}")
        print("\n✓ Export complete!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
