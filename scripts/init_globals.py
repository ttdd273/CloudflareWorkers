import os

# All global vars
WORKER_NAME = ACCOUNT_ID = CLOUDFLARE_API_KEY = BASE_URL = HEADERS = None

def initialize_globals():
    global WORKER_NAME, ACCOUNT_ID, CLOUDFLARE_API_KEY, BASE_URL, HEADERS

    # The account ID and the Cloudflare API key needs to be a secret of some sort
    ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_TOKEN")
    WORKER_NAME = os.getenv("WORKER_NAME")
    BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_NAME}"
    HEADERS = {
        "Authorization": f"Bearer {CLOUDFLARE_API_KEY}",
        "Content-Type": "application/json",
    }

# ----------------------------HELPER FUNCTION----------------------------------------
def prompt_for_approval(msg):
    """Prompts the user for a y/n answer."""
    user_input = input(msg)
    while user_input.lower() not in ["y", "n"]:
        user_input = input("Answer must be (y/n): ")
    if user_input == "y":
        return True
    return False

if __name__ == "__main__":
    initialize_globals()
