INSERT INTO company (id, name)
VALUES
    (0, 'Company0'),
    (1, 'Company1'),
    (2, 'Company2');

INSERT INTO person (id, name, age, address, phone, eye_colour, has_died, company_id)
VALUES
    (0, 'Person0', 10, 'Address0', 'Phone0', 'red', FALSE, 0),
    (1, 'Person1', 11, 'Address1', 'Phone1', 'green', FALSE, 1),
    (2, 'Person2', 12, 'Address2', 'Phone2', 'blue', FALSE, 2),
    (3, 'Person3', 13, 'Address3', 'Phone3', 'brown', FALSE, NULL),
    (4, 'Person4', 14, 'Address4', 'Phone4', 'brown', TRUE, NULL);

INSERT INTO friend (person1_id, person2_id)
VALUES
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4);

INSERT INTO food (id, name, food_group)
VALUES
    (0, 'Food0', 0),
    (1, 'Food1', 1),
    (2, 'Food2', 0),
    (3, 'Food3', 1),
    (4, 'Food4', 0),
    (5, 'Food5', 1);

INSERT INTO favourite_food (person_id, food_id)
VALUES
    (0, 0),
    (1, 1),
    (2, 2),
    (2, 3),
    (2, 4);
