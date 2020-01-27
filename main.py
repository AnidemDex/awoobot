import os
from discord.ext import commands
from dotenv import load_dotenv

# No olvides crear un archivo .env en la raiz de la carpeta con estos atributos
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('BOT_PREFIX')

bot = commands.Bot(command_prefix=prefix)

bot.load_extension('comandos.misc')
bot.load_extension('comandos.debug')
bot.load_extension('comandos.cumpleaños')

help_command = commands.DefaultHelpCommand()


bot.help_command = help_command
@bot.event
async def on_ready():
    print("Poderes de dulce activados.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        string = """> **Exclusivo para el creador**
        Lo siento. Este comando solamente puede usarlo quien hostea el bot.
        """
        await ctx.send(string)
    else:
        print(error)

bot.run(token)