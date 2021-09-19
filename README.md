# cigargary-bot
A bot for cigargary's twtich and discord?

## Plan

1. Twitch bot that responds to commands like !project, !devops
2. Link twitch to discord to tell discord when cigargary is live?

## Set up

1. Set up pre-commit
```
pip install pre-commit
pre-commit install
```
2. Set up a twitch bot token (see below)

## How to generate a token for the twitch bot

Documentation on twitchio library: https://pypi.org/project/twitchio/

1. Logout of account
2. Create a bot account
3. Create a token: https://twitchtokengenerator.com/
4. Add tokens in an .env file
	```
	# .env

	ACCESS_TOKEN=
	FRESH_TOKEN=
	CLIENT_ID=
	```
