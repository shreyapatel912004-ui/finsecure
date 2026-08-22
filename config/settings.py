from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / 'logs'
DATA_DIR = PROJECT_ROOT / 'data'

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_PATH = DATA_DIR / 'finsecure.db'

# GitHub API
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_API_URL = 'https://api.github.com'

# Stripe API
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY', '')

# Detection Patterns
SECRET_PATTERNS = {
    'stripe_live': r'sk_live_[a-zA-Z0-9]{32,}',
    'stripe_test': r'sk_test_[a-zA-Z0-9]{32,}',
    'stripe_restricted': r'rk_live_[a-zA-Z0-9]{32,}',
}

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = LOGS_DIR / 'finsecure.log'

# Scan settings
GITHUB_REPOS_LIMIT = 50
DAYS_LOOKBACK = 7
