# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
uv sync
# Or using just:
just install
```

### 2. Configure GitHub Token
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your token
# Get token from: https://github.com/settings/tokens
# Required scope: repo (full control)

# Or use just to do both:
just setup
```

Your `.env` file should look like:
```
GITHUB_TOKEN=ghp_your_actual_token_here
```

### 3. Configure Target Topic
Edit `config.json`:
```json
{
  "target_topic": "sync-from-master",
  "stop_on_error": false
}
```

### 4. Test Connection
```bash
uv run python test_auth.py
# Or using just:
just test-auth
```

You should see:
```
✓ Connected to GitHub as: your-username
✓ Authentication successful!
```

## Usage Workflow

### Step 1: Export Settings from Master Repository
```bash
uv run python export.py --repo your-org/master-repo
# Or using just:
just export your-org/master-repo
```

This creates `settings/branch-protection.json` with all branch protection rules from your master repository.

### Step 2: Add Topic to Target Repositories

On GitHub, for each repository you want to sync:
1. Go to repository → Settings
2. Scroll to "Topics" section
3. Add the topic: `sync-from-master` (or whatever you configured)

### Step 3: Verify Target Repositories
```bash
uv run python discover.py
# Or using just:
just discover
```

You should see a list of repositories with your topic.

### Step 4: Preview Changes (Dry-Run)
```bash
uv run python sync.py --dry-run
# Or using just:
just dry-run
```

This shows what changes would be applied without actually making them.

### Step 5: Apply Changes
```bash
uv run python sync.py
# Or using just:
just sync
```

This applies the settings to all target repositories and creates a log file in `logs/`.

## Example Output

### Export Command
```
$ uv run python export.py --repo myorg/master-repo
Exporting settings from myorg/master-repo...
✓ Repository found: myorg/master-repo
✓ Exported 3 branches
✓ Saved to: /path/to/settings/branch-protection.json
✓ Export complete!
```

### Discover Command
```
$ uv run python discover.py
Discovering target repositories...
Looking for repositories with topic: sync-from-master

✓ Found 2 repositories:
  - myorg/repo1
  - myorg/repo2
```

### Dry-Run
```
$ uv run python sync.py --dry-run
=== DRY-RUN MODE ===

✓ Loaded master settings (3 branches)
✓ Found 2 target repositories

Repository: myorg/repo1
  Modifications (1 branches):
    ~ main: Update protection

Repository: myorg/repo2
  No changes needed

Summary: 1 total changes across 2 repositories

✓ Dry-run complete (no changes applied)
```

### Apply Changes
```
$ uv run python sync.py
=== APPLY MODE ===

✓ Loaded master settings (3 branches)
✓ Found 2 target repositories

Repository: myorg/repo1
  Modifications (1 branches):
    ~ main: Update protection
  Applied: 1 successful, 0 errors

Repository: myorg/repo2
  No changes needed

Summary: 1 total changes across 2 repositories
✓ Applied: 1 successful, 0 errors
✓ Log file: /path/to/logs/sync_20260215_220000.jsonl
```

## Troubleshooting

### Error: "GITHUB_TOKEN not found"
- Make sure you created `.env` file (not `.env.example`)
- Check that the token is on a line: `GITHUB_TOKEN=ghp_...`
- No quotes needed around the token

### Error: "Module not found"
- Run `uv sync` to install dependencies
- Make sure you're in the project directory

### Error: "No repositories found with topic"
- Verify you added the topic to repositories on GitHub
- Check the topic name matches exactly (case-sensitive)
- Ensure you have admin access to those repositories

### Error: "Settings file not found"
- Run `uv run python export.py --repo owner/repo` first
- Check that `settings/branch-protection.json` was created

### Error: "Invalid settings file"
- Open `settings/branch-protection.json` and verify it's valid JSON
- Check for syntax errors (missing commas, brackets, etc.)
- Ensure `required_approving_review_count` is between 1-6

## Tips

1. **Always run dry-run first** to preview changes before applying
2. **Start with one test repository** - add the topic to just one repo initially
3. **Check the log files** in `logs/` directory for detailed information
4. **Use stop_on_error: true** in config.json when testing to catch issues early
5. **Keep settings in version control** - commit the `settings/` directory to track changes

## What's Next?

Once you're comfortable with branch protection, you can extend the tool to sync:
- Repository settings (description, features, visibility)
- Labels and milestones
- Topics
- Collaborators and teams
- Security settings

The modular design makes it easy to add new settings groups following the same pattern.
