import requests
import difflib
import sys
from scripts.helpers import *
import toml

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
    url = f"{BASE_URL}/versions/{latest_version_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("content", "")
    else:
        print(f"Failed to fetch version {latest_version_id}: {response.status_code} {response.text}")
        sys.exit(1)

def get_local_content():
    wrangler_path = f"{WORKER_NAME}/wrangler.toml"
    try:
        # Load the wrangler.toml file
        with open(wrangler_path, 'r') as toml_file:
            config = toml.load(toml_file)

        content_path = config.get('main', None)

        if not content_path:
            raise ValueError(f"'main' field not found in {wrangler_path}")

        local_path = f"{WORKER_NAME/{content_path}}"

        with open(local_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"{wrangler_path} not found.", file=sys.stderr)
        sys.exit(1)
    except toml.TomlDecodeError as e:
        print(f"Error parsing {wrangler_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        print(f'Something went wrong in getting local content', file=sys.stderr)
        sys.exit(1)
    

def display_diff(old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(),
        new_content.splitlines(),
        fromfile="Old Version",
        tofile="New Version",
        lineterm=""
    )
    return "\n".join(diff)


def main():
    # Get the most recent version
    # Compare it with the current version
    old_content = get_latest_content()
    new_content = get_local_content()
    display_diff(old_content, new_content)

if __name__ == "__main__":
    main()