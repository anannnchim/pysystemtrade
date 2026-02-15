import requests
import yaml
from requests.auth import HTTPDigestAuth
from pathlib import Path


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


def add_ip(ip):
    payload = [{
        "ipAddress": ip,
        "comment": "Auto-added by update_ip.py"
    }]

    r = requests.post(
        BASE_URL,
        json=payload,
        auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    r.raise_for_status()


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    current_ip = get_current_ip()
    current_cidr = f"{current_ip}/32"

    print(f"\nCurrent IP: {current_ip}")

    access_list = get_access_list()
    existing_ips = [entry["cidrBlock"] for entry in access_list]

    if current_cidr in existing_ips:
        print("IP already exists in Atlas. Nothing to do.")
    else:
        print("IP not found. Adding to Atlas...")
        add_ip(current_ip)
        print("IP successfully added.")

    print("\nDone.")
