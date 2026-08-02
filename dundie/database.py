import json
from datetime import datetime

from dundie.settings import EMAIL_FROM
from dundie.utils.email import check_valid_email, send_email
from dundie.utils.user import (
    generate_simple_password,
    get_password_hash,
    verify_password,
)

EMPTY_DB = {"people": {}, "balance": {}, "moviment": {}, "users": {}}


def connect() -> dict:
    """Connect to the database, returns dict data."""
    from dundie import settings
    try:
        with open(settings.DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return json.loads(json.dumps(EMPTY_DB))


def commit(db):
    """Save db back to the database file."""
    from dundie import settings
    if db.keys() != EMPTY_DB.keys():
        raise RuntimeError("Database schema is invalid.")
    with open(settings.DATABASE_PATH, "w") as database_file:
        database_file.write(json.dumps(db, indent=4))


def add_person(db, pk, data):
    """Save person data to database

    - Email is unique (resolved by dictionary has table)
    - Set initial balance (manager = 100, others = 500)
    - Generate a password if user is new and send_email
    """
    if not check_valid_email(pk):
        raise ValueError(f"{pk} is not valid email address.")
    table = db["people"]
    person = table.get(pk, {})
    created = not bool(person)
    person.update(data)
    table[pk] = person
    if created:
        set_initial_balance(db, pk, person)
        password = set_initial_password(db, pk)
        send_email(EMAIL_FROM, pk, "Your dundie password", password)
        # TODO: Encrypt and send only link not password
    return person, created


def set_initial_password(db, pk):
    """Generate and saves hashed password"""
    db["users"].setdefault(pk, {})
    raw_password = generate_simple_password(8)
    db["users"][pk]["password"] = get_password_hash(raw_password)
    return raw_password


def authenticate_user(db, email, password) -> bool:
    """Authenticate user with email and password."""
    user = db.get("users", {}).get(email)
    if not user:
        return False
    return verify_password(password, user.get("password", ""))


def set_initial_balance(db, pk, person):
    """Add movement and set initial balance"""
    value = 100 if person["role"] == "Manager" else 500
    add_movement(db, pk, value)


def add_movement(db, pk, value, actor="system"):
    """Add moviment and update balance"""
    movements = db["moviment"].setdefault(pk, [])
    movements.append(
        {"date": datetime.now().isoformat(), "actor": actor, "value": value}
    )
    db["balance"][pk] = sum([item["value"] for item in movements])
