# Paranuara Challenge

## Installation Instructions
1. Install Anaconda 2018.12 Python 3.7 64-bit
2. Install Microsoft Visual C++ 2015 Redistributable Package `http://www.microsoft.com/en-us/download/default.aspx`
3. Clone the repo `https://github.com/griffonchan/paranuara.git` to a directory, i.e. `C:\paranuara`
4. `cd C:\paranuara`
5. Create a virtual environment `python -m venv venv`
6. Activate the virtual environment `.\venv\Scripts\activate.bat`
7. Install additional Python modules `pip install flask pytest`
8. Set environment variables:
<pre>
set FLASK_APP=paranuara/__init__.py
set FLASK_ENV=development
</pre>
9. Initialise the database `flask init-db`
10. Import companies.json and people.json into the database `flask import-json <path-to>companies.json <path-to>people.json`

## Run Pytest
1. `cd C:\paranuara`
2. Activate the virtual environment `.\venv\Scripts\activate.bat`
3. Set environment variable `set PYTHONPATH=.`
4. Run Pytest `pytest`

## Run Server
1. `cd C:\paranuara`
2. Activate the virtual environment `.\venv\Scripts\activate.bat`
3. Set environment variables:
<pre>
set FLASK_APP=paranuara/__init__.py
set FLASK_ENV=development
</pre>
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

