# My first RESTful Python API (aka CompanyDatabaseAPI)
(Thursday, 18th March 2021 - Wednesday, 24th March 2021 // remote work // Programming challenge)

## Introduction
This is the first Python API I was writing. Actually it was part of a small programming challenge.

The API is hosting a company database which consists of some fields for each company.
The API has 4 methods:

1. GET a single company by company ID
2. GET a complete list of ALL companies
3. POST an update to an existing company (by ID)
4. POST a new record of company

The API is based on Flask, SQLAlchemy and Marshmallow.

## File descriptions
Here the list of files in this project. Files which are meant for execution are highlighted with "Usage". All other files are invoked on the fly.
* **api_REST_001.py**: This is the core file containing the frontend (**Usage**: `python3 api_REST_001.py`)
* **CompanyModel**: This is holding the Model and Schema definitions for company records
* **setup.py**: Keep the configuration out of the main API script, here is the application setup done
* **company.db**: An SQLite3 database, you may switch to any other DB if you like (this file is optiona, the create_database script will remove it anyways)
* **create_database.py**: A small script to initialize and fill the SQLite DB with some test data (**Usage**: `python3 create_database.py`)

## How to use
Actually by downloading the files you can apply them on your machine or in a Docker image and run the API server script.
The create_database script is executed in the shell manually.


## Resources
I did not invent this on my own for sure. Merely I worked through a great tutorial which you can find here: https://realpython.com/flask-connexion-rest-api-part-2/#database-interaction. [Part 3](https://realpython.com/flask-connexion-rest-api-part-3/#update-response-json) includes the part about dynamically adding new columns (or fields) to your schema.

How to deploy using Docker is explained [here](https://dev.to/swarnimwalavalkar/build-and-deploy-a-rest-api-microservice-with-python-flask-and-docker-5c2d), but actually this is pretty straightforward.

In addition I used the standard documentation of the included modules:
* https://github.com/marshmallow-code/flask-marshmallow
* https://www.sqlalchemy.org/
