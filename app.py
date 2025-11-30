import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from io import BytesIO
import time
import functools

# ==================== CACHE CONFIGURATION ====================
# Cache configuration
CACHE_DURATION = 300  # 5 minutes cache

def cache_data(ttl=CACHE_DURATION):
    """Decorator to cache function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key for this function call
            key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Initialize cache if not exists
            if '
