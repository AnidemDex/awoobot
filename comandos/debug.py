import logging
from discord.ext import commands

log = logging.getLogger(__name__)

class Desarrollo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_folder = 'comandos'
        self.message_pass = "Comandos actualizados"
        self.owner_id = 496111747711631360
    
    @commands.group()
    @commands.is_owner()
    async def reload(self, ctx):
        if ctx.invoked_subcommand is None:
            command = ctx.args[0]
            log.debug(f"<<<Intento de refrescar {command}>>>")
            self.bot.reload_extension(command)
            await ctx.send(self.message_pass)
    
    @reload.command()
    @commands.is_owner()
    async def all(self, ctx):
        self.bot.reload_extension(f"{self.commands_folder}.debug")
        self.bot.reload_extension(f"{self.commands_folder}.misc")
        await ctx.send(self.message_pass)
    
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.send("Prueba exitosa")
    
def setup(bot):
    bot.add_cog(Desarrollo(bot))