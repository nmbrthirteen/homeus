import yaml
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

def load_config(config_path: str) -> Dict[str, Any]:
    load_dotenv()
    
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    config = _substitute_env_vars(config)
    
    return config

def _substitute_env_vars(obj):
    if isinstance(obj, dict):
        return {key: _substitute_env_vars(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_substitute_env_vars(item) for item in obj]
    elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
        env_var = obj[2:-1]
        default_value = None
        if ':' in env_var:
            env_var, default_value = env_var.split(':', 1)
        return os.getenv(env_var, default_value)
    else:
        return obj 