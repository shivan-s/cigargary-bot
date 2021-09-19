#!python3.8
# bot.py - contains the main scripts for running the twitch bot

import os

from twitchio.ext import commands


class Bot(commands.Bot):
    """
    This will be our bot class
    """

    def __init__(self):
        super().__init__(
            token=os.environ.get("ACCESS_TOKEN"),
            prefix=os.environ.get("BOT_PREFIX"),
            initial_channel=[os.environ.get("CHANNELS")],
        )

    async def event_ready(self):
        """
        Notify us the bot is logged and ready to go
        """
        print(f"Logged in as {self.nick}")

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
        await ctx.send(f"Hello {ctx.author.name}!")
