import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from .model_config import ModelConfig, DEFAULT_CONFIGS

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self._config: Optional[ModelConfig] = None

    def load_config(self, model_name: str = "sd-v1-5") -> ModelConfig:
        """Load configuration from file or use default if not exists."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config_dict = json.load(f)
                self._config = ModelConfig.from_dict(config_dict)
        else:
            self._config = DEFAULT_CONFIGS.get(model_name, DEFAULT_CONFIGS["sd-v1-5"])
            self.save_config()
        
        return self._config

    def save_config(self) -> None:
        """Save current configuration to file."""
        if self._config is None:
            return
        
        config_dict = {
            field: getattr(self._config, field)
            for field in self._config.__dataclass_fields__
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_dict, f, indent=4)

    def update_config(self, **kwargs) -> None:
        """Update configuration with new values."""
        if self._config is None:
            self.load_config()
        
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
        
        self.save_config()

    def get_available_models(self) -> Dict[str, str]:
        """Get dictionary of available models and their IDs."""
        return {name: config.model_id for name, config in DEFAULT_CONFIGS.items()} 