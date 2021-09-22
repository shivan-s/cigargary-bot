# discord.py - contains bot for discord

import discord
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class DiscordBot:
    pass


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISORD_GUILD")

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    logger.info(
        f"{client.user} is connected to the following guild:\n {guild.name} (id: %{guild.id})"
    )


client.run(TOKEN)
