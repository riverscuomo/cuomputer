# Cuomputer [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
The bot for my discord server.
https://discord.gg/mr-rivers-neighborhood
Obviously there are many tokens and secrets in this repo, so I'm not sure how useful it will be to anyone else. But, ideally, others could figure out how to help me improve it or make improvements themselves.

## Installation: set up venv on each computer
### Get path to python
where python

### Create the venv (use the name of the computer, such as G for desktop or 9 for laptop)
"C:\Users\aethe\AppData\Local\Programs\Python\Python310\python" -m venv .G
"C:\Users\Rivers Cuomo\AppData\Local\Programs\Python\Python310\python.exe" -m venv .9

### Activate the venv

### Install requirements

pip install -r requirements.txt

### Set environment variables in a .env file and in HEROKU
```
CLIENT_ID = 
CLIENT_SECRET = 
TOKEN = its another secret looking string from discord?
REPLICATE_API_TOKEN = 
OPENAI_API_KEY= 
GOOGLE_APPLICATION_CREDENTIALS= path to json file
GOOGLE_DRIVE_CREDFILE= path to json file
```

It seems I was able to set all credentials in heroku settings
```
firestore
gspread
```
except for google drive. I just couldn't figure out how to authorize from a creds json object rather than a path to an object.

## RUN
`py.main.py` in the top level directory

## Deploy to Heroku
This is probably just for me.

## Contribute
Most of the interesting code is in bot/on_message folder and bot/scripts folder.

in discord_bot. 
