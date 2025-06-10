"""
Common utility functions used across projects.
"""
import os
from pathlib import Path
from typing import Optional

def get_project_root() -> Path:
    """Get the root directory of the project."""
    return Path(__file__).parent.parent.parent

def get_config_path() -> Path:
    """Get the path to the config directory."""
    return get_project_root() / "packages" / "config"

def load_env_file(env_file: Optional[str] = None) -> None:
    """Load environment variables from a .env file."""
    from dotenv import load_dotenv
    
    if env_file is None:
        env_file = get_project_root() / ".env"
    
    load_dotenv(env_file) 