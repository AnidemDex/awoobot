from discord.ext import commands, tasks

import json
import time

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
        actual_time = time.localtime()
        actual_day = actual_time.tm_mday
        actual_month = actual_time.tm_mon

        if actual_time.tm_hour < 18:

            old_data = read_json(self.database)
            
            for user_id in old_data:
                user = old_data[user_id]
                user_month = int(user['month'])
                user_day = int(user['day'])
                user_celebrated = bool(user['celebrated'])
                if user_month == actual_month and user_day == actual_day:
                    
                    if not user_celebrated:
                        config_json = read_json('./comandos/config.json')
                        user_guild = str(user['guild'])
                        if user_guild in config_json:
                            guild = config_json[user_guild]
                            channel = guild['birthday_channel']
                            channel = channel.replace('#', '')
                            channel = channel.replace('<', '')
                            channel = channel.replace('>', '')
                            channel = int(channel)
                            channel = self.bot.get_channel(channel)

                            message = guild['birthday_message']
                            id = int(user_id)
                            client = self.bot.get_user(id)
                            message = message.replace("{user}", client.mention)

                            await channel.send(message)
                            
                            old_data[user_id].update(user)
                            user.update({'celebrated':True})
                            with open(self.database, 'w') as outfile:
                                json.dump(old_data, outfile)
    
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

    @commands.group(aliases=['bd'])
    async def birthday(self, ctx):
        if ctx.invoked_subcommand is None:
            data = read_json(self.database)
            if ctx.guild is None:
                user_id = data[str(ctx.author.id)]
                
                await ctx.send(f"Tu cumples el " + f"{user_id['day']}/{user_id['month']}/{user_id['year']}")
            else:
                string = "\n ```ini\n°·.¸.·°¯°·.¸.·°¯°·.¸.->   🎀  𝐹𝑒𝒸𝒽𝒶𝓈  🎀   >-.¸.·°¯°·.¸.·°¯°·.¸.·°\n"
                for users in data:
                    user_id = data[users]
                    user_name = user_id['name']
                    user_bday = f"{user_id['day']}/{user_id['month']}/{user_id['year']}"
                    text = f"[{user_name}]: {user_bday}"
                    string = string + f"\n{text}"
                string = string + "``` Para mas informacion, usa `c.help birthday` y si quieres añadir tu cumpleaños usa `c.birthday add [tu fecha de cumpleaños]`"
                await ctx.send(string)
                pass
    
    @birthday.command()
    @is_configurated()
    async def add(self, ctx, day: str, month: str, year: str):
        id = ctx.author.id
        name = ctx.author.name
        date = f"{day} {month} {year}"
        old_data = read_json(self.database)
        
        if str(id) in old_data:
            await ctx.send(self.msg_duplicated)

        elif await self.is_valid_date(date):
            self.data.update(old_data)
            self.data[str(id)]= {}
            self.data[str(id)].update({'name':name, 'guild':ctx.guild.id, 'day':day, 'month':month, 'year': year, 'celebrated':False})
            with open(self.database, 'w') as outfile:
                json.dump(self.data, outfile)
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