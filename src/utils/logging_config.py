"""
Logging Configuration Module

This module provides centralized logging configuration for the entire application.
It configures logging with both console and file handlers, with automatic log rotation.
"""
import logging
import logging.config
from src.config import Config

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',  # Automatic log rotation
            'filename': str(Config.LOG_FILE),
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name):
    """
    Get a logger with the specified name
    
    Args:
        name: Logger name, typically __name__ of the calling module
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
