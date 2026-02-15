# Justfile Added for Easier Command Handling

## What is Just?

`just` is a command runner that makes it easy to run project-specific commands. It's similar to `make` but simpler and more modern.

Install from: https://github.com/casey/just

## Available Commands

Run `just --list` to see all available commands:

```bash
$ just --list
Available recipes:
    clean       # Clean generated files
    default     # List available commands
    discover    # Discover repositories with configured topic
    dry-run     # Preview changes without applying (dry-run)
    export repo # Export settings from a repository (usage: just export owner/repo)
    install     # Install dependencies
    setup       # Setup project (install + create .env)
    sync        # Apply settings to target repositories
    test        # Run all tests
    test-auth   # Test GitHub authentication
    verify      # Verify project setup
```

## Command Reference

### Setup Commands

```bash
# Install dependencies
just install

# Setup project (install + create .env file)
just setup

# Verify project setup
just verify

# Test GitHub authentication
just test-auth
```

### Workflow Commands

```bash
# Export settings from a repository
just export owner/repo-name

# Discover target repositories
just discover

# Preview changes (dry-run)
just dry-run

# Apply changes
just sync
```

### Utility Commands

```bash
# Run all tests
just test

# Clean generated files
just clean
```

## Benefits

1. **Shorter commands** - `just sync` instead of `uv run python sync.py`
2. **Easier to remember** - Descriptive command names
3. **Self-documenting** - `just --list` shows all available commands
4. **Consistent** - Same commands work across different environments
5. **Convenient** - `just setup` handles multiple steps at once

## Comparison

### Before (without just)
```bash
uv sync
cp .env.example .env
# Edit .env manually
uv run python verify.py
uv run python test_auth.py
uv run python export.py --repo owner/repo
uv run python discover.py
uv run python sync.py --dry-run
uv run python sync.py
```

### After (with just)
```bash
just setup
just verify
just test-auth
just export owner/repo
just discover
just dry-run
just sync
```

## Documentation Updates

All documentation has been updated to include justfile commands:

- ✅ README.md - Installation and usage sections
- ✅ QUICKSTART.md - All workflow steps
- ✅ COMPLETE.md - Command reference and getting started
- ✅ New troubleshooting section about just commands

## You Can Still Use UV Directly

The justfile is optional. You can still use `uv run python` commands directly:

```bash
uv run python export.py --repo owner/repo
uv run python sync.py --dry-run
```

Both approaches work equally well. The justfile just makes it more convenient!
