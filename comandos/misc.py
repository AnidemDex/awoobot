from discord.ext import commands
from discord import version_info, __version__
import json

class Miscelaneo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configuration = './comandos/config.json'

        self.msg_configerror = """> _**Info**_
        Este comando necesita que configures el canal y el mensaje de la forma:```
        c.config {canal} {mensaje}```
        No te preocupes, no necesitas darme el ID del canal, solo _#mencionalo_
        Y si quieres pinguear a la persona, escribe `{user}` en la parte del mensaje
        donde quieres mencionarlo"""

        self.msg_info = """> _**Info**_
        Fui hecha como en ~~15 minutos xd~~ 5 horas. No te alarmes, no sé hacer pastel
        `PyVersion` **{} {}**
        `Servidores` {}
        `Invitacion` <https://discordapp.com/api/oauth2/authorize?client_id=669722029196443679&permissions=378944&scope=bot>
        Usa `c.help` si quieres ver los comandos""".format(__version__, version_info.releaselevel, len(self.bot.guilds))
        pass

    @commands.command()
    async def info(self, ctx):
        await ctx.send(self.msg_info)
        pass

    @commands.command()
    async def ping(self, ctx):
        pass

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx, channel, *, message):
        config = {ctx.guild.id: {'birthday_channel': channel, 'birthday_message': message}}
        with open(self.configuration, 'w') as outfile:
            json.dump(config, outfile)
        await ctx.send(f"El canal a usar es {channel}")
    
    @config.error
    async def config_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(self.msg_configerror)


def setup(bot):
    bot.add_cog(Miscelaneo(bot))