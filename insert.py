import psycopg2
from config import load_config
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash




def insert_user(nom, prenom, nom_utilisateur, e_mail, password):
    """Insert a new user into the table"""

    hashed_password = generate_password_hash(password)

    sql="""INSERT INTO users (nom, prenom, nom_utilisateur, e_mail, password)
        values(%s, %s, %s, %s, %s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nom, prenom, nom_utilisateur, e_mail, hashed_password))
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]
                conn.commit()
                print("Utilisateur inséré avec succès !")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Erreur lors de l'insertion de l'utilisateur :", error)                   
    finally:
        return record_id




def verify_user(nom_utilisateur, password):
    """Verify user credentials"""

    sql = "SELECT * FROM users WHERE nom_utilisateur = %s"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (nom_utilisateur,))
                user = cur.fetchone()
                if user and check_password_hash(user['password'], password):
                    return user
    except (psycopg2.DatabaseError, Exception) as error:
        print("Erreur lors de la vérification de l'utilisateur :", error)
    return None



def insert_contexte_projet(contexte):
    """Insert a new contexte_projet into the table"""

    sql="""INSERT INTO contexte_projet(contexte)
            values(%s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (contexte,))
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]
                conn.commit()
                print("Donnée bien insérée dans la base de données pour l'utilisateur")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données utilisateur:", error)    
    finally:
        return record_id
    
donnees_contexte_projet = [
    ("Dans un monde de plus en plus digitalisé, la présence en ligne est devenue indispensable pour toute entreprise souhaitant étendre sa portée et maximiser ses opportunités de vente. Le projet de création d'un site web e-commerce vise à répondre à cette nécessité en offrant une plateforme numérique performante, ergonomique et sécurisée. Ce site devra permettre à l'entreprise de vendre ses produits ou services à un large public tout en offrant une expérience utilisateur optimale."),
]

for contexte in donnees_contexte_projet:
    record_id = insert_contexte_projet(contexte)
    if record_id:
        print(f'Record inserted with id: {record_id}')
    else:
        print('Erreur lors de l\'insertion des données dans contexte_projet')
    


def insert_project_info(title, content):
    """Insert a new project into the table"""

    sql="""INSERT INTO project_info(title, content)
             values(%s, %s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (title, content))
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]
                conn.commit()
                print("Donnée bien insérée dans la base de données pour l'utilisateur")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données utilisateur:", error)    
    finally:
        return record_id
    
donnees_project_info = [
    ("site e-commerce","création d'un site e-commerce"),
]
for title, content in donnees_project_info:
    record_id = insert_project_info(title, content)
    if record_id:
        print(f'Record inserted with id: {record_id}')
    else:
        print('Erreur lors de l\'insertion des données dans projetc_info')




def insert_users(nom, prenom, nom_utilisateur, e_mail, password):
    """Insert a new user into the table"""

    sql = """INSERT INTO users(nom, prenom, nom_utilisateur, e_mail, password)
             VALUES(%s, %s, %s, %s, %s) RETURNING users_id"""
    
    users_id = None
    config = load_config()

    try: 
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Hash the password before inserting it into the database
                hashed_password = generate_password_hash(password, method='sha256')
                
                # Execute the insert statement
                cur.execute(sql, (nom, prenom, nom_utilisateur, e_mail, hashed_password))

                # Get the generated id back
                rows = cur.fetchone()
                if rows:
                    users_id = rows[0]

                # Commit the changes to the database
                conn.commit()
                print("Donnée bien insérée dans la base de données pour l'utilisateur")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données utilisateur:", error)    
    finally:
        return users_id





#expression_des_besoins


def insert_expression_besoin(besoins, description):
    """Insert a new record into the expression_besoin table"""

    sql = """INSERT INTO expression_besoin(besoins, description)
             VALUES(%s, %s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try: 
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute the insert statement
                cur.execute(sql, (besoins, description))

                # Get the generated id back
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]

                # Commit the changes to the database
                conn.commit()
                print("Donnée bien insérée dans la base de données pour l'expression de besoin")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données expression_besoin:", error)    
    finally:
        return record_id

# Données à insérer pour expression_besoin
donnees_expression_besoin = [
    ("Augmentation des Ventes", "Plateforme accessible 24/7, optimisation du parcours d'achat."),
    ("Expansion de la Portée", "Référencement SEO, marketing digital."),
    ("Expérience Client", "Navigation intuitive, processus de paiement sécurisé, support client réactif."),
    ("Optimisation SEO", "Contenu optimisé pour les moteurs de recherche, structure de site adéquate."),
    ("Gestion des Stocks", "Système intégré de gestion des stocks."),
    ("Analyse des Données", "Outils d'analyse pour suivre les comportements des utilisateurs et les performances des ventes."),
    ("Accessibilité et Ergonomie", "Design responsive, navigation facile sur tous les appareils."),
    ("Catalogue de Produits", "Affichage clair et organisé des produits avec filtres et catégories."),
    ("Sécurité des Transactions", "Protocoles de sécurité pour protéger les données personnelles et les paiements."),
    ("Facilité de Paiement", "Options de paiement variées, processus de paiement simplifié."),
    ("Service Après-Vente", "Support client via chat, email ou téléphone."),
    ("Programme de Fidélité", "Offrir des réductions et des récompenses pour fidéliser les clients."),
    ("Interface de Gestion", "Tableau de bord pour la gestion des produits, commandes et promotions."),
    ("Rapports et Analyses", "Outils de reporting pour les ventes et le comportement des clients."),
    ("Mises à Jour Faciles", "CMS pour mettre à jour les informations sur les produits et les contenus du site."),
    ("Gestion des Clients", "Base de données clients pour suivre les interactions et les commandes."),
    ("Sécurité et Conformité", "Respect des normes de sécurité et de confidentialité, y compris le RGPD.")
]

# Insertion des données dans expression_besoin
for besoins, description in donnees_expression_besoin:
    record_id = insert_expression_besoin(besoins, description)
    if record_id:
        print(f'Record inserted with id: {record_id}')
    else:
        print('Erreur lors de l\'insertion des données dans expression_besoin')





#cahier_de_charge

def insert_cahier_charge(fonctionnalite, exigences_techniques, contraintes_performance, autres_specifications):
    """Insert a new record into the cahier_charge table"""

    sql = """INSERT INTO cahier_charge(fonctionnalite, exigences_techniques, contraintes_performance, autres_specifications)
             VALUES(%s, %s, %s, %s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try: 
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute the insert statement
                cur.execute(sql, (fonctionnalite, exigences_techniques, contraintes_performance, autres_specifications))

                # Get the generated id back
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]

                # Commit the changes to the database
                conn.commit()
                print("Donnée bien insérée dans la base de données pour le cahier des charge")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données cahier des charge:", error)    
    finally:
        return record_id

# Données à insérer pour cahier_charges
donnees_cahier_charge = [
    ("Catalogue de Produits", "Base de données SQL, Interface utilisateur responsive", "Temps de réponse inférieur à 2s", "Support multi-langue"),
    ("Panier d'Achat", "Gestion des sessions, Enregistrement des cookies", "Supporte jusqu'à 1000 utilisateurs simultanés", "Fonctionnalité de sauvegarde du panier"),
    ("Paiement en Ligne", "Intégration avec PayPal, Stripe", "Transactions sécurisées via SSL", "Support pour plusieurs devises"),
    ("Gestion des Commandes", "Suivi des commandes en temps réel", "Performances stables avec forte charge", "Notification par email/SMS"),
    ("Support Client", "Chat en direct, FAQ intégrée", "Disponibilité 24/7", "Base de connaissances dynamique"),
    ("Analyse des Ventes", "Tableaux de bord en temps réel", "Rapports générés en moins de 5s", "Exportation des données en CSV, PDF"),
    ("Optimisation SEO", "Balises méta dynamiques, URLs conviviales", "Chargement rapide des pages", "Compatibilité avec les outils de webmaster"),
    ("Programme de Fidélité", "Gestion des points de fidélité", "Calcul des récompenses en temps réel", "Personnalisation des offres"),
    ("Sécurité", "Protection contre les attaques DDoS", "Chiffrement des données sensibles", "Conformité RGPD"),
    ("Gestion du Contenu", "CMS intégré", "Chargement asynchrone du contenu", "Éditeur WYSIWYG"),
    ("Intégration Réseaux Sociaux", "Partage automatique sur les réseaux sociaux", "Suivi des interactions", "Support des principaux réseaux (Facebook, Twitter)"),
    ("Gestion des Stocks", "Suivi des niveaux de stock", "Alertes en cas de stock faible", "Intégration avec les fournisseurs"),
    ("Performance du Site", "Utilisation de CDN", "Optimisation des images", "Cache côté client et serveur"),
    ("Personnalisation de l'Expérience Utilisateur", "Recommandations personnalisées", "Historique de navigation et d'achat", "Interface adaptative"),
    ("Mises à Jour et Maintenance", "Système de versioning", "Déploiement continu", "Sauvegardes régulières")
]

# Insertion des données dans cahier_charges
for fonctionnalite, exigences_techniques, contraintes_performance, autres_specifications in donnees_cahier_charge:
    record_id = insert_cahier_charge(fonctionnalite, exigences_techniques, contraintes_performance, autres_specifications)
    if record_id:
        print(f'Record inserted with id: {record_id}')
    else:
        print('Erreur lors de l\'insertion des données dans cahier_charge')



#backlog

def insert_backlog(tache, description, priorite, statut):
    """Insert a new record into the backlog table"""

    sql = """INSERT INTO backlog(tache, description, priorite, statut)
             VALUES(%s, %s, %s, %s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try: 
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute the insert statement
                cur.execute(sql, (tache, description, priorite, statut))

                # Get the generated id back
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]

                # Commit the changes to the database
                conn.commit()
                print("Donnée bien insérée dans la base de données pour le backlog")
    except error.UniqueViolation:
        print(f"Erreur: La tâche '{tache}' avec la description '{description}' existe déjà dans la base de données.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données backlog:", error)    
    finally:
        return record_id

# Données à insérer pour backlog
donnees_backlog = [
    ("Création de la page d'accueil", "Développer la page d'accueil avec une interface utilisateur attrayante", "Haute", "À faire"),
    ("Intégration du panier d'achat", "Ajouter une fonctionnalité de panier d'achat pour permettre aux utilisateurs de sélectionner des produits", "Moyenne", "En cours"),
    ("Mise en place du paiement en ligne", "Intégrer les passerelles de paiement comme PayPal et Stripe", "Haute", "À faire"),
    ("Gestion des utilisateurs", "Développer des fonctionnalités pour l'inscription, la connexion et la gestion des profils utilisateurs", "Haute", "À faire"),
    ("Optimisation SEO", "Améliorer le référencement du site pour augmenter la visibilité sur les moteurs de recherche", "Moyenne", "À faire"),
    ("Analyse des ventes", "Créer des tableaux de bord pour analyser les ventes et le comportement des utilisateurs", "Basse", "À faire"),
    ("Support client", "Intégrer une fonctionnalité de chat en direct pour le support client", "Moyenne", "À faire"),
    ("Gestion des stocks", "Développer un système pour suivre et gérer les niveaux de stock", "Haute", "À faire"),
    ("Intégration des réseaux sociaux", "Permettre le partage sur les réseaux sociaux et le suivi des interactions", "Basse", "À faire"),
    ("Programme de fidélité", "Mettre en place un programme de fidélité pour récompenser les clients réguliers", "Moyenne", "À faire")
]

# Insertion des données dans backlog
for tache, description, priorite, statut in donnees_backlog:
    record_id = insert_backlog(tache, description, priorite, statut)
    if record_id:
        print(f'Record inserted with id: {record_id}')
    else:
        print('Erreur lors de l\'insertion des données dans backlog')



def insert_documents(file_name, content):
    """Insert a new file_name into the documents table"""

    sql = """INSERT INTO documents(file_name, content)
             VALUES(%s, %s) RETURNING id"""
    
    record_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (file_name, content))
                rows = cur.fetchone()
                if rows:
                    record_id = rows[0]
                    conn.commit()
                    print("Donnée bien insérée dans la base de données pour le document")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de l'insertion des données documents:", error) 
    finally:
        return record_id
    

