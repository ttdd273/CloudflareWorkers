import argparse
import subprocess

# We first get the versions 
# If there's only one version, we will just skip, it should just be skipped
# If there's more than two versions we can canary ramp 

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

if __name__ == "main":
    parser = argparse.ArgumentParser(description="Canary deployment script.")
    parser.add_argument(
        "--ramp-percentage", 
        required=True, 
        help="The ramp percentage for the new version."
    )

    args = parser.parse_args()
    ramp_perc = args.ramp_percentage

    canary_ramp(ramp_perc)