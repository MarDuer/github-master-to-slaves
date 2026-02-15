#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import load_config, get_settings_dir, get_logs_dir

if __name__ == "__main__":
    print("Testing project setup...")
    
    config = load_config()
    print(f"✓ Config loaded: {config}")
    
    settings_dir = get_settings_dir()
    print(f"✓ Settings directory: {settings_dir}")
    
    logs_dir = get_logs_dir()
    print(f"✓ Logs directory: {logs_dir}")
    
    print("\n✓ Project setup complete!")
