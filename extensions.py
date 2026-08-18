from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Single instance of Flask-Limiter for the entire application
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
