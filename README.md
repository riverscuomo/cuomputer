# Cuomputer [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

The bot for my discord server.
<https://discord.gg/mr-rivers-neighborhood>

Obviously there are many missing tokens and secrets in this repo, so I'm not sure how useful it will be to anyone else. But, ideally, others could figure out how to help me improve it or make improvements themselves.

## This is where I set up the bot

<https://discord.com/developers>

   <https://discord.com/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&scope=bot&permissions=PERMISSIONS_INT>
   8 = admin

## Installation: set up venv on each computer

### Get path to python

where python

### Create the venv (use the name of the computer, such as G for desktop or 9 for laptop)

"C:\Users\aethe\AppData\Local\Programs\Python\Python310\python" -m venv .G
"C:\Users\Rivers Cuomo\AppData\Local\Programs\Python\Python310\python.exe" -m venv .9

### Activate the venv

### Install requirements

pip install -r requirements.txt

### Set up path-related environment variables in the root directory terminal

(this one is necessary to run the tests from the root directory with pytest)

```bash
PYTHONPATH=%cd%
```

### Set environment variables in both a .env file and in HEROKU

#### Discord

```
CLIENT_ID = 
CLIENT_SECRET = 
TOKEN = its another secret looking string from discord?
```

#### Other Apis

```
REPLICATE_API_TOKEN = 
OPENAI_API_KEY= 
```

### Other Credentials

#### `gspreader` [service account]

Heroku.Settings.configVariables: `GSPREADER_GOOGLE_CREDS` json object . Gspreader uses the `gspreader.json` method to get the creds.
.env: it still has access to a file using the `gspreader.path` method to `GSPREADER_GOOGLE_CREDS_PATH`=`C:\RC Dropbox\Rivers Cuomo\Apps\credentials\rctweetcleaner-3d2160633739.json`

#### `firestore` and `google drive` [service account]

Heroku.Settings.configVariables: `GOOGLE_CREDENTIALS` json object.
.env: I think it's just authorizing itself by using the `riverscuomo-8cc6c....json` cred file in the top level of the project. This file is not commited to git/github but it is avaialable in the directory via dropbox.

## RUN

`py.main.py` in the top level directory

## Debug

press play in the debugger in vscode on the `main.py` file

## Deploy to Heroku

This should automatically deploy to Heroku now when you `git push origin main`

## Unit Tests

Unit tests can be found in the folder `tests/unit_tests`, and they can be executed with the following command (from the repository root directory):

```bash
PYTHONPATH=. pytest tests/unit_tests
```

If you do not have `pytest` installed, refer to <https://docs.pytest.org/en/stable/getting-started.html>

## Contribute

Most of the interesting code is in bot/on_message folder and bot/scripts folder.

in discord_bot.
