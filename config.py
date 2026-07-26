import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# App Settings
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "15"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validate required environment variables
required_vars = {
    "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
}

missing = [key for key, value in required_vars.items() if not value]

if missing:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing)}"
    )
