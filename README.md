# Telegram invites services

## Introduction
We use Airtable CMS to track the invitations for FED Telegram channel.
If an invited user joined the channel we have to update the status of invitation on Airtable.

This is a tiny python script to automaticaly check if some pending invites are joined in FED Telegram channel.
If a pending invitation has joined the Telegram group we update the status to "Joined" on Airtable.

The script use a scheduler to exec the check every 5 minutes.


## Getting started

#### Clone the repository

#### Create the env file
Create the `.env` file in the directory root using `.env.example`.

#### Add the telegram session file
Copy inside the directory root the telegram session file.

#### Build the docker image
```sh
docker build -t fed-telegram-invites .
```

#### Run the docker image
```sh
docker run --env-file .env  fed-telegram-invites:latest
```

## Development
Requirements:
- python3
- pip
- pipenv

#### Install dependecies
```sh
pipenv install
```

#### Run script
```sh
pipenv run python3 main.py
```