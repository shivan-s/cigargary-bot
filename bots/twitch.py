#!python3.8
# -*- coding: utf-8 -*-
# twitch.py - contains the main scripts for running the twitch bot
# pipenv - this will load .env variables

import logging
import os
import sys
import random
import asyncio

from sqlalchemy import create_engine
from twitchio.ext import commands

# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:

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
        !hello
            says hello to the user
        """
        if ctx.author.name == "vesklabs":
            await ctx.send(f"Veskkkkky!")
        else:
            await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command(name="commands")
    async def commands_(self, ctx: commands.Context):
        """
        !commands
            prints a list of commands
        """
        list_commands = [
            f"!{str(command)}" for command in ctx.bot.commands.keys()
        ]

        if list_commands:
            await ctx.send(", ".join(list_commands))
        else:
            await ctx.send("No commands set")

    # TODO: Creat ability for owner of the chat + mod? to create commands
    # e.g. !commands <action> response

    @commands.command()
    async def stack(self, ctx: commands.Context):
        """
        What is the stack?
        """
        await ctx.send(
            f"{ctx.author.name} nuaudit uses a React Frontend, \
                FastAPI Backend, \
                and DynamoDB as a database"
        )

    @commands.command()
    async def roll(self, ctx: commands.Context):

        await ctx.send(
            f"{ctx.author.name} rolls {random.randint(1,100)} (1-100)"
        )

    @commands.command()
    async def project(self, ctx: commands.Context):
        """
        !project
            explains the project
        """

        await ctx.send(
            f"{ctx.author.name} @cigargary is working on \
                    https://www.nuaudit.com. A SaaS for generating an audit \
                    trail"
        )

    @commands.command()
    async def flag(self, ctx: commands.Context):
        """
        !project
            explains the project
        """

        await ctx.send(
            f"{ctx.author.name} https://nzhistory.govt.nz/media/photo/fire-lazar"
        )

    @commands.command()
    async def devops(self, ctx: commands.Context):
        """
        !devops
            devops explained
        """

        await ctx.send(
            f"""{ctx.author.name} DevOps Engineers automate the deployment \
                of code and infrastructure. A DevOps engineer needs to understand \
                how to administer servers and infrastructure (mostly Linux based), \
                and how to deploy and run code on servers. See !howtodevops for \
                more info."""
        )

    @commands.command()
    async def howtodevops(self, ctx: commands.Context):
        """
        !howtodevops
            howtodevops explained
        """

        await ctx.send(
            f"""{ctx.author.name} DevOps engineers use software scripting (Bash, Python, etc), \
                Infrastructure as Code (Terraform, AWS CloudFormation) and CI/CD \
                platforms (Gitlab, AWS Codepipeline, CircleCI, Jenkins)."""
        )
        await asyncio.sleep(3)
        await ctx.send(
            f"""{ctx.author.name} DevOps engineers also work closely with container technologies \
                such as docker which help standardise software deployments. \
                Containers are often deployed to container orchestration systems \
                such as Kubernetes and AWS ECS."""
        )

    @commands.command()
    async def discord(self, ctx: commands.Context):
        """
        !project
            explains the project
        """

        await ctx.send(f"{ctx.author.name} https://discord.gg/mrEJ99WbyG")
