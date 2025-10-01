import re
import hashlib
import time
from typing import Any, Dict
import json

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\!\?]', '', text)
    
    return text.strip()

def generate_text_hash(text: str) -> str:
    """Generate hash for text caching"""
    return hashlib.md5(text.encode()).hexdigest()

def timing_decorator(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def safe_json_parse(json_string: str, default: Any = None) -> Any:
    """Safely parse JSON string"""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default

def format_confidence(confidence: float) -> str:
    """Format confidence as percentage string"""
    return f"{confidence * 100:.1f}%"

def get_verdict_color(verdict: str) -> str:
    """Get color for verdict display"""
    colors = {
        'true': '#00ff9d',
        'false': '#ff0080', 
        'misleading': '#ffff00',
        'unverifiable': '#ffa500'
    }
    return colors.get(verdict, '#808080')