#
# Database access
#

from __future__ import print_function

import flask
import flask.cli
import click
import sqlite3
import json
import enum


@enum.unique
class FoodGroup(enum.IntEnum):
    FRUIT = 0
    VEGETABLE = 1


PERSON_JSON_FIELDS = ["index", "name", "age", "address", "phone", "eyeColor", "has_died", "company_id"]


def open_db():
    if "db_con" not in flask.g:
        flask.g.db_con = sqlite3.connect(flask.current_app.config["DATABASE"])

    return flask.g.db_con


def close_db(exc=None):
    db_con = flask.g.pop("db_con", None)

    if db_con is not None:
        db_con.close()


def init_db():
    db_con = open_db()

    with flask.current_app.open_resource("schema.sql") as f:
        db_con.executescript(f.read().decode("utf8"))


def get_all_employee_names(company_name):
    """
    Returns a list of employee names of the company with the given name.

    :param company_name: Then name of the company.
    :return: A list of employee names of the company
    """
    db_con = open_db()
    cursor = db_con.cursor()

    cursor.execute(
        """
            SELECT person.name
            FROM person, company
            WHERE UPPER(company.name) = UPPER(?) AND person.company_id = company.id AND person.has_died = FALSE
            ORDER BY person.name
        """,
        (company_name, )
    )

    return [r[0] for r in cursor.fetchall()]


def get_person(person_name):
    """
    Returns a dictionary of the name, age, address and phone of the person with the given name.
    Or None if no such person is found.

    :param person_name: The name of the person.
    :return: a dictionary of the name, age, address and phone of the person with the given name.
    Or None if no such person is found.
    """
    db_con = open_db()
    cursor = db_con.cursor()

    cursor.execute(
        "SELECT name, age, address, phone FROM person WHERE UPPER(name) = UPPER(?)",
        (person_name, )
    )

    row = cursor.fetchone()

    if row is None:
        person = None
    else:
        person = dict(zip(["name", "age", "address", "phone"], row))

    return person


def get_common_friends(person1_name, person2_name):
    """
    Returns a list of common friends (with brown eyes and alive) between the two persons.

    :param person1_name: The name of the first person.
    :param person2_name: The name of the second person.
    :return: a list of common friends (with brown eyes and alive) between the two persons.
    """
    db_con = open_db()
    cursor = db_con.cursor()

    cursor.execute(
        """
            SELECT person.name FROM person
            WHERE 
            (
                person.eye_colour = "brown"
                AND
                person.has_died = FALSE
                AND
                person.id IN
                (
                    SELECT friend.person2_id
                    FROM friend
                    WHERE friend.person1_id = (SELECT person.id FROM person WHERE UPPER(person.name) = UPPER(?))
                    INTERSECT
                    SELECT friend.person2_id FROM friend
                    WHERE friend.person1_id = (SELECT person.id FROM person WHERE UPPER(person.name) = UPPER(?))
                )
            )
            ORDER BY person.name
        """,
        (person1_name, person2_name)
    )

    return [r[0] for r in cursor.fetchall()]


def get_favourite_food(person_name, food_group):
    """
    Returns a list of favourite food in the given food group of the person.

    :param person_name: The name of the person.
    :param food_group: The food group to return
    :return: a list of favourite food in the given food group of the person.
    """
    assert isinstance(food_group, FoodGroup)

    db_con = open_db()
    cursor = db_con.cursor()

    cursor.execute(
        """
            SELECT food.name FROM food
            WHERE
            (
                food.food_group = ?
                AND
                food.id IN 
                (
                    SELECT food_id FROM favourite_food
                    WHERE person_id = (SELECT person.id FROM person WHERE UPPER(person.name) = UPPER(?))
                )
            )
            ORDER BY food.name
        """,
        (food_group, person_name)
    )

    return [r[0] for r in cursor.fetchall()]


@click.command("init-db")
@flask.cli.with_appcontext
def init_db_command():
    """
    Initialises the database.
    """
    init_db()


@click.command("import-json")
@click.argument("companies_json", type=click.File("rb"))
@click.argument("people_json", type=click.File("rb"))
@flask.cli.with_appcontext
def import_json_command(companies_json, people_json):
    """
    Imports companies.json and people.json into the database.

    :param companies_json: The path to companies.json
    :param people_json: The path to people.json
    """
    db_con = open_db()
    cursor = db_con.cursor()

    try:
        import_fruits_vegetables(cursor)
        import_companies_json(cursor, companies_json)
        import_people_json(cursor, people_json)
    except (sqlite3.OperationalError, json.JSONDecodeError, ValueError) as e:
        raise e
    else:
        db_con.commit()


def import_fruits_vegetables(cursor):
    """
    Import fruits.txt and vegetables.txt into the database.

    Both fruits.txt and vegetables.txt contain names of fruit and vegetable respectively,
    each on its own line.

    :param cursor: The database cursor
    """
    fruits = load_fruits()
    num_fruits = len(fruits)
    vegetables = load_vegetables()

    cursor.executemany(
        f"INSERT INTO food (id, name, food_group) VALUES (?, ?, {FoodGroup.FRUIT})",
        zip(range(num_fruits), fruits)
    )
    cursor.executemany(
        f"INSERT INTO food (id, name, food_group) VALUES (?, ?, {FoodGroup.VEGETABLE})",
        zip(range(num_fruits, num_fruits + len(vegetables)), vegetables)
    )


def load_fruits():
    with flask.current_app.open_resource("fruits.txt", "r") as f:
        fruits = set(filter(lambda i: len(i) > 0, [l.strip() for l in f]))

    return fruits


def load_vegetables():
    with flask.current_app.open_resource("vegetables.txt", "r") as f:
        vegetables = set(filter(lambda i: len(i) > 0, [l.strip() for l in f]))

    return vegetables


def import_companies_json(cursor, companies_json):
    """
    Imports companies.json into the database.

    :param cursor: The database cursor
    :param companies_json: The path to companies.json
    """
    companies = json.load(companies_json)

    cursor.executemany(
        "INSERT INTO company (id, name) VALUES (?, ?)",
        [(c["index"], c["company"]) for c in companies if "index" in c and "company" in c]
    )


def check_person_json(person):
    """
    Returns True if the person (loaded from people.json) has all the essential fields.

    :param person: The person dictionary.
    :return: True if the person (loaded from people.json) has all the essential fields.
    """
    return all([f in person for f in PERSON_JSON_FIELDS])


def json_to_sql_person(person_json):
    """
    Returns person dictionary imported from people.json as a tuple with fields used
    by the database.

    :param person_json: The person dictionary imported from people.json
    :return: The person tuple
    """
    return (
        person_json["index"],
        person_json["name"],
        person_json["age"],
        person_json["address"],
        person_json["phone"],
        person_json["eyeColor"].lower() if person_json["eyeColor"] is not None else None,
        person_json["has_died"],
        person_json["company_id"]
    )


def import_people_json(cursor, people_json):
    """
    Imports people.json into the database.

    :param cursor: The database cursor
    :param people_json: The path to people.json
    """
    people = json.load(people_json)
    people_sql = list()

    for p in people:
        if not check_person_json(p):
            raise ValueError(f"{p} failed check.")
        
        people_sql.append(json_to_sql_person(p))

    cursor.executemany(
        """
            INSERT INTO person (id, name, age, address, phone, eye_colour, has_died, company_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        people_sql
    )

    for p in people:
        cursor.executemany(
            "INSERT INTO friend (person1_id, person2_id) VALUES (?, ?)",
            [(p["index"], f["index"]) for f in p["friends"] if "index" in f]
        )

        if "favouriteFood" in p:
            cursor.executemany(
                """
                INSERT INTO favourite_food (person_id, food_id)
                VALUES (?, (SELECT id FROM food WHERE UPPER(name) = UPPER(?)))
                """,
                zip([p["index"]] * len(p["favouriteFood"]), p["favouriteFood"])
            )


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_json_command)
