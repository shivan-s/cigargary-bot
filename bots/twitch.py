#!python3.8
# twitch.py - contains the main scripts for running the twitch bot
# pipenv - this will load .env variables

import logging
import os

from sqlalchemy import create_engine
from twitchio.ext import commands

# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    import sys

    sys.exit("DATABASE_URL not supplied.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TwitchBot(commands.Bot):
    """
    This will be our bot class
    """

    def __init__(self):
        super().__init__(
            token=os.getenv("ACCESS_TOKEN"),
            prefix=os.getenv("BOT_PREFIX"),
            initial_channels=[os.getenv("CHANNELS")],
        )

    async def event_ready(self):
        """
        Notify us the bot is logged and ready to go
        """
        logging.info(f"Logged in as {self.nick}")
        logging.info(f"Connected channels: {self.connected_channels}")

    async def event_message(self, message):
        """
        Overwriting the event_message, prevent echoing
        """
        if message.echo:
            return
        logging.info(f"{message.author}-{message.content}")
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """
        Say hello back to the user, assuming prefix is !
        e.g !hello
            hello user
        """
        if ctx.author.name == "vesklabs":
            await ctx.send(f"Veskkkkky!")
        else:
            await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command(name="commands")
    async def commands_(self, ctx: commands.Context):
        """
        Commands function
        e.g. !commands - prints all commands
        """
        list_commands = ctx.bot.commands
        if list_commands:
            await ctx.send(str([_ for _ in list_commands]))
        else:
            await ctx.send("No commands set")

    # TODO: Creat ability for owner of the chat + mod? to create commands
    # e.g. !commands <action> response

    @commands.command()
    async def stack(self, ctx: commands.Context):
        """
        Say hello back to the user, assuming prefix is !
        e.g !hello
            hello user
        """
        await ctx.send(
            f"{ctx.author.name} nuaudit uses a React Frontend, \
                FastAPI Backend, \
                and DynamoDB as a database"
        )
