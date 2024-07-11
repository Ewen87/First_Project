Ceci est une brève description de mon projet : 

Thème de Projet : Mise en place d'une plateforme de génération automatisée de documents de projet avec l'IA

Fonctionnalités:

- Inscription et connexion des utilisateurs.
- Génération de documentation de projet via OpenAI et Ollama.
- Sauvegarde et récupération de documents depuis une base de données PostgreSQL.
- Téléchargement de la documentation générée en différents formats (txt, docx, md).
- Visualisation de l'historique des documents générés.

Installation:

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/Ewen87/First_Project.git
   cd First_Project

2. Insallation des dépendances :
pip install -r requirements.txt

Assuerez vous aussi que les bibliothèques suivantes sont égamement installées :
Flask
openai
psycopg2-binary
python-dotenv
werkzeug
langchain-community
python-docx


3.Configuration de la clé Openai
OPENAI_API_KEY="votre clé Openai"

4.Configuration de la base de donnée PostgreSql
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

UTILISATION :
1.Lancez l'application Flask

python app.py

2.Accéder à l'application via :http://localhost:5000

Capture d'écran :
Page d'inscription : <img src="image/inscription.png">
Il faut s'inscrire avant d'avoir accès à la page .

page de connexion:<img src="image/se_connecter.png">
Pour les utilisateurs ayant déja un compte , il suffit de se connecter

Page de génération de document : <img src="image/formulaire.png">
Il faut donner un nom projet puis une description de son projet et choisir le modèle d'IA.
Remarque : Si une clé API n'est pas défini dans le code une erreur s'affichera.

Page d'affichage : <img src="image/document.png">

Des formats pour télécharger la documentation générée qui sont : Word , MarkDown ou PDF: <img src="image/telecharger.png">

Page d'historique : <img src="image/historique.png">

N.B : Dans cette application il reste à permettre à chque utilisateur d'avoir son propre environnement de travail . Pour l'instant lorsqu'un utilisateur se connecte il a un espace de travail en commun avec tous les autres utilisateurs.
