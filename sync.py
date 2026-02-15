#!/usr/bin/env python3
import sys
import json
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from github_client import GitHubClient
from discovery import find_repos_by_topic
from exporter import export_branch_protection
from comparator import compare_branch_protection
from applier import apply_branch_protection, remove_branch_protection
from logger import ChangeLogger
from validator import validate_settings_file
from config import load_config, get_settings_dir, get_logs_dir

def load_master_settings():
    settings_file = get_settings_dir() / "branch-protection.json"
    if not settings_file.exists():
        raise FileNotFoundError(f"Settings file not found: {settings_file}")
    
    valid, error = validate_settings_file(settings_file)
    if not valid:
        raise ValueError(f"Invalid settings file: {error}")
    
    with open(settings_file) as f:
        return json.load(f)

def print_changes(repo_name, changes):
    if not changes["has_changes"]:
        print(f"  No changes needed")
        return
    
    if changes["additions"]:
        print(f"  Additions ({len(changes['additions'])} branches):")
        for item in changes["additions"]:
            print(f"    + {item['branch']}: Add protection")
    
    if changes["modifications"]:
        print(f"  Modifications ({len(changes['modifications'])} branches):")
        for item in changes["modifications"]:
            print(f"    ~ {item['branch']}: Update protection")
    
    if changes["deletions"]:
        print(f"  Deletions ({len(changes['deletions'])} branches):")
        for item in changes["deletions"]:
            print(f"    - {item['branch']}: Remove protection")

def apply_changes(repo, changes, logger, stop_on_error):
    success_count = 0
    error_count = 0
    
    for item in changes["additions"]:
        if apply_branch_protection(repo, item["branch"], item["protection"], logger):
            success_count += 1
        else:
            error_count += 1
            if stop_on_error:
                return success_count, error_count
    
    for item in changes["modifications"]:
        if apply_branch_protection(repo, item["branch"], item["new"], logger):
            success_count += 1
        else:
            error_count += 1
            if stop_on_error:
                return success_count, error_count
    
    for item in changes["deletions"]:
        if remove_branch_protection(repo, item["branch"], logger):
            success_count += 1
        else:
            error_count += 1
            if stop_on_error:
                return success_count, error_count
    
    return success_count, error_count

def main():
    parser = argparse.ArgumentParser(description="Apply GitHub repository settings")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    args = parser.parse_args()
    
    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"=== {mode} MODE ===\n")
    
    try:
        config = load_config()
        topic = config["target_topic"]
        stop_on_error = config.get("stop_on_error", False)
        
        master_settings = load_master_settings()
        print(f"✓ Loaded master settings ({len(master_settings)} branches)")
        
        client = GitHubClient()
        repos = find_repos_by_topic(client, topic)
        
        if not repos:
            print(f"✗ No repositories found with topic '{topic}'")
            sys.exit(1)
        
        print(f"✓ Found {len(repos)} target repositories\n")
        
        logger = None if args.dry_run else ChangeLogger(get_logs_dir())
        
        total_changes = 0
        total_success = 0
        total_errors = 0
        
        for repo in repos:
            print(f"Repository: {repo.full_name}")
            
            target_settings = export_branch_protection(repo)
            changes = compare_branch_protection(master_settings, target_settings)
            
            print_changes(repo.full_name, changes)
            
            if changes["has_changes"]:
                change_count = len(changes["additions"]) + len(changes["modifications"]) + len(changes["deletions"])
                total_changes += change_count
                
                if not args.dry_run:
                    success, errors = apply_changes(repo, changes, logger, stop_on_error)
                    total_success += success
                    total_errors += errors
                    print(f"  Applied: {success} successful, {errors} errors")
                    
                    if errors > 0 and stop_on_error:
                        print("\n✗ Stopped due to error (stop_on_error=true)")
                        break
            
            print()
        
        print(f"Summary: {total_changes} total changes across {len(repos)} repositories")
        
        if args.dry_run:
            print("\n✓ Dry-run complete (no changes applied)")
        else:
            print(f"✓ Applied: {total_success} successful, {total_errors} errors")
            print(f"✓ Log file: {logger.get_log_file()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
