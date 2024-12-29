import os
import subprocess
import requests

# --------------------------------------------GLOBAL VARS------------------------------------
WORKER_NAME = ACCOUNT_ID = CLOUDFLARE_API_KEY = BASE_URL = HEADERS = None


def initialize_globals():
    global WORKER_NAME, ACCOUNT_ID, CLOUDFLARE_API_KEY, BASE_URL, HEADERS

    # The account ID and the Cloudflare API key needs to be a secret of some sort
    ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_TOKEN")
    WORKER_NAME = input("Please enter the worker name: ")
    BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}"


def publish_worker(script_path):
    """Publish the worker script to Cloudflare."""
    # We need to figure out how to get the script path
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


def get_old_worker_versions():
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
            # new_version_id = version_list[0]["id"]
            old_version_id = version_list[1]["id"]

            # print("New Version:", new_version_id)
            # print("Old Version:", old_version_id)
            return old_version_id
        else:
            # To deploy the first version of the worker, I guess we can use the publish command
            # print("This is the first deploy, come up with a diff workflow")
            return None
    else:
        print(
            f"Version fetch failed. Status code: {response.status_code}, Response: {response.text}"
        )


def gradual_deploy(new_ver_id, new_ver_perc, old_ver_id, old_ver_perc):
    command = [
        "npx",
        "wrangler",
        "versions",
        "deploy",
        f"{new_ver_id}@{new_ver_perc}%",
        f"{old_ver_id}@{old_ver_perc}%",
        "-y",
    ]

    # Run the subprocess for this
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Succesfully deploy new version ({new_ver_id}) to {new_ver_perc}%")
    else:
        print(f"Deployment failed: {result}")


def prompt_for_approval(msg):
    """Prompts the user for a y/n answer."""
    user_input = input(msg)
    while user_input.lower() not in ["y", "n"]:
        user_input = input("Answer must be (y/n): ")
    if user_input == "y":
        return True
    return False


def canary_ramp(new_version_id, old_version_id):
    ramp_up_values = [1, 5, 10, 25, 50, 75, 100]

    for ramp_perc in ramp_up_values:
        try:
            gradual_deploy(new_version_id, ramp_perc, old_version_id, 100 - ramp_perc)
        except Exception as error:
            print(f"Exception occurred when deploying: {error}")

        if ramp_perc != 100:
            if prompt_for_approval(
                f"Deployed to {ramp_perc}%. Do you approve to proceed? (y/n):"
            ):
                continue
            else:
                # We need to abort the workflow
                gradual_deploy(new_version_id, 0, old_version_id, 100)
                break


def full_ramp(new_version_id):
    payload = {"new_version_id": new_version_id, "enabled": True}

    try:
        # Send PUT request to deploy traffic
        response = requests.put(f"{BASE_URL}/traffic", headers=HEADERS, json=payload)

        if response.status_code == 200:
            print(f"All traffic routed to the new version: {new_version_id}")
        else:
            print(f"Failed to route traffic: {response.status_code} {response.text}")
            # response.raise_for_status()
    except Exception as e:
        print(f"An error occurred while deploying traffic: {e}")


if __name__ == "main":
    initialize_globals()

    # We will need to publish the new version of the worker
    # After publishing, we can get worker versions
    # If it's < 2 versions, we can just ramp to 100 right away, 'cause it's new
    # If it >= 2 versions, then we need to canary ramp
    new_version_id = publish_worker(f"{WORKER_NAME}/src/index.js")

    old_version_id = get_old_worker_versions()
    if not old_version_id and new_version_id:
        full_ramp(new_version_id)
    elif old_version_id and new_version_id:
        canary_ramp(new_version_id, old_version_id)
    else:
        print(f"Something went wrong with finding old and new version IDs")
