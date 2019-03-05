#
# Server
#

from __future__ import print_function

import flask
import os


def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("../config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    @app.route("/company/<company_name>/employees", methods=["GET"])
    def handle_employees(company_name):
        return flask.jsonify(db.get_all_employee_names(company_name))

    @app.route("/common-friends", methods=["GET"])
    def handle_common_friends():
        person1_name = flask.request.args.get("person1_name")
        person2_name = flask.request.args.get("person2_name")

        person1 = db.get_person(person1_name)
        person2 = db.get_person(person2_name)
        common_friends = db.get_common_friends(person1_name, person2_name)

        return flask.jsonify(
            {
                "person1": person1,
                "person2": person2,
                "common_friends": common_friends
            }
        )

    @app.route("/person/<person_name>", methods=["GET"])
    def handle_person(person_name):
        person = db.get_person(person_name)
        fruits = db.get_favourite_food(person_name, db.FoodGroup.FRUIT)
        vegetables = db.get_favourite_food(person_name, db.FoodGroup.VEGETABLE)

        if person is None:
            ret = None
        else:
            ret = {
                "username": person["name"],
                "age": str(person["age"]),
                "fruits": fruits,
                "vegetables": vegetables
            }

        return flask.jsonify(ret)

    return app
