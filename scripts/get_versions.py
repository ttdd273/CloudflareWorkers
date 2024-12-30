from scripts.helpers import *
import requests
import sys
import subprocess

def get_worker_versions():
    """
    Returns the old_version_id of a worker if it been changed, which would be 2nd most recent version.

    If there's less than 2 versions, the worker is either completely new, or a new version needs to be published.
    """
    # Curl equivalent in Python using requests to get all the versions of a worker
    url = f"{BASE_URL}/versions"
    
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        version_list = data["result"]["items"]

        if len(version_list) >= 2:
            # Get the first and second versions
            new_version_id = version_list[0]["id"]
            old_version_id = version_list[1]["id"]

            os.environ["OLD_VERSION_ID"] = old_version_id
            os.environ["NEW_VERSION_ID"] = new_version_id

            subprocess.run(['buildkite-agent',  'meta-data', 'set', 'OLD_VERSION_ID', old_version_id], capture_output=True, text=True)
            subprocess.run(['buildkite-agent',  'meta-data', 'set', 'NEW_VERSION_ID', new_version_id], capture_output=True, text=True)

            print("New Version:", new_version_id)
            print("Old Version:", old_version_id)
            print("Version IDs saved as metadata.")
        # else:
        # To deploy the first version of the worker, I guess we can use the publish command
        # print("This is the first deploy, come up with a diff workflow")
        # This is fine, nothing gets returned
    else:
        print(f"Version fetch failed. Status code: {response.status_code}, Response: {response.text}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    get_worker_versions()