import requests
import yaml
from requests.auth import HTTPDigestAuth
from pathlib import Path
import urllib.parse


# ==============================
# LOAD CONFIG
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT.joinpath("private", "private_config.yaml")

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

PUBLIC_KEY = config["MONGO_PUBLIC_KEY"]
PRIVATE_KEY = config["MONGO_PRIVATE_KEY"]
PROJECT_ID = config["MONGO_PROJECT_ID"]

BASE_URL = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{PROJECT_ID}/accessList"


# ==============================
# HELPERS
# ==============================

def get_current_ip():
    return requests.get("https://api.ipify.org").text.strip()


def get_access_list():
    r = requests.get(
        BASE_URL,
        auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)
    )
    r.raise_for_status()
    return r.json()["results"]



def delete_ip(cidr_block):
    encoded = urllib.parse.quote(cidr_block, safe='')
    url = f"{BASE_URL}/{encoded}"

    r = requests.delete(
        url,
        auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    r.raise_for_status()


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    current_ip = get_current_ip()
    current_cidr = f"{current_ip}/32"

    print(f"Current IP: {current_ip}")
    print("Cleaning Atlas IP access list...\n")

    access_list = get_access_list()

    for entry in access_list:
        cidr = entry["cidrBlock"]

        if cidr != current_cidr:
            print(f"Removing: {cidr}")
            delete_ip(cidr)
        else:
            print(f"Keeping: {cidr}")

    print("\nDone.")
