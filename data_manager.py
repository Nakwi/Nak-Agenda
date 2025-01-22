import json
from config import DEVOIRS_FILE

def load_devoirs():
    try:
        with open(DEVOIRS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_devoirs(liste_devoirs):
    with open(DEVOIRS_FILE, "w") as file:
        json.dump(liste_devoirs, file, indent=4)
