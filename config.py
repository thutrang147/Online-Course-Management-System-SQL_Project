# Database configuration
from dotenv import load_dotenv
import os
# TODO: Move sensitive data to environment variables for production
DB_CONFIG = {
    'host': 'localhost',
    'database': 'OnlineCourses',
    'user': 'admin_app_user',
    'password': 'complexAdminPass456!'  # WARNING: Do not hardcode in production
}