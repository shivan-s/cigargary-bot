#!python3.8
# -*- coding: utf-8 -*-
# twitch.py - contains the main scripts for running the twitch bot
# pipenv - this will load .env variables

import logging
import os
import sys
import random
import asyncio

from typing import Optional

from sqlalchemy import create_engine, MetaData, Column, String, Integer, select
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session, declarative_base
from twitchio.ext import commands

# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:

    sys.exit("DATABASE_URL not supplied.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)

Base: DeclarativeMeta = declarative_base()


class Motivation(Base):
    __tablename__ = "motivations"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    phrase = Column(String)

    def __repr__(self):
        return f"Motivation(id={self.id!r}, name={self.user!r}, phrase={self.phrase!r})"


meta = MetaData(engine)
meta.create_all()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


async def strip_command(command: str, message: str) -> Optional[str]:
    prefix = f"""{os.getenv("BOT_PREFIX")}{command}"""

    if not message.lower().startswith(prefix):
        return None

    import re

    content = re.sub(f"^{prefix}\\s+", "", message, flags=re.I)

    if content.lower().startswith(prefix):
        return None

    return content


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

    @commands.command()
    async def givemotivation(self, ctx: commands.Context):
        """
        !givemotivation
            Store a motivation
        """

        content = ctx.message.content
        content = await strip_command("givemotivation", content)

        if content is None:
            await ctx.send(
                f"{ctx.author.name} - I couldn't save your motivation :("
            )
            return

        with Session(engine) as session:
            motivation = Motivation(user=ctx.author.name, phrase=content)

            session.add(motivation)
            session.commit()

            await ctx.send(
                f"{motivation.id}: {motivation.phrase} - {motivation.user}"
            )

    @commands.command()
    async def motivate(self, ctx: commands.Context):
        """
        !motivate
            Get a motivate
        """
        content = ctx.message.content
        content = await strip_command("motivate", content)

        with Session(engine) as session:
            if content is not None and content.isdigit():
                stmt = select(Motivation).where(Motivation.id == content)
            else:
                stmt = select(Motivation).order_by(func.random()).limit(1)

            result = session.execute(stmt)
            row = result.fetchone()

            if not row:
                await ctx.send(
                    f"{ctx.author.name} - I'm not motivated right now."
                )
            else:
                await ctx.send(
                    f"""{row["Motivation"].id}: \
                        {row["Motivation"].phrase} - {row["Motivation"].user}"""
                )

    @commands.command()
    async def takemotivation(self, ctx: commands.Context):
        """
        !takemotivation
            Delete a motivation
        """
        if ctx.author.name not in ["cigargary", "Shivans93"]:
            await ctx.send(
                f"{ctx.author.name} - Thou shalt not take motivation."
            )
            return

        content = ctx.message.content
        content = await strip_command("takemotivation", content)

        with Session(engine) as session:
            if content is not None and content.isdigit():
                stmt = select(Motivation).where(Motivation.id == content)
                result = session.execute(stmt)
                row = result.fetchone()
                if row is None:
                    await ctx.send(
                        f"{ctx.author.name} - Motivation already taken."
                    )
                    return
                session.delete(row["Motivation"])
                session.commit()
            else:
                await ctx.send(
                    f"{ctx.author.name} - Usage !takemotivation <NUMBER>"
                )
                return
