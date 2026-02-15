# Migration to UV Package Manager

## Changes Made

The project has been migrated from `pip` to `uv` for dependency management.

### Files Changed

1. **pyproject.toml** (new)
   - Replaced `requirements.txt`
   - Defines project metadata and dependencies
   - Configured for Python 3.8+
   - Includes hatch build configuration

2. **Documentation Updates**
   - README.md - Updated installation instructions
   - QUICKSTART.md - Updated all commands to use `uv run`
   - COMPLETE.md - Updated quick start and commands
   - IMPLEMENTATION_SUMMARY.md - Updated references
   - verify.py - Updated error messages

### Key Differences

#### Before (pip)
```bash
pip install -r requirements.txt
python export.py --repo owner/name
```

#### After (uv)
```bash
uv sync
uv run python export.py --repo owner/name
```

### Benefits of UV

1. **Faster** - Much faster dependency resolution and installation
2. **Deterministic** - Creates lock file for reproducible builds
3. **Modern** - Uses pyproject.toml standard
4. **Virtual Environment** - Automatically manages `.venv`
5. **Better Caching** - Efficient package caching

### Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
cd github-master-to-slaves
uv sync
```

### Usage

All Python scripts should be run with `uv run`:

```bash
# Verify setup
uv run python verify.py

# Test authentication
uv run python test_auth.py

# Export settings
uv run python export.py --repo owner/repo

# Discover repositories
uv run python discover.py

# Sync settings (dry-run)
uv run python sync.py --dry-run

# Sync settings (apply)
uv run python sync.py
```

### Virtual Environment

UV automatically creates and manages a `.venv` directory:

```bash
# Activate virtual environment (optional)
source .venv/bin/activate

# Now you can run scripts directly
python export.py --repo owner/repo

# Deactivate when done
deactivate
```

### Project Structure

```
github-master-to-slaves/
├── pyproject.toml         # Project configuration (replaces requirements.txt)
├── .venv/                 # Virtual environment (created by uv sync)
├── uv.lock               # Lock file (created by uv sync)
├── src/                   # Source code
├── settings/              # Settings files
├── logs/                  # Log files
└── ...
```

### Troubleshooting

#### "uv: command not found"
Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### "No solution found when resolving dependencies"
Check Python version:
```bash
python --version  # Should be 3.8 or higher
```

#### "Module not found" errors
Run uv sync:
```bash
uv sync
```

### Migration Checklist

- [x] Created pyproject.toml
- [x] Removed requirements.txt
- [x] Updated README.md
- [x] Updated QUICKSTART.md
- [x] Updated COMPLETE.md
- [x] Updated IMPLEMENTATION_SUMMARY.md
- [x] Updated verify.py
- [x] Tested uv sync
- [x] Tested uv run python verify.py
- [x] All dependencies installed correctly

## Verification

Run the verification script to ensure everything is set up correctly:

```bash
uv run python verify.py
```

You should see:
```
✓ All checks passed!
```

## Next Steps

1. Run `uv sync` to install dependencies
2. Configure `.env` with your GitHub token
3. Follow QUICKSTART.md for usage instructions
