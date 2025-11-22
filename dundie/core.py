"""Core module of dundie"""

from csv import reader

from dundie.database import add_person, commit, connect
from dundie.utils.log import get_logger

log = get_logger()


def load(filepath):
    """Loads data from filepath to the database.

    >>> len(load("assets/sample_data.csv"))
    2
    """
    try:
        csv_data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

    db = connect()
    people = []
    headers = ["name", "dept", "role", "e-mail"]
    for line in csv_data:
        person_date = dict(zip(headers, [item.strip() for item in line]))
        pk = person_date.pop("e-mail")
        person, created = add_person(db, pk, person_date)

        return_data = person.copy()
        return_data["created"] = created
        return_data["e-mail"] = pk
        people.append(return_data)

    commit(db)
    return people
