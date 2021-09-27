# cigargary-bot
A bot for cigargary's twitch and discord? Below is all for developers and contributors

- Project for the project management for this app and also storing resources
- Issues for ideas and problems

## Plan

0. Write tests
1. Twitch bot that responds to commands like !project, !devops
2. Link twitch to discord to tell discord when cigargary is live?
3. Write tests

## Set up

1. Set up `pre-commit`
	```shell
	pip install pre-commit
	pre-commit install
	```
2. Set up `pipenv`
	```shell
	pip install pipenv
	pipenv lock

	# enter the shell to run code
	pipenv shell

	# or use pipenv run
	pipenv run blah
	```
2. Set up a twitch bot token (see below)
3. Run the bot
	```
	# from root of the project directory
	pipenv run start
	```

## [TWITCH] How to generate a token for the twitch bot

Documentation on twitchio library: https://pypi.org/project/twitchio/

1. Logout of current twitch account
2. Create a bot twitch account
3. Create a token: https://twitchtokengenerator.com/
4. Add tokens in an .env file
	```
	# .env
	ACCESS_TOKEN=oauth:<ACCESS TOKEN>
	CLIENT_ID=
	BOT_NICK=
	BOT_PREFIX=!
	CHANNELS=

	FRESH_TOKEN=
	```

## [DISCORD] Setting up discord bot

Resources:
- https://pypi.org/project/discord.py/
- https://realpython.com/how-to-make-a-discord-bot-python/
1. Create a bot account and get tokens (see resouces above) TODO: write 1. Create a bot account and get tokens (see resouces above) TODO: write1. Create a bot account and get tokens (see resouces above) TODO: write this
2. Add below to .env file
	``` # discord .env portion
	DISCORD_TOKEN=
	DISCORD_GUILD=cigargary
	```
3. TODO: Consoldate this with twitch .env files settings
