# GitHub Repository Settings Sync Tool
# Use 'just' to run common tasks

# List available commands
default:
    @just --list

# Install dependencies
install:
    uv sync

# Verify project setup
verify:
    uv run python verify.py

# Test GitHub authentication
test-auth:
    uv run python test_auth.py

# Export settings from a repository (usage: just export owner/repo)
export repo:
    uv run python export.py --repo {{repo}}

# Discover repositories with configured topic
discover:
    uv run python discover.py

# Preview changes without applying (dry-run)
dry-run:
    uv run python sync.py --dry-run

# Apply settings to target repositories
sync:
    uv run python sync.py

# Run all tests
test:
    uv run python test_setup.py
    uv run python test_auth.py

# Clean generated files
clean:
    rm -rf .venv uv.lock
    rm -rf logs/*.jsonl
    find . -type d -name __pycache__ -exec rm -rf {} +

# Setup project (install + create .env)
setup:
    uv sync
    @if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file - please add your GitHub token"; fi
    @echo "Run 'just verify' to check setup"
