# flask-restfulapi

![Static Badge](https://img.shields.io/badge/python-3.12.4-blue?style=plastic&logo=python&logoColor=white&link=https%3A%2F%2Fwww.python.org%2F)
 ![Static Badge](https://img.shields.io/badge/flask-3.0.3-blue?style=plastic&logo=flask&link=https%3A%2F%2Fflask.palletsprojects.com%2Fen%2F3.0.x%2F) ![Static Badge](https://img.shields.io/badge/licence-GPL--3.0-blue?style=plastic&logo=gpl&logoColor=white&cacheSeconds=https%3A%2F%2Fwww.gnu.org%2Flicenses%2Fgpl-3.0.en.html) ![Static Badge](https://img.shields.io/badge/PEP8-passing-green?style=plastic&logo=pep8&logoColor=green&link=https%3A%2F%2Fpeps.python.org%2Fpep-0008%2F) 

<img width="1089" alt="image" src="https://github.com/kennethrioja/flask-restfulapi/assets/59597207/a0b0c1e2-d9a2-45c7-9747-f9d8da0bc8f8">

## Overview

Using Flask (3.0.3) and SQLite, this RESTful API allows to receive and store logs. This has been done for the video game TSADK for the [Laboratoire d'Innovation Pédagogique](https://www.lip-unige.ch/).

Note: Each time this `<>` syntax is used, you should see it as something that you have chosen. `<UPPERCASEWORDS>` are for .env variables, and `<lowercasewords>` are for a string that you have chosen. For example, if I write `<APP_NAME>/api/v1/users` and on your side you have chosen in `APP_NAME = hello`, it means that at the end you should have `hello/api/v1/user`. Whereas, if you have `flask db migrate -m "<yourcommenthere>"`, you should run `flask db migrate -m "This is my comment or anything else I have chosen"`

## Features
- **Data storage**: Store data in database
- **Basic Authentication**: Secure routes with client secret credentials.
- **Token Authentication**: Generate and verify tokens for secure API access.
- **Role-Based Access Control (ACL)**: Restrict access based on user roles.

## Project Structure
```
flask-restfulapi/
├── app
│   ├── api
│   │   ├── auth
│   │   │   ├── auth.py
│   │   │   └── decorators.py
│   │   └── errors
│   │       └── handlers.py
│   ├── logs.py
│   ├── models.py
│   ├── users.py
│   └── utils.py
└── migrations
```

## Quick Start
- **Prerequisites**: Having installed `python3`
- **Setup**:
    - `python3 -m venv venv`
    - `source venv/bin/activate`
    - `pip install --upgrade pip`
    - `pip install --no-deps -r requirements.txt`.
    - Configure environment by first `mv .envcopy .env` and change the .env variables.
- **Run**: Run `flask run` to start the Flask server
- **Test**: Use `curl` to test the API endpoints, e.g., `curl -u <CLI_ID>:<CLI_PWD> -i http://localhost:5000/<APP_NAME>/api/v1/users`. Note: CLI_ID, CLI_PWD and APP_NAME are the variables you have chosen in `.env` file, for example, if I have CLI_ID=123, CLI_PWD=456, APP_NAME=myapp, you should test with `curl -u 123:456 -i http://localhost:5000/myapp/api/v1/users`
- **To reboot database**: Run `flask db downgrade base` then `flask db upgrade`

## Endpoints

Endpoint prefix will always begin by your `<APP_NAME>`.

### Authentication
- **Generate Token**: `<APP_NAME>/api/token` - Obtain a token using basic auth with admin IDs
- **Protected Resources**: Access secured resources with the generated token or basic auth.

## Usage

### Users

- **/v1/users [GET]**:
    - Accessible by admin
    - Returns a json formatted list of the users table
- **/v1/users [POST]**: 
    - Accessible by admin
    - Create user, client must provide with a json with `username` and `pwd` as keys. Example:
```
{
    "username": "john,
    "pwd": "johnpwd"
}
```
- **/v1/users/:user_id [GET]**: 
    - Accessible by admin
    - Returns a json formated list of user of the chosen id

### Logs

- **/v1/logs [GET]**:
    - Accessible by admin
    - Returns a json formatted list of the logs table
- **/v1/logs [POST]**: 
    - Accessible by admin and token authentification
    - Create log, client must provide with a json with `userID`, `timestamp`, `sequence`, `roomName`, `actionNature`, `actionType`, `userAnswer`, `userError` as keys. Example:
```
{
    "userID": 2,
    "timestamp": "2023-04-18T10:17.109Z",
    "sequence": 9,
    "roomName": "salleForet",
    "actionNature": "mettre_main",
    "actionType": "regionDeposer",
    "userAnswer": "if(none){win}else{loose}",
    "userError": "incorrect"
}
```
- **/v1/logs/:log_id [GET]**:
    - Accessible by admin
    - Returns a json formatted list of log of the chosen id

### Utils

- **/v1/utils/export/logs**: 
    - Accessible by admin
    - Returns a .csv of the logs table

- **v1/utils/token**:
    - Accessible by admin and user
    - Returns an authentification token, to use for `/v1/logs` POST

## Table Fields
- To create new or amend fields, modify the classes' fields under `models.py`, for example, you add : `newvar: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))`. Note: you max have ALTER TABLE errors, see https://blog.miguelgrinberg.com/post/fixing-alter-table-errors-with-flask-migrate-and-sqlite.
- (Optional) Create the specific error handling under the python file of the class.
- Run on the terminal `flask db migrate -m "<YOURCOMMENTHERE>"`, then `flask db upgrade`

## Misc
- **TOKEN_EXPIRATION_SEC**: Client can choose how many seconds the token should last, change value in `.env`
- **DATABASE_URL**: Client can choose another database, add path in `.env`

## License
- **GPL-3.0 License**: This project is licensed under the GPL-3.0 License.

## Resources
- https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- https://blog.miguelgrinberg.com/post/restful-authentication-with-flask

## Usage of ChatGPT
- Mild: I used it for the Class' fields to be more flexible, e.g., for the `create_log` and `export_log` methods.
