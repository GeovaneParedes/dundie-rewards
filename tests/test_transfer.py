import pytest

from dundie.database import (
    add_person,
    connect,
    get_balance,
    get_movements,
    transfer_points,
)
from dundie.utils.user import get_password_hash


@pytest.mark.unit
def test_get_balance_and_movements():
    db = connect()
    pk = "pam@dundler.com"
    data = {"role": "Receptionist", "dept": "Admin", "name": "Pam Beesly"}
    add_person(db, pk, data)

    balance = get_balance(db, pk)
    assert balance == 500

    movements = get_movements(db, pk)
    assert len(movements) == 1
    assert movements[0]["value"] == 500


@pytest.mark.unit
def test_transfer_points_success():
    db = connect()
    sender_pk = "dwight@dundler.com"
    receiver_pk = "jim@dundler.com"

    add_person(
        db, sender_pk, {"role": "Salesman", "dept": "Sales", "name": "Dwight"}
    )
    add_person(
        db, receiver_pk, {"role": "Salesman", "dept": "Sales", "name": "Jim"}
    )

    db["users"][sender_pk] = {"password": get_password_hash("dwight123")}

    # Dwight tem 500 pontos iniciais e transfere 150 para Jim (que tem 500)
    success, msg = transfer_points(
        db, sender_pk, "dwight123", receiver_pk, 150
    )
    assert success is True
    assert get_balance(db, sender_pk) == 350
    assert get_balance(db, receiver_pk) == 650


@pytest.mark.unit
def test_transfer_points_insufficient_balance():
    db = connect()
    sender_pk = "michael@dundler.com"
    receiver_pk = "ryan@dundler.com"

    add_person(
        db,
        sender_pk,
        {"role": "Manager", "dept": "Management", "name": "Michael"},
    )
    add_person(
        db, receiver_pk, {"role": "Temp", "dept": "Sales", "name": "Ryan"}
    )

    db["users"][sender_pk] = {"password": get_password_hash("bestboss")}

    # Michael tem 100 pontos (Manager) e tenta transferir 200
    success, msg = transfer_points(db, sender_pk, "bestboss", receiver_pk, 200)
    assert success is False
    assert "Insufficient balance" in msg
    assert get_balance(db, sender_pk) == 100


@pytest.mark.unit
def test_transfer_points_invalid_password():
    db = connect()
    sender_pk = "kevin@dundler.com"
    receiver_pk = "oscar@dundler.com"

    add_person(
        db,
        sender_pk,
        {"role": "Accountant", "dept": "Accounting", "name": "Kevin"},
    )
    add_person(
        db,
        receiver_pk,
        {"role": "Accountant", "dept": "Accounting", "name": "Oscar"},
    )

    db["users"][sender_pk] = {"password": get_password_hash("correctpass")}

    success, msg = transfer_points(db, sender_pk, "wrongpass", receiver_pk, 50)
    assert success is False
    assert "Invalid credentials" in msg
