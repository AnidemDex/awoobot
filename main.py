#!/usr/bin/env python3

import os
import logging
from discord.ext import commands
from config import configuration

log = logging.getLogger(__name__)
log_handler = logging.FileHandler('info.log')
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

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
    log.info("Poderes dulces activados")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        string = """> **Exclusivo para el creador**
        Lo siento. Este comando solamente puede usarlo quien hostea el bot.
        """
        await ctx.send(string)
    else:
        log.exception("Ocurrio un problema")

bot.run(token)