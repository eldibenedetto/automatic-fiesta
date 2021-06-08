# The Atlantic Subscriptions API

The Subscriptions API is a RESTful Django application used to create and list Customer resources.
## Manual Installation

### Clone Repo

```bash
git clone https://github.com/eldibenedetto/automatic-fiesta.git && cd automatic-fiesta
```
This project was developed using [Poetry](https://github.com/python-poetry/poetry), a python package manager. If you'd like to use poetry you can install it using the command below. (You can install packages manually in your ```virtualenv``` using the pyproject.toml file as a reference)
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
PATH="${PATH}:/root/.local/bin"
poetry install
```
*** You may need to adjust the pyproject.toml file to use the python environment configured on your machine. Also ```poetry env use python3.__``` can help configure the python environment correctly.

### Make Migrations
```bash
poetry run python3 manage.py migrate
```

## Database Schema
![alt text](https://github.com/eldibenedetto/upgraded-barnacle/blob/main/Screen%20Shot%202021-06-07%20at%2011.59.40%20PM.png?raw=true)

## Getting Started
### Start Server
```bash
poetry run python3 manage.py runserver
```
or 
```bash
docker-compose build
docker-compose up -d
```

base url = ```http://127.0.0.1/api/v1/```

### List

method = ```GET```

endpoint = ```subscriptions/```

params = ```None```

response:
```python
[
    {
        "id": str,
        "first_name": str,
        "last_name": str,
        "address_1": str,
        "address_2": str,
        "city": str,
        "state": str,
        "postal_code": str,
        "subscription": {
            "id": str,
            "plan_name": str,
            "price": str
        },
        "gifts": [
            {
                "id": str,
                "plan_name": str,
                "price": "4999",
                "recipient_email": str
            },
            {
                "id": str,
                "plan_name": str,
                "price": str,
                "recipient_email": str
            }
        ]
    },
   ...
]
```
### Create
method = ```POST```

endpoint = ```subscriptions/```

body:
```python
## Valid JSON
    {
        "id": str,
        "first_name": str,
        "last_name": str,
        "address_1": str,
        "address_2": str,
        "city": str,
        "state": str,
        "postal_code": str,
        "subscription": {  ## This Key is Required. Based on the assumption that a Customer must have some kind of subscription
            "id": str,
            "plan_name": str,
            "price": str
        },
        "gifts": [
            {
                "id": str,
                "plan_name": str,
                "price": "4999",
                "recipient_email": str
            },
            {
                "id": str,
                "plan_name": str,
                "price": str,
                "recipient_email": str
            }
        ]
    }
```

response: Same as Above (Newly Created Customer)

## Stretch Goals
This I would've liked to add with more time:
```
1) Add Retrieve/Update Endpoints
2) Organized tests into a test suite i.e.
└── subscriptions
    └── tests
        ├── __init__.py
        ├── test_models.py
3) Normally I would've broken the tests out into separate test cases.
4) Add admindocs to each function i.e.
def create_subscription(self, sub_data, custy):
  """
    Creates Instance of a Subscription
    """
		return Subscription.objects.create(customer_id=custy, **sub_data)
5) Secrets Management i.e. using AWS Secret Manager to manage django secret key
6) Added more irregularity and edge case handling.
7) If I had more time I would normally develop on a development branch and merge to master after testing the code extensively.
```
