from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import (
    SLACK_BOT_TOKEN,
    SLACK_DM_CHANNEL,
)


class SlackClient:

    def __init__(self):

        self.client = WebClient(
            token=SLACK_BOT_TOKEN
        )

    # --------------------------------------------------
    # Send Main Message
    # --------------------------------------------------

    def send(self, message):

        try:

            response = self.client.chat_postMessage(
                channel=SLACK_DM_CHANNEL,
                text=message,
            )

            message_ts = response["ts"]

            print("\n✓ Slack message sent successfully.")
            print(f"Message Timestamp: {message_ts}")

            return message_ts

        except SlackApiError as e:

            print("\n" + "=" * 60)
            print("Slack Error")
            print("=" * 60)
            print(e.response["error"])

            raise

    # --------------------------------------------------
    # Send Text Thread Reply
    # --------------------------------------------------

    def send_thread_reply(
        self,
        message,
        thread_ts,
    ):

        try:

            response = self.client.chat_postMessage(
                channel=SLACK_DM_CHANNEL,
                text=message,
                thread_ts=thread_ts,
            )

            print("\n✓ Thread reply sent successfully.")
            print(f"Thread Message Timestamp: {response['ts']}")

            return response["ts"]

        except SlackApiError as e:

            print("\n" + "=" * 60)
            print("Slack Thread Error")
            print("=" * 60)
            print(e.response["error"])

            raise

    # --------------------------------------------------
    # Upload Image to Thread
    # --------------------------------------------------

    def upload_image_to_thread(
        self,
        image_path,
        thread_ts,
    ):

        try:

            response = self.client.files_upload_v2(
                channel=SLACK_DM_CHANNEL,
                file=image_path,
                title="Distro Partnership Weekly Pulse",
                initial_comment="📱 Mobile-friendly report view",
                thread_ts=thread_ts,
            )

            print(
                "\n✓ Report image uploaded to Slack thread successfully."
            )

            return response

        except SlackApiError as e:

            print("\n" + "=" * 60)
            print("Slack Image Upload Error")
            print("=" * 60)
            print(e.response["error"])

            raise