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
    
    @commands.command()
    @commands.is_owner()
    async def page(self, ctx, *, text: str):
        pass
        
    
    @commands.group()
    @commands.is_owner()
    async def database(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    # FIXME Encontrar como enviar todos estos mensajes en un embebido
    @database.command()
    @commands.is_owner()
    async def readall(self, ctx):
        reply = self.bot.database.select_all_from('birthdays')
        for data in reply:
            await ctx.send(data)
    
    @database.command()
    @commands.is_owner()
    async def send(self, ctx, *, sql: str):
        reply = self.bot.database.send(sql)
        await ctx.send(reply)
    
    @database.command()
    @commands.is_owner()
    async def getuserdata_len(self, ctx, user_id: str):
        reply = self.bot.database.get_user_data(user_id)
        await ctx.send(reply)
        await ctx.send(len(reply))
    
    @database.command()
    @commands.is_owner()
    async def getservers_configuration(self, ctx):
        reply = self.bot.database.get_birthday_config()
        await ctx.send(reply)
        await ctx.send(len(reply))

    
def setup(bot):
    bot.add_cog(Desarrollo(bot))