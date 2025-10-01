import os
from dataclasses import dataclass
from typing import Dict, List
import yaml

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    MODEL_NAMES = {
        'deberta': 'microsoft/deberta-v3-base',
        'roberta': 'roberta-base',
        'electra': 'google/electra-base-discriminator',
        'bert': 'bert-base-uncased'
    }
    
    ENSEMBLE_WEIGHTS = {
        'deberta': 0.35,
        'roberta': 0.25,
        'electra': 0.20,
        'bert': 0.20
    }
    
    CONFIDENCE_THRESHOLDS = {
        'high': 0.85,
        'medium': 0.70,
        'low': 0.55
    }

@dataclass
class APIConfig:
    """API configurations"""
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'your_news_api_key')
    WIKIPEDIA_RATE_LIMIT = 1  # requests per second
    REQUEST_TIMEOUT = 30

@dataclass
class PathConfig:
    """Path configurations"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, 'models', 'trained')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    
    def ensure_directories(self):
        """Create necessary directories"""
        for directory in [self.MODEL_DIR, self.DATA_DIR, self.LOG_DIR]:
            os.makedirs(directory, exist_ok=True)

class AppConfig:
    """Main application configuration"""
    def __init__(self):
        self.models = ModelConfig()
        self.api = APIConfig()
        self.paths = PathConfig()
        self.paths.ensure_directories()
        
        # Application settings
        self.MAX_INPUT_LENGTH = 1000
        self.CACHE_DURATION = 3600  # 1 hour
        self.LOG_LEVEL = 'INFO'

# Global configuration instance
config = AppConfig()