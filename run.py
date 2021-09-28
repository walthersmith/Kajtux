"""
======================= START OF LICENSE NOTICE =======================
  Copyright (C) 2021 walther smith franco otero. All Rights Reserved

  NO WARRANTY. THE PRODUCT IS PROVIDED BY DEVELOPER "AS IS" AND ANY
  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DEVELOPER BE LIABLE FOR
  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
  IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE PRODUCT, EVEN
  IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
======================== END OF LICENSE NOTICE ========================
  Primary Author: walther smith franco otero

"""
import logging
import os
import sys
import traceback
from os import listdir
from os.path import join, isfile

# Discord
import discord
from discord.ext import commands
from dotenv import load_dotenv

# project
from models.base import engine, Base, session
from models.jail import Jail
from models.users_roles import Users_roles
from models.warning_config import Warning_config
from models.giveaways import Giveaways


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['c.']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


""" principal class where everything begins"""
intents = discord.Intents().all()
intents.members = True
intents.presences = True
description = '''Kajtux Bot'''
client = commands.AutoShardedBot(command_prefix=get_prefix, description=description, intents=intents)


@client.event
async def on_ready():
    """https://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await client.change_presence(activity=discord.Game(name='> Cucarachin :) '))
    print(f'Successfully logged in and booted...!')

    # create database
    c = os.getenv("CREATE_DB")
    if int(c) != 0:
        # generate database schema
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@client.command(name='restart', hidden=True)
@commands.is_owner()
async def restart(ctx):
    message = await ctx.send("Restarting... Allow up to 5 seconds")
    restart_program()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.  use command help")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the appropriate permissions to run this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")
    else:
        print("error not caught")
        print(error)


# Initial configuration
if __name__ == "__main__":
    EXTENSIONS_DIR = "extensions"
    print("Loading extensions")
    print("-----------------------")
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    for extension in [f.replace('.py', '') for f in listdir(EXTENSIONS_DIR) if isfile(join(EXTENSIONS_DIR, f))]:
        try:
            print(f"loading: {extension}")
            client.load_extension(EXTENSIONS_DIR + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load Extension {extension}")
            traceback.print_exc()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        logger.error("Discord bot token not found at: .env file \n... Please correct file path in run.py file.")
        raise Exception("Discord bot token not found at: .env file \n... Please correct file path in run.py file.")
        sys.exit()
    client.run(TOKEN, bot=True, reconnect=True)
