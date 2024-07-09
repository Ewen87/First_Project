# ajouter le database.ini au .gitignorefichier pour éviter de transmettre des informations sensibles à un référentiel public comme GitHub
#utilise le config.py module pour lire la configuration de la base de données et se connecter à PostgreSQL
import psycopg2
from config import load_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        with psycopg2.connect(**config) as conn:
            print('connecté au serveur PostgreSQL')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    connect(config)


conn = psycopg2.connect("dbname=suppliers user=postgres password=Christyoann88")
