from urllib.parse import quote
import json
import requests

from config import OMNI_API_TOKEN, OMNI_BASE_URL

dashboard_id = "fe5fe006"

headers = {
    "Authorization": f"Bearer {OMNI_API_TOKEN}",
    "Content-Type": "application/json",
}

filter_value = quote(json.dumps({
    "left_side": "400 complete days ago",
    "right_side": "400 days"
}))

url = (
    f"{OMNI_BASE_URL}/api/v1/dashboards/"
    f"{dashboard_id}/download"
    f"?f--K8KUMBhs={filter_value}"
)

response = requests.post(
    url,
    headers=headers,
    json={
        "format": "csv",
        "filename": "test",
    },
)

print("Status:", response.status_code)
print(response.text)