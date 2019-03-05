#
# pytest
#


def test_employees(client):
    response = client.get("/company/CompanyX/employees")
    assert response.get_json() == list()

    response = client.get("/company/Company0/employees")
    assert response.get_json() == ["Person0"]

    response = client.get("/company/CoMpAnY1/employees")
    assert response.get_json() == ["Person1"]


def test_common_friends(client):
    response = client.get("/common-friends?person1_name=Person0&person2_name=Person1")
    assert response.get_json() == {
        "common_friends": [],
        "person1": {"address": "Address0", "age": 10, "name": "Person0", "phone": "Phone0"},
        "person2": {"address": "Address1", "age": 11, "name": "Person1", "phone": "Phone1"}
    }

    response = client.get("/common-friends?person1_name=PERson0&person2_name=perSON1")
    assert response.get_json() == {
        "common_friends": [],
        "person1": {"address": "Address0", "age": 10, "name": "Person0", "phone": "Phone0"},
        "person2": {"address": "Address1", "age": 11, "name": "Person1", "phone": "Phone1"}
    }

    response = client.get("/common-friends?person1_name=Person1&person2_name=Person2")
    assert response.get_json() == {
        "common_friends": ["Person3"],
        "person1": {"address": "Address1", "age": 11, "name": "Person1", "phone": "Phone1"},
        "person2": {"address": "Address2", "age": 12, "name": "Person2", "phone": "Phone2"}
    }


def test_person(client):
    response = client.get("/person/PersonX")
    assert response.get_json() is None

    response = client.get("/person/Person0")
    assert response.get_json() == {
        "username": "Person0",
        "age": "10",
        "fruits": ["Food0"],
        "vegetables": []
    }

    response = client.get("/person/perSON0")
    assert response.get_json() == {
        "username": "Person0",
        "age": "10",
        "fruits": ["Food0"],
        "vegetables": []
    }

    response = client.get("/person/Person2")
    assert response.get_json() == {
        "username": "Person2",
        "age": "12",
        "fruits": ["Food2", "Food4"],
        "vegetables": ["Food3"]
    }
