
import os
import logging
import discord
from discord.ext import commands
from config import Configuration
from config import set_loggers
from config import DataBase

# `Invitacion` <https://discordapp.com/api/oauth2/authorize?client_id=669722029196443679&permissions=378944&scope=bot>

log = logging.getLogger(__name__)
set_loggers()

config = Configuration()
token = config.discord_token
prefix = config.prefix

database_parameters = {"host":config.database_host_name,
                        "database":config.database_name,
                        "user":config.database_user_name,
                        "password":config.database_password}

bot = commands.Bot(command_prefix=prefix)

bot.database = DataBase(database_parameters)
bot.database.connect()

help_command = commands.DefaultHelpCommand()

bot.help_command = help_command
@bot.event
async def on_ready():
    bot.load_extension('comandos.misc')
    bot.load_extension('comandos.debug')
    bot.load_extension('comandos.cumpleaños')
    log.info(f"[{bot.user}] Poderes dulces activados")
    log.info(f"[Servidores] {len(bot.guilds)}")
    log.info(f"[Descripción] {bot.description}")

#@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        string = """> **Exclusivo para el creador**
        Lo siento. Este comando solamente puede usarlo quien hostea el bot.
        """
        await ctx.send(string)
    if isinstance(error, type(None)):
        pass
    else:
        log.exception("Ocurrio un problema")
        log.error(ctx)

def start():
    bot.run(token)