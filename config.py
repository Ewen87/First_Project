#cette fonction permet de lire les données de configuration de database.ini
from configparser import ConfigParser
import os
import config

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)


    #get section , default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
    return config


class config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '4e3d2b6fcbf4439b6d9f24af7301a7d5f2b9f6e5a1f4e3d4b6c7e2f1')
if __name__ == '__main__':
    config = load_config()
    print(config)