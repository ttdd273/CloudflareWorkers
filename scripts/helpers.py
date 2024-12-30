import os

# -----------------------------GLOBAL VARS-------------------------------------
# The account ID and the Cloudflare API key needs to be a secret of some sort

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_TOKEN")
WORKER_NAME = os.getenv("WORKER_NAME")
BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}"
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
    "Content-Type": "application/json",
}

# ANSI escape sequences for coloring text
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# ----------------------------HELPER FUNCTION----------------------------------------
def prompt_for_approval(msg):
    """Prompts the user for a y/n answer."""
    user_input = input(msg)
    while user_input.lower() not in ["y", "n"]:
        user_input = input("Answer must be (y/n): ")
    if user_input == "y":
        return True
    return False