#!/usr/bin/env python3

import os
import requests
import subprocess

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_TOKEN")
WORKER_NAME = os.getenv("WORKER_NAME")
BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}"
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
    "Content-Type": "application/javascript",
}

def publish_worker():
    """Publish the worker script to Cloudflare."""
    # We need to figure out how to get the script path
    command = [
        "npx",
        "wrangler",
        "deploy",
        "--config",
        f"{WORKER_NAME}/wrangler.toml"
    ]

    # Run the subprocess for this
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Succesfully published new version.")
    else:
        print(f"Deployment failed: {result}")
        exit(1)
    
    # try:
    #     with open(script_path, "r") as script_file:
    #         script_content = script_file.read()

    #     response = requests.put(BASE_URL, headers=HEADERS, data=script_content)

    #     if response.status_code == 200:
    #         print(f"Worker '{WORKER_NAME}' deployed successfully.")
    #         return response.json()["result"]["id"]
    #     print(f"Failed to deploy worker: {response.status_code} {response.text}")
    #     exit(1)

    # except Exception as e:
    #     print(f"Error uploading worker: {e}")
    #     exit(1)

if __name__ == "__main__":
    publish_worker()