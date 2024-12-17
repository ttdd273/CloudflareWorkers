import requests
import json
import subprocess
import time

# Set variables
SCRIPT_NAME = "first-worker-tong"
ACCOUNT_ID = "ce4d5664815cbd558429d45bfaac44d2"
CLOUDFLARE_EMAIL = "tong.duan@affirm.com"
CLOUDFLARE_API_KEY = "xtP2Gs0X6IT9X3qhW2Plh8hgYSEPcXwU-8hKkuYu"

# Curl equivalent in Python using requests to get all the versions of a worker
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}/versions"
headers = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
    "Content-Type": "application/json"
}

ramp_up_values = [3, 6, 10, 16, 25, 50, 100]

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    version_list = data["result"]["items"]
    
    if len(version_list) >= 2:
        # Get the first and second versions
        new_version_id = version_list[0]["id"]
        old_version_id = version_list[1]["id"]

        print("New Version:", new_version_id)
        print("Old Version:", old_version_id)
    else:
        # To deploy the first version of the worker, I guess we can use the publish command
        print("This is the first deploy, come up with a diff workflow")
else:
    print(f"Version fetch failed. Status code: {response.status_code}, Response: {response.text}")

# After getting the versions, we need to perform the ramp
# In order to run this, we need to run the subprocess 

def deploy_version(new_ver_id, new_ver_perc, old_ver_id, old_ver_perc):
    command = ["npx",
        "wrangler", 
        "versions", 
        "deploy", 
        f"{new_ver_id}@{new_ver_perc}%", 
        f"{old_ver_id}@{old_ver_perc}%", 
        "-y"
    ]

    # Run the subprocess for this
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Succesfully deploy new version ({new_ver_id}) to {new_ver_perc}%")
    else:
        print(f"Deployment failed: {result}")

for ramp_perc in ramp_up_values:
    try:
        deploy_version(new_version_id, ramp_perc, old_version_id, 100-ramp_perc)
    except Exception as error:
        print(f"Exception occurred when deploying: {error}")

    if ramp_perc != 100:
        # We still have more to go
        time.sleep(120)

print("Finished canary deployment")