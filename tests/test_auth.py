import pytest

from dundie.database import add_person, authenticate_user, connect
from dundie.utils.user import get_password_hash, verify_password


@pytest.mark.unit
def test_password_hashing():
    raw_pwd = "secretpassword123"
    hashed = get_password_hash(raw_pwd)
    assert hashed != raw_pwd
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


@pytest.mark.unit
def test_authenticate_user():
    db = connect()
    pk = "admin@dundlermifflin.com"
    data = {"role": "Manager", "dept": "Management", "name": "Admin User"}
    add_person(db, pk, data)

    # Em add_person, a senha aleatoria criada e salva com hash
    hashed_pwd = db["users"][pk]["password"]
    assert verify_password("wrong", hashed_pwd) is False


@pytest.mark.unit
def test_authenticate_user_function():
    db = connect()
    pk = "employee@dundler.com"
    db["users"][pk] = {"password": get_password_hash("mysecret")}

    assert authenticate_user(db, pk, "mysecret") is True
    assert authenticate_user(db, pk, "wrong") is False
    assert (
        authenticate_user(db, "nonexistent@dundler.com", "mysecret") is False
    )
