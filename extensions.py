import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure storage URI based on environment
redis_url = os.environ.get('REDIS_URL')
storage_uri = redis_url if redis_url else 'memory://'

# Single instance of Flask-Limiter for the entire application
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=storage_uri,
    default_limits=["200 per day", "50 per hour"]
)
