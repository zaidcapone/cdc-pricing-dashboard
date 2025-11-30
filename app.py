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
            if 'app_cache' not in st.session_state:
                st.session_state.app_cache = {}
            
            # Check if cached data exists and is not expired
            if key in st.session_state.app_cache:
                cached_data, timestamp = st.session_state.app_cache[key]
                if time.time() - timestamp < ttl:
                    return cached_data
            
            # If not cached or expired, call the function
            result = func(*args, **kwargs)
            st.session_state.app_cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached data"""
    if 'app_cache' in st.session_state:
        st.session_state.app_cache = {}
