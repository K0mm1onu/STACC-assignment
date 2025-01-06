# Solution to STACC's Data Engineer Test Task

Author: Argo Kamenik

**Django application serving a REST API which provides data from the Iris dataset in JSON format**

No tests were implemented but I'd use a combination of end-to-end tests on all of the API endpoints (with a test set in Postman or Insomnia for example) and unit tests on operations with data (insertion, deletion, updates etc.).

Data in the database is initialized from the Iris dataset and outlying flower specimen (those that have at least one measurement exceeding 3 standard deviations from the species' mean) are removed. The data model separates species from a single flower specimen with a many-to-one relationship to have the DB in normal form and to future-proof the solution in case the species get other properties other than their name.

The REST API enables reading all of the flower specimen in the database and adding new ones.

### Stack:
- Web service: Django + Django rest_framework
- Database: PostgreSQL (using Django's built-in ORM)
- Docker compose for running the application and database containers

## Installation instructions

1. Clone the repository and navigate to its root folder
2. Run `docker-compose up -d --build`
3. Inside the `web` container with `docker exec` run
    - `python manage.py makemigrations`
    - `python manage.py migrate` \
    This will run Django's database migration scripts to initalize the application's DB schema
4. Restart the docker-compose setup:
    - `docker-compose down`
    - `docker-compose up -d --build`
5. Make the `GET /init-data` request as shown in the API usage guide (by default this setup run on `localhost:8080`). \
This request makes the application delete all existing data and download the Iris dataset


## API usage guide

### GET /init-data

Delete all data from the database, download the dataset, remove outliers and insert the data into the database.

Body: none\
Params: none

**EXAMPLE**
Request:
```
GET /init-data
```

Response:
```
204 NO CONTENT
```

### GET /flowers

Get all flower specimens.

Body: none\
Parameters: none

**EXAMPLE:**\
Request:
```
GET /flowers
```

Response:
```json
[
	{
		"id": 1798,
		"species": {
			"name": "setosa"
		},
		"sepalLength": 6.5,
		"sepalWidth": 3.0,
		"petalLength": 5.2,
		"petalWidth": 2.0
	},
	{
		"id": 1799,
		"species": {
			"name": "virginica"
		},
		"sepalLength": 6.2,
		"sepalWidth": 3.4,
		"petalLength": 5.4,
		"petalWidth": 2.3
	}
]
```

### POST /flowers
Body: JSON
Parameters: none

**EXAMPLE:** \
Request: 

```
POST /flowers
```

Request body:
```json
{
    "species": "setosa",
    "sepalLength": 6.901,
    "sepalWidth": 4.2069,
    "petalLength": 1.4,
    "petalWidth": 0.2
}
```
Response:
```
204 CREATED
```

