import psycopg2
from config import load_config

def create_tables():
    """Create tables in the PostgreSQL database"""

    e_commerce_tables = (
        """CREATE TABLE IF NOT EXISTS contexte_projet(
            id SERIAL PRIMARY KEY,
            contexte TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS project_info (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(80) NOT NULL,
            prenom VARCHAR(80) NOT NULL,
            nom_utilisateur VARCHAR(80) UNIQUE NOT NULL,
            e_mail VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS expression_besoin (
            id SERIAL PRIMARY KEY,
            besoins VARCHAR(255),
            description TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS cahier_charge (
            id SERIAL PRIMARY KEY,
            fonctionnalite VARCHAR(255),
            exigences_techniques TEXT,
            contraintes_performance TEXT,
            autres_specifications TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS backlog(
            id SERIAL PRIMARY KEY,
            tache VARCHAR(255),
            description TEXT,
            priorite VARCHAR(50),
            statut VARCHAR(50)
        )""",
        """CREATE TABLE IF NOT EXISTS documents(
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
    )

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute the CREATE TABLE statements
                for sql_statement in e_commerce_tables:
                    cur.execute(sql_statement)
        print("Tables créées avec succès !")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Erreur lors de la création des tables :", error)

if __name__ == '__main__':
    create_tables()
