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
# MAIN
# ==============================

if __name__ == "__main__":

    response = requests.get(
        BASE_URL,
        auth=HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)
    )

    response.raise_for_status()

    results = response.json()["results"]

    print("\nCurrent IPs in MongoDB Atlas Access List:\n")

    for entry in results:
        print(f"- {entry['cidrBlock']}")

    print("\nTotal:", len(results))
