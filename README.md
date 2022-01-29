# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

We will be using external library called Requests (https://docs.python-requests.org/en/master/) to make the API requests and interpret the JSON response. You need to add the requests library to your list of poetry dependencies in pyproject.toml:
```bash
$ poetry add requests
```

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Create a Trello account and API key

We're going to be using Trello's API to fetch and save to-do tasks. 
1. Create an account by visiting this link https://trello.com/signup in you're favourite browser.
2. Generate an API Key and get your token
3. Explore the Trello's API thru here https://developer.atlassian.com/cloud/trello/rest/api-group-actions/ using POSTMAN.
4. Update add the API_KEY and API_TOKEN to the `.env` file in your project folder.
5. On https://trello.com/ create a new board and give a title (e.g. todo_app).  
6. Once you have created your board you well need the BOARD_ID. To get the Board ID you need to use this API in POSTMAN https://api.trello.com/1/members/me/boards?fields=name,url&key={apiKey}&token={apiToken}
7. Update the BOARD_ID to the `.env` file in your project folder
