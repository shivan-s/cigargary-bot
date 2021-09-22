#!python3.8
# twitch.py - contains the main scripts for running the twitch bot
# pipenv - this will load .env variables

import os
import logging

from twitchio.ext import commands

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
        print(message.content)
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

    # TODO: Creat ability for owner of the chat + mod? to create commands
    # e.g. !command <action> response
