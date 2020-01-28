import os
import logging
import json
from discord.ext import commands

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

    

class configuration():
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

    def read_configuration(self):
        with open(self.configuration_file, 'r') as json_file:
            return json.load(json_file)
        pass

    def __create_empty_configuration_file(self, path):
        config_file = open(path, 'w')
        config_file.write('{\"DISCORD_TOKEN\": \"\", \"PREFIX\": [], \"servers\": {}}')
        config_file.close()