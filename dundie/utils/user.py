import hashlib
import hmac

SECRET_KEY = "dundie-secret-key-security"


def generate_simple_password(size=8):
    """Generation of simple random passwords.
    [a-z][A-Z][0-9]
    """
    from random import sample
    from string import ascii_letters, digits

    password = sample(ascii_letters + digits, size)
    return "".join(password)


def get_password_hash(password: str) -> str:
    """Generate SHA256 HMAC hash from raw password."""
    return hmac.new(
        SECRET_KEY.encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    if not hashed_password or not plain_password:
        return False
    return hmac.compare_digest(get_password_hash(plain_password), hashed_password)
