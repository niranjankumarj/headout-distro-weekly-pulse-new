from config import DASHBOARDS
from omni import OmniClient

client = OmniClient()

client.download_dashboard(
    DASHBOARDS["api_agent"],
    "api_agent",
)