# Paranuara Challenge

## Installation Instructions
1. Install Anaconda 2018.12 Python 3.7 64-bit
2. Install Microsoft Visual C++ 2015 Redistributable Package `http://www.microsoft.com/en-us/download/default.aspx`
3. Create a directory, i.e. `C:\paranuara`
4. /paranuara/paranuara
5. /paranuara/tests
6. `cd C:\paranuara`
7. Create a virtual environment `python -m venv venv`
8. Activate the virtual environment `.\venv\Scripts\activate.bat`
9. Install additional Python modules `pip install flask pytest`
10. Set environment variables:
<code>
set FLASK_APP=paranuara/__init__.py
set FLASK_ENV=development
</code>
11. Initialise the database `flask init-db`
12. Import companies.json and people.json into the database `flask import-json <path-to>companies.json <path-to>people.json`

## Run Pytest
1. `cd C:\paranuara`
2. Set environment variable `set PYTHONPATH=.`
3. Run Pytest `pytest`

## Run Server
1. `cd C:\paranuara`
2. Activate the virtual environment `.\venv\Scripts\activate.bat`
3. Set environment variables:
<code>
set FLASK_APP=paranuara/__init__.py
set FLASK_ENV=development
</code>
4. Start server `flask run`

## Check Endpoints
1. List all employees of a given company:
`http://127.0.0.1:5000/company/<company_name>/employees`
E.g. `http://127.0.0.1:5000/company/jamnation/employees`
2. Given 2 people, show their information and list their friends in common which have brown eyes and are still alive:
`http://127.0.0.1:5000/common-friends?person1_name=<person1_name>&person2_name=<person2_name>`
E.g. `http://127.0.0.1:5000/common-friends?person1_name=Cote Booth&person2_name=Bonnie Bass`
3. Give a person, show their information and they favorite fruits and vegetables:
`http://127.0.0.1:5000/person/<person_name>`
E.g. `http://127.0.0.1:5000/person/Cote Booth`

