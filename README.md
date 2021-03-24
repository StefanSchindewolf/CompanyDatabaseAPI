# My first RESTful Python API (aka CompanyDatabaseAPI)

### Introduction
This is the first Python API I was writing. Actually it was part of a small programming challenge.

The API is hosting a company database which consists of some fields for each company.
The API has 4 methods:

1. GET a single company by company ID
2. GET a complete list of ALL companies
3. POST an update to an existing company (by ID)
4. POST a new record of company

The API is based on Flask, SQLAlchemy and Marshmallow.

### File descriptions
* **api_REST_001.py**: This is the core file containing the frontend
* **CompanyModel**: This is holding the Model and Schema definitions for company records
* **setup.py**: Keep the configuration out of the main API script, here is the application setup done
* **company.db**: An SQLite3 database, you may switch to any other DB if you like
* **create_database.py**: A small script to initialize and fill the SQLite DB with some test data
