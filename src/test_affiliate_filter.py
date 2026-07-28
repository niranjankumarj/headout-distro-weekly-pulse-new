from omni import OmniClient

client = OmniClient()

job_id = client.start_download(
    "8ffd90f4",
    "affiliate_test",
)

client.wait_until_complete(
    "8ffd90f4",
    job_id,
)

zip_path = client.download_zip(
    "8ffd90f4",
    job_id,
    "affiliate_test",
)

client.extract_zip(
    zip_path,
    "affiliate_test",
)