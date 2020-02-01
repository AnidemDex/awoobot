import os
import logging
import json
import psycopg2
from discord.ext import commands

log = logging.getLogger('awoobot')

# FIXME
class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        pass

def set_loggers():
    datefmt = '%d/%m/%Y %I:%M:%S %p'

    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    log_file_handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
    log_console_handler = logging.StreamHandler()
    log_file_formatter = logging.Formatter('[%(asctime)s] [%(name)s] %(levelname)s: %(message)s', datefmt=datefmt)
    log_console_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt=datefmt)
    log_file_handler.setFormatter(log_file_formatter)
    log_console_handler.setFormatter(log_console_formatter)

    discord_log = logging.getLogger('discord')
    discord_log.setLevel(logging.INFO)    
    discord_log.addHandler(handler)

    bot_log = logging.getLogger('awoobot')
    bot_log.setLevel(logging.INFO)
    bot_log.addHandler(log_file_handler)
    bot_log.addHandler(log_console_handler)

    commands_owner_log = logging.getLogger('debug')
    commands_owner_log.setLevel(logging.DEBUG)
    commands_owner_log.addHandler(log_file_handler)

class DataBase():
    """
    Database connection class
    """

    def __init__(self, params):
        self.__connection = None
        self.__parameters = params

        log.info("Objeto para el manejo de la base de datos creado")
    
    def connect(self):
        try:
            log.info("Conectandose a la base de datos...")

            self.__connection = psycopg2.connect(**self.__parameters)
            cursor = self.__connection.cursor()
            
            cursor.execute('SELECT version();')
            version = cursor.fetchone()

            log.debug(f"{version}")
            cursor.close()

        except Exception as error:
            log.exception("Hubo un problema al conectarse a la base de datos")
            log.error(error)
            exit()
    
    def select_all_from(self, table):
        try:
            SQL = f"""SELECT * FROM {table}"""
            result = None
            with self.__connection:
                with self.__connection.cursor() as cursor:
                    cursor.execute(SQL)
                    result = cursor.fetchall()
            return result

        except Exception:
            log.exception("Hubo un problema leyendo los datos de la tabla")

    def insert_birthday(self, user_id, name, guild_id, birthday_date, is_celebrated=False):
        try:
            SQL = """INSERT INTO birthdays (user_id, name, guild_id, birthday_date, is_celebrated)
                    VALUES (%s, %s, %s, %s, %s);"""
            with self.__connection:
                with self.__connection.cursor() as cursor:
                    cursor.execute(SQL, (user_id, name, guild_id, birthday_date, is_celebrated))

        except Exception as error:
            log.exception("Hubo un problema insertando datos a la tabla")
            log.error(error)

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
            log.info("Conexion con la base de datos finalizada")
    
    def send(self, str):
        try:
            SQL = f"""{str}"""
            result = None
            with self.__connection:
                with self.__connection.cursor() as cursor:
                    cursor.execute(SQL)
                    result = cursor.fetchall()
            return result

        except Exception:
            log.exception("Hubo un problema enviando el mensaje")
    
    def get_user_data(self, user_id):
        query = f"""SELECT * FROM birthdays WHERE user_id='{user_id}' """
        reply = self.send(query)
        return reply



class Configuration():
    def __init__(self, configuration_file='config.json'):
        if os.path.isfile(configuration_file):
            self.configuration_file = configuration_file
        else:
            self.__create_empty_configuration_file(configuration_file)
            raise FileNotFoundError

        self.configuration_data = self.read_configuration()
        
    @property
    def discord_token(self):
        return self.configuration_data['DISCORD_TOKEN']
    
    @property
    def prefix(self):
        return self.configuration_data['PREFIX']

    @property
    def database_host_name(self):
        return self.configuration_data['HOST']
    
    @property
    def database_user_name(self):
        return self.configuration_data['USER']
    
    @property
    def database_password(self):
        return self.configuration_data['PSWD']
    
    @property
    def database_name(self):
        return self.configuration_data['DB']

    def read_configuration(self):
        with open(self.configuration_file, 'r') as json_file:
            return json.load(json_file)
        pass

    def __create_empty_configuration_file(self, path):
        config_file = open(path, 'w')
        config_file.write('{\"DISCORD_TOKEN\": \"\", \"PREFIX\": [], \"host\": \"\", \"user\": \"\", \"password\": \"\", \"database\": \"\"}')
        config_file.close()