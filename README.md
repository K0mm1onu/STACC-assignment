# Solution to STACC's Data Engineer Test Task

Author: Argo Kamenik

**Django application serving a REST API which provides data from the Iris dataset in JSON format**

### Stack:
- Web service: Django + Django rest_framework
- Database: PostgreSQL (using Django's built-in ORM)
- Docker compose for running the application and database containers

## Installations instructions
...

## API usage guide

### GET /flowers
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

