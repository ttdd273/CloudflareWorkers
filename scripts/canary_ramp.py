import argparse
import subprocess
from scripts.helpers import *

# We first get the versions 
# If there's only one version, we will just skip, it should just be skipped
# If there's more than two versions we can canary ramp 

def gradual_deploy(new_ver_id, new_ver_perc, old_ver_id, old_ver_perc):
    command = [
        "npx",
        "wrangler",
        "versions",
        "deploy",
        f"{old_ver_id}@{old_ver_perc}%",
        f"{new_ver_id}@{new_ver_perc}%",
        "-y",
        "--config",
        f"{WORKER_NAME}/wrangler.toml"
    ]

    # Run the subprocess for this
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Succesfully deploy new version ({new_ver_id}) to {new_ver_perc}%")
    else:
        print(f"Deployment failed: {result}")
        exit(1)

def canary_ramp(new_version_id, old_version_id, ramp_perc):
    try:
        gradual_deploy(new_version_id, ramp_perc, old_version_id, 100 - ramp_perc)
    except Exception as error:
        print(f"Exception occurred when deploying: {error}")

def main():
    parser = argparse.ArgumentParser(description="Canary deployment script.")
    parser.add_argument(
        "--ramp-percentage", 
        required=True, 
        help="The ramp percentage for the new version."
    )
    args = parser.parse_args()

    ramp_perc = int(args.ramp_percentage)
    old_version_id = os.getenv("OLD_VERSION_ID")
    new_version_id = os.getenv("NEW_VERSION_ID")

    canary_ramp(new_version_id, old_version_id, ramp_perc)

if __name__ == "__main__":
    main()