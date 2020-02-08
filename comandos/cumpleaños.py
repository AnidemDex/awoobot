from discord.ext import commands, tasks

import json
import time
import logging
import datetime
import discord

log = logging.getLogger('awoobot')

def read_json(file):
    with open(file, 'r') as json_file:
        return json.load(json_file)

def is_configurated():
    async def predicate(ctx):
        data = read_json('./comandos/config.json')
        if ctx.guild is None:
            return True
        if str(ctx.guild.id) in data:
            return True
        else:
            string = """> **Error**
            Aun no se han configurado las opciones de cumpleaños.
            Usa `c.config <canal> <mensaje>` para configurarlo
            O usa `c.help config` para mas información"""
            raise BirthdayNotConfigurated(string)
    return commands.check(predicate)

class BirthdayNotConfigurated(commands.CheckFailure):
    pass

class Cumpleaños(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot
        self.database = './db/cumpleaños.json'
        self.data = {}

        self.verify_day.start()
        
        self.msg_duplicated = "Ya habias enviado tu fecha de cumpleaños"
        self.msg_sucess = "Cumpleaños guardado"
        self.msg_badformat = """> _Error_
        Intenta enviar la fecha de forma `dia mes año`, y enviar una fecha valida
        Asi, si naciste el 10 de enero del 2000 deberias enviar: ```
        c.birthday 10 01 2000
        ```
        """
    @tasks.loop(hours=12)
    async def verify_day(self):
        print("Verificando cumpleañeros...")
        today = datetime.date.today()
        actual_time = datetime.datetime.now().time()
        limit_time = datetime.time(18, 0, 0, 0)
        actual_month = today.month
        actual_day = today.day

        if actual_time < limit_time:
            users = self.bot.database.get_birthday_where(actual_month, actual_day)
            if len(users) != 0:
                for user in users:
                    user_id = user[0]
                    user_celebrated = user[1]
                    user_guild = user[2]

                    servers_configuration = self.bot.database.get_birthday_config()

                    for server in servers_configuration:
                        guild_id = server[0]
                        guild_channel = server[1]
                        guild_message = server[2]

                        if user_guild == guild_id:
                            channel = self.bot.get_channel(int(guild_channel))

                            if not user_celebrated:
                                client = self.bot.get_user(int(user_id))

                                if "{user}" in guild_message:
                                    guild_message = guild_message.replace("{user}", client.mention)
                                
                                await channel.send(guild_message)

                                self.bot.database.update_celebrated_state(user_id)

                                guild = self.bot.get_guild(int(guild_id))
                                role = discord.utils.get(guild.roles, name='Cumpleañere')
                                member = guild.get_member(int(user_id))
                                await member.add_roles(role, reason="Está de cumple UwU")
    
    def cog_unload(self):
        self.verify_day.cancel()
        
    @verify_day.before_loop
    async def before_verify_day(self):
        await self.bot.wait_until_ready()

    @commands.command()
    @commands.is_owner()
    async def f5(self, ctx):
        self.verify_day.restart()
        pass

    # FIXME Usar un paginador
    @commands.group(aliases=['bd'])
    async def birthday(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.guild is None:
                user_id = ctx.author.id
                user_data = self.bot.database.get_user_data(user_id, 'birthday_date')
                if len(user_data) != 0:
                    user_birthday = user_data[0][0].strftime("%d del mes %m")
                    await ctx.send(f"Tu cumple es el {user_birthday}")
            else:
                string = "\n ```ini\n°·.¸.·°¯°·.¸.·°¯°·.¸.->   🎀  𝐹𝑒𝒸𝒽𝒶𝓈  🎀   >-.¸.·°¯°·.¸.·°¯°·.¸.·°\n"
                users = self.bot.database.select_two_from('name', 'birthday_date', 'birthdays')
                log.info(users)
                if len(users) != 0:
                    for user_data in users:
                        user_name = user_data[0]
                        log.info(user_name)
                        user_birthday = user_data[1].strftime("%d/%m")
                        string = string + f"\n[{user_name}]:\t\t  {user_birthday}"
                string = string + "``` Para mas informacion, usa `c.help birthday` y si quieres añadir tu cumpleaños usa `c.birthday add [tu fecha de cumpleaños]`"
                await ctx.send(string)

    
    @birthday.command()
    @is_configurated()
    async def add(self, ctx, day: int, month: int, year: int):
        user_id = ctx.author.id
        user_name = ctx.author.name
        user_guild_id = ctx.guild.id
        user_date = f"{day} {month} {year}"
        db_user_data = self.bot.database.get_user_data(user_id)
        
        if len(db_user_data) != 0:
            await ctx.send(self.msg_duplicated)

        elif await self.is_valid_date(user_date):
            self.bot.database.insert_birthday(user_id, user_name, user_guild_id, f"{day}-{month}-{year}")
            await ctx.send(self.msg_sucess)

        else:
            await ctx.send(self.msg_badformat, delete_after=10)

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(self.msg_badformat, delete_after=10)
        if isinstance(error, BirthdayNotConfigurated):
            await ctx.send(error)
        
    async def is_valid_date(self, date):
        try:
            time.strptime(date, "%d %m %Y")
            return True
        except:
            return False

def setup(bot):
    bot.add_cog(Cumpleaños(bot))