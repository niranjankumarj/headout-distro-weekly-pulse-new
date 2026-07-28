import shutil
import time
import zipfile

import requests

from config import DOWNLOAD_DIR, OMNI_API_TOKEN, OMNI_BASE_URL


class OmniClient:

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {OMNI_API_TOKEN}",
            "Content-Type": "application/json",
        }

    # --------------------------------------------------
    # Download
    # --------------------------------------------------

    def start_download(
        self,
        dashboard_id,
        filename,
    ):

        url = (
            f"{OMNI_BASE_URL}/api/v1/dashboards/"
            f"{dashboard_id}/download"
        )

        body = {
            "format": "csv",
            "filename": filename,
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=body,
        )

        # --------------------------------------------------
        # Debug Output
        # --------------------------------------------------

        if not response.ok:

            print("\n" + "=" * 60)
            print("OMNI API ERROR")
            print("=" * 60)
            print(f"URL: {url}")
            print(f"Dashboard ID: {dashboard_id}")
            print(f"Status Code: {response.status_code}")
            print("Response Headers:")
            print(dict(response.headers))
            print("Response Body:")
            print(response.text)
            print("=" * 60 + "\n")

        response.raise_for_status()

        return response.json()["job_id"]

    def wait_until_complete(
        self,
        dashboard_id,
        job_id,
    ):

        url = (
            f"{OMNI_BASE_URL}/api/v1/dashboards/"
            f"{dashboard_id}/download/{job_id}/status"
        )

        while True:

            response = requests.get(
                url,
                headers=self.headers,
            )

            response.raise_for_status()

            status = response.json()["status"]

            print(f"Status : {status}")

            if status == "complete":
                return

            time.sleep(2)

    def download_zip(
        self,
        dashboard_id,
        job_id,
        filename,
    ):

        url = (
            f"{OMNI_BASE_URL}/api/v1/dashboards/"
            f"{dashboard_id}/download/{job_id}"
        )

        response = requests.get(
            url,
            headers=self.headers,
        )

        response.raise_for_status()

        DOWNLOAD_DIR.mkdir(
            exist_ok=True
        )

        zip_path = DOWNLOAD_DIR / f"{filename}.zip"

        with open(zip_path, "wb") as f:
            f.write(response.content)

        print(f"Saved : {zip_path}")

        return zip_path

    def extract_zip(
        self,
        zip_path,
        folder_name,
    ):

        destination = DOWNLOAD_DIR / folder_name

        # ---------------------------------------------
        # Remove previous extracted files
        # ---------------------------------------------
        if destination.exists():
            shutil.rmtree(destination)

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        with zipfile.ZipFile(
            zip_path,
            "r",
        ) as zip_ref:

            zip_ref.extractall(destination)

        print(f"Extracted : {destination}")

        return destination

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def download_dashboard(
        self,
        dashboard_id,
        folder_name,
    ):

        print(f"\nDownloading {folder_name}...")

        job_id = self.start_download(
            dashboard_id,
            folder_name,
        )

        self.wait_until_complete(
            dashboard_id,
            job_id,
        )

        zip_path = self.download_zip(
            dashboard_id,
            job_id,
            folder_name,
        )

        return self.extract_zip(
            zip_path,
            folder_name,
        )