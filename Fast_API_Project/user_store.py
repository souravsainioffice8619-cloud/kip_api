import json
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

USERS_FILE = Path(__file__).parent / "data" / "users.json"
USERS_FILE.parent.mkdir(exist_ok=True)


def load_users():
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as file_obj:
        json.dump(users, file_obj, indent=2)


def add_user(username: str, password: str) -> bool:
    users = load_users()
    users[username] = generate_password_hash(password)
    save_users(users)
    return True


def verify_user(username: str, password: str) -> bool:
    users = load_users()
    if username not in users:
        return False
    stored = users[username]
    return check_password_hash(stored, password)


def list_users():
    return list(load_users().keys())


def get_user(username: str):
    """Return the stored password hash for a user, or None if not found."""
    users = load_users()
    return users.get(username)
