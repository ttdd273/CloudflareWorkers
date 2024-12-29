import os
import requests

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_TOKEN")
WORKER_NAME = os.getenv("WORKER_NAME")
BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}"
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
    "Content-Type": "application/json",
}

def publish_worker(script_path):
    """Publish the worker script to Cloudflare."""
    # We need to figure out how to get the script path
    print(f"Clloudflare id {ACCOUNT_ID}")
    print(f"Worker name {WORKER_NAME}")

    try:
        with open(script_path, "r") as script_file:
            script_content = script_file.read()

        response = requests.put(BASE_URL, headers=HEADERS, data=script_content)

        if response.status_code == 200:
            print(f"Worker '{WORKER_NAME}' deployed successfully.")
            return response.json()["result"]["id"]
        else:
            print(f"Failed to deploy worker: {response.status_code} {response.text}")
        return None
    except Exception as e:
        print(f"Error uploading worker: {e}")

if __name__ == "main":
    publish_worker(f"{WORKER_NAME}/scr/index.js")