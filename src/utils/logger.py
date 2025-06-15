import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any

def setup_logger(config: Dict[str, Any]) -> logging.Logger:
    logger = logging.getLogger('homeus')
    logger.setLevel(getattr(logging, config.get('level', 'INFO')))
    
    if logger.handlers:
        logger.handlers.clear()
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if config.get('file'):
        log_file = Path(config['file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        max_bytes = config.get('max_size_mb', 10) * 1024 * 1024
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger 