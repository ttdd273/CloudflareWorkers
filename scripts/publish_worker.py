import subprocess
from scripts.helpers import *
import sys

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
        sys.exit(1)

if __name__ == "__main__":
    publish_worker()