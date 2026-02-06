import json
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = Path(__file__).parent / 'data' / 'users.json'
USERS_FILE.parent.mkdir(exist_ok=True)


def load_users():
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_users(users: dict):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)


def add_user(username: str, password: str):
    users = load_users()
    users[username] = generate_password_hash(password)
    save_users(users)


def verify_user(username: str, password: str) -> bool:
    users = load_users()
    if username not in users:
        return False
    stored = users[username]
    # stored is a hash
    return check_password_hash(stored, password)


def list_users():
    return list(load_users().keys())

def get_user(username: str):
    """Returns the stored password hash for a user, or None if not found."""
    users = load_users()
    return users.get(username)