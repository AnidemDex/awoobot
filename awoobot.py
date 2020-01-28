
import os
import logging
import discord
from discord.ext import commands
from config import configuration
from config import set_loggers

log = logging.getLogger(__name__)
set_loggers()

config = configuration()
token = config.discord_token
prefix = config.prefix

bot = commands.Bot(command_prefix=prefix)

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