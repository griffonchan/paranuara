DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS friend;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS favourite_food;

CREATE TABLE company
(
    id   INTEGER NOT NULL PRIMARY KEY,
    name TEXT    NOT NULL
);

CREATE TABLE person
(
    id         INTEGER NOT NULL PRIMARY KEY,
    name       TEXT    NOT NULL,
    age        INTEGER,
    address    TEXT,
    phone      TEXT,
    eye_colour TEXT,
    has_died   BOOLEAN,
    company_id INTEGER,
    FOREIGN KEY (company_id) REFERENCES company (id)
);

CREATE TABLE friend
(
    person1_id INTEGER NOT NULL,
    person2_id INTEGER NOT NULL,
    FOREIGN KEY (person1_id) REFERENCES person (id),
    FOREIGN KEY (person2_id) REFERENCES person (id)
);

CREATE TABLE food
(
    id         INTEGER NOT NULL PRIMARY KEY,
    name       TEXT    NOT NULL,
    food_group INTEGER NOT NULL
);

CREATE TABLE favourite_food
(
    person_id INTEGER NOT NULL,
    food_id   INTEGER NOT NULL,
    FOREIGN KEY (person_id) REFERENCES person (id),
    FOREIGN KEY (food_id) REFERENCES food (id)
);

CREATE INDEX index_company ON company (UPPER(name));

CREATE INDEX index_person ON person (UPPER(name));

CREATE INDEX index_food ON food (UPPER(name));
