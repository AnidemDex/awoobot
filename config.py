import os
import json
from discord.ext import commands

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        pass

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