import requests
import difflib
import sys
import subprocess
from scripts.helpers import *


def get_latest_version():
    url = f"{BASE_URL}/versions"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        versions = response.json().get("result", {}).get("items", [])
        if versions:
            latest_version = versions[0]
            return latest_version["id"]
        else:
            print("No versions found for the worker.")
            sys.exit(1)
    else:
        print(f"Failed to fetch versions: {response.status_code} {response.text}")
        sys.exit(1)


def get_latest_content():
    latest_version_id = get_latest_version()
    url = f"{BASE_URL}/content/v2"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        content = response.text
        lines = content.splitlines()
        lines = lines[3:-2]
        cleaned_content = "\n".join(lines)
        return cleaned_content
    else:
        print(
            f"Failed to fetch version {latest_version_id}: {response.status_code} {response.text}"
        )
        sys.exit(1)


def get_local_content():
    try:
        command = [
            "npx",
            "wrangler",
            "deploy",
            "--dry-run",
            "--outdir",
            f"dist",
            "--config",
            f"{WORKER_NAME}/wrangler.toml",
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Local dry run failed: {result}")
            exit(1)
        # Read the file and return it
        with open(f"{WORKER_NAME}/dist/index.js", "r") as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Something went wrong in getting local content: {e}", file=sys.stderr)
        sys.exit(1)


def display_diff(old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(),
        new_content.splitlines(),
        fromfile="Old Version",
        tofile="New Version",
        lineterm="",
    )
    colored_diff = []
    
    for line in diff:
        if line.startswith("+") or line.startswith("+++"):
            colored_diff.append(f"{GREEN}{line}{RESET}")
        elif line.startswith("-") or line.startswith("---"):
            colored_diff.append(f"{RED}{line}{RESET}")
        else:
            colored_diff.append(line)
    return "\n".join(colored_diff)


def main():
    # Get the most recent version
    # Compare it with the current version
    old_content = get_latest_content()
    new_content = get_local_content()
    # print(old_content)
    print(display_diff(old_content, new_content))


if __name__ == "__main__":
    main()
