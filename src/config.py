import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Omni Configuration
# --------------------------------------------------

OMNI_BASE_URL = "https://headout.omniapp.co"
OMNI_API_TOKEN = os.getenv("OMNI_API_TOKEN")

# --------------------------------------------------
# Slack Configuration
# --------------------------------------------------

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_DM_CHANNEL = os.getenv("SLACK_DM_CHANNEL")

# --------------------------------------------------
# Download folder
# --------------------------------------------------

DOWNLOAD_DIR = Path("downloads")

# --------------------------------------------------
# Dashboards
# --------------------------------------------------

DASHBOARDS = {
    "affiliate": "8ffd90f4",
    "api_agent": "fe5fe006",
}