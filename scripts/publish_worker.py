import subprocess
from scripts.init_globals import *

def publish_worker():
    """Publish the worker script to Cloudflare."""
    # We need to figure out how to get the script path
    command = [
        "npx",
        "wrangler",
        "versions",
        "upload",
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