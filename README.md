# GitHub Repository Settings Sync Tool

A Python CLI tool to synchronize GitHub repository settings from a master repository to multiple target repositories identified by topics.

## Features

- **Export settings** from any repository to JSON files
- **Topic-based targeting** - sync to repositories with specific topics
- **Dry-run mode** - preview changes before applying
- **Detailed logging** - track all changes in JSONL format
- **Modular settings** - currently supports branch protection rules
- **Error handling** - configurable stop-on-error behavior

## Prerequisites

- Python 3.8+
- GitHub Personal Access Token with `repo` scope
- Admin access to repositories you want to manage

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd github-master-to-slaves
```

2. Install dependencies using uv:
```bash
uv sync
# Or using just:
just install
```

3. Configure authentication:
```bash
cp .env.example .env
# Edit .env and add your GitHub token
# Or use just setup to do both:
just setup
```

4. Configure tool settings:
```bash
# Edit config.json
{
  "target_topic": "sync-from-master",  # Topic to identify target repos
  "stop_on_error": false               # Continue on errors or stop
}
```

## Usage

### 1. Export Settings from Master Repository

Export branch protection settings from your master repository:

```bash
python export.py --repo owner/master-repo
# Or using just:
just export owner/master-repo
```

This creates `settings/branch-protection.json` with all branch protection rules.

### 2. Tag Target Repositories

Add the configured topic (e.g., `sync-from-master`) to all repositories you want to sync:

- Go to each repository on GitHub
- Click "Settings" → scroll to "Topics"
- Add your configured topic

### 3. Discover Target Repositories

Verify which repositories will be affected:

```bash
python discover.py
# Or using just:
just discover
```

### 4. Preview Changes (Dry-Run)

See what changes would be applied without making any modifications:

```bash
python sync.py --dry-run
# Or using just:
just dry-run
```

### 5. Apply Changes

Apply the settings to all target repositories:

```bash
python sync.py
# Or using just:
just sync
```

Changes are logged to `logs/sync_TIMESTAMP.jsonl`.

## Configuration Files

### config.json

```json
{
  "target_topic": "sync-from-master",
  "stop_on_error": false
}
```

- `target_topic`: GitHub topic used to identify target repositories
- `stop_on_error`: If `true`, stops on first error; if `false`, continues and reports all errors

### settings/branch-protection.json

Example structure:

```json
[
  {
    "name": "main",
    "protection": {
      "required_status_checks": {
        "strict": true,
        "contexts": ["ci/test", "ci/lint"]
      },
      "required_pull_request_reviews": {
        "dismiss_stale_reviews": true,
        "require_code_owner_reviews": true,
        "required_approving_review_count": 2
      },
      "enforce_admins": false,
      "restrictions": {
        "users": [],
        "teams": []
      }
    }
  },
  {
    "name": "develop"
  }
]
```

Branches without a `protection` key will not have protection applied.

## Log Files

Logs are written to `logs/sync_TIMESTAMP.jsonl` in JSON Lines format:

```json
{"timestamp": "2026-02-15T22:00:00", "repository": "owner/repo", "setting_type": "branch_protection", "action": "apply", "details": {...}, "status": "success"}
{"timestamp": "2026-02-15T22:00:01", "repository": "owner/repo2", "setting_type": "branch_protection", "action": "apply", "details": {...}, "status": "error", "error": "..."}
```

## Troubleshooting

### Using Just Commands

This project includes a `justfile` for easier command execution. Install `just` from https://github.com/casey/just

Available commands:
```bash
just --list              # List all available commands
just install             # Install dependencies
just setup               # Install + create .env file
just verify              # Verify project setup
just test-auth           # Test GitHub authentication
just export owner/repo   # Export settings from a repository
just discover            # Discover target repositories
just dry-run             # Preview changes
just sync                # Apply changes
just test                # Run all tests
just clean               # Clean generated files
```

### "GITHUB_TOKEN not found in environment variables"

Create a `.env` file with your GitHub Personal Access Token:
```
GITHUB_TOKEN=ghp_your_token_here
```

### "No repositories found with topic 'X'"

Ensure:
1. You've added the topic to target repositories
2. You have admin access to those repositories
3. The topic in `config.json` matches exactly

### "Settings file not found"

Run `python export.py --repo owner/master-repo` first to create the settings file.

### "Invalid settings file"

Check that your `settings/branch-protection.json` is valid JSON and follows the correct schema. Common issues:
- Missing `name` field for branches
- Invalid `required_approving_review_count` (must be 1-6)
- Malformed JSON syntax

### Permission Errors

Ensure your GitHub token has:
- `repo` scope (full control of private repositories)
- Admin access to all target repositories

### Rate Limiting

PyGithub automatically handles rate limiting. If you hit limits:
- Wait for the rate limit to reset (shown in error message)
- Consider using a GitHub App instead of PAT for higher limits

## Future Enhancements

Additional settings groups can be added incrementally:
- Repository settings (description, homepage, features)
- Labels
- Topics
- Collaborators
- Security settings
- Webhooks

## License

MIT License - see LICENSE file for details.
