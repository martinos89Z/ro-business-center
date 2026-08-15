import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Security: SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set. Please set it in your .env file.")

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "instance" / "ro_business.db"}')
USE_POSTGRES = 'postgresql' in DATABASE_URL

# Upload configuration
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit for security
WHATSAPP_PHONE = os.environ.get('WHATSAPP_PHONE', '22892888759')

# Admin login rate limiting
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_WINDOW = 300  # 5 minutes in seconds
