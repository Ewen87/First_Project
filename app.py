from flask import Flask, render_template, request, redirect, send_file, session, url_for, flash,jsonify
import openai
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from insert import insert_documents, insert_user, insert_users, verify_user
from config import load_config
import psycopg2
# import openai
import os
from langchain_community.llms import Ollama
from docx import Document
from psycopg2.extras import RealDictCursor


# from fdpf import FPDF


app = Flask(__name__)

app.config.from_object(config)
openai.api_key= os.getenv('OPENAI_API_KEY')
#openai.api_key="sk-proj-pyvKcTjCSHZe71Fx9wmOT3BlbkFJxoJ0gLjbrILvpolbAwMR"

llm = Ollama(
    model="llama3"
)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/document')
def document():
    return render_template('document.html')


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        nom_utilisateur = request.form['nom_utilisateur']
        e_mail = request.form['email']
        password = request.form['password']
        
        # Insérer l'utilisateur dans la base de données
        try:
            insert_user(nom, prenom, nom_utilisateur, e_mail, password)
            flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('inscription'))
        except Exception as e:
            flash(f'Erreur lors de l\'inscription: {e}', 'danger')
            return redirect(url_for('inscription'))
    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        password = request.form['password']
        
        # Vérifier les informations d'identification de l'utilisateur
        try:
            user = verify_user(nom_utilisateur, password)
            if user:
                session['user_id'] = user['id']
                session['nom_utilisateur'] = user['nom_utilisateur']
                flash('Connexion réussie', 'success')
                return redirect(url_for('document'))  # Rediriger vers la page d'accueil ou une autre page
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
        except Exception as e:
            flash(f'Erreur lors de la connexion: {e}', 'danger')
    return render_template('connexion.html')



#Endpoints pour récupérer les données dans postgresql
def connect_to_database():
    config = load_config()
    conn = psycopg2.connect(**config)
    return conn


@app.route('/contexte_projet')
def get_contexte_projet():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT contexte FROM contexte_projet")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/expression_besoin')
def get_expression_besoin():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expression_besoin")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/cahier_charge')
def get_cahier_charge():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cahier_charge")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/backlog')
def get_backlog():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM backlog")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/display')
def display():
    return render_template('display.html')


@app.route('/project_info')
def get_project_info():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT content FROM project_info")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/compare', methods=['POST'])
def compare_description():
    data = request.json
    description_projet = data.get('description_projet')

    config = load_config()
    db_contents = []

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT content FROM project_info")
                rows = cur.fetchall()
                db_contents = [row[0] for row in rows]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de la récupération des données:", error)
        return jsonify({'error': str(error)}), 500

    match = description_projet in db_contents
    return jsonify({'match': match})

@app.route('/documentation')
def documentation_page():
    return render_template('documentation.html')




# Gestionnaire d'erreurs global
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Erreur serveur: {e}")
    response = {
        "error": "Erreur interne du serveur",
        "details": str(e)
    }
    return jsonify(response), 500


@app.route('/generer_documentation_chatgpt', methods=['POST'])
def generer_documentation_chatgpt():
    data = request.json
    nom_projet = data.get('nom_projet')
    description_projet = data.get('description_projet')
    format = data.get('format', 'txt')
    file_name = data.get('file_name', 'document')

    if not nom_projet or not description_projet:
        return jsonify({'error': 'Nom du projet et description du projet sont requis'}), 400

    # Prépare le prompt 
    prompt = f"""
    Vous allez créer la documentation complète pour un projet. Cette documentation inclut l'expression des besoins, le cahier des charges, et le backlog. Vous recevrez deux éléments pour chaque projet : le nom du projet et une description détaillée du projet.

    Inputs :
    - Nom du projet : {nom_projet}
    - Description du projet : {description_projet}

    Outputs attendus :
    1. Expression des besoins :
       - Liste des besoins fonctionnels et non fonctionnels
       - Objectifs principaux du projet
       - Contraintes et dépendances

    2. Cahier des charges :
       - Présentation du projet (incluant le nom et la description)
       - Contexte et problématique
       - Périmètre du projet
       - Spécifications fonctionnelles détaillées
       - Spécifications techniques
       - Critères de réussite et indicateurs de performance
       - Risques et plans de mitigation

    3. Backlog :
       - Liste des User Stories avec priorités
       - Tâches associées à chaque User Story
       - Définition des critères de complétion (definition of done) pour chaque tâche
       - Estimations en termes de points de complexité ou de temps

    4. Tableau récapitulatif :
        - Vue d'ensemble des éléments de l'expression des besoins, du cahier des charges, et du backlog sous forme de tableau
    """

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=2000
    )
    documentation = response.choices[0].text.strip()

    insert_documents(nom_projet, documentation)

    return jsonify({'documentation': documentation})

@app.route('/generer_documentation_ollama', methods=['POST'])
def generer_documentation_ollama():
    data = request.json
    nom_projet = data.get('nom_projet')
    description_projet = data.get('description_projet')

    if not nom_projet or not description_projet:
        return jsonify({'error': 'Nom du projet et description du projet sont requis'}), 400
    
    # Prépare le prompt 
    prompt = f"""
Vous allez créer la documentation complète pour un projet. Cette documentation inclut l'expression des besoins, le cahier des charges, et le backlog. Vous recevrez deux éléments pour chaque projet : le nom du projet et une description détaillée du projet.

Inputs :
- Nom du projet : {nom_projet}
- Description du projet : {description_projet}

Outputs attendus :
1. Expression des besoins :
   - Liste des besoins fonctionnels et non fonctionnels
   - Objectifs principaux du projet
   - Contraintes et dépendances

2. Cahier des charges :
   - Présentation du projet (incluant le nom et la description)
   - Contexte et problématique
   - Périmètre du projet
   - Spécifications fonctionnelles détaillées
   - Spécifications techniques
   - Critères de réussite et indicateurs de performance
   - Risques et plans de mitigation

3. Backlog :
   - Liste des User Stories avec priorités
   - Tâches associées à chaque User Story
   - Définition des critères de complétion (definition of done) pour chaque tâche
   - Estimations en termes de points de complexité ou de temps

4. Tableau récapitulatif :
   - Vue d'ensemble des éléments de l'expression des besoins, du cahier des charges, et du backlog sous forme de tableau
"""

    documentation = llm.invoke(prompt)

    insert_documents(nom_projet, documentation)

    return jsonify({'documentation': documentation})

@app.route('/generer_documentation_other', methods=['POST'])
def generer_documentation_other():
    return jsonify({'error': 'Ce modèle n\'est pas encore implémenté. Veuillez choisir un autre modèle.'}), 501

@app.route('/result')
def result():
    documentation = request.args.get('documentation')
    if documentation:
        return render_template('result.html', documentation=documentation)
    else:
        return jsonify({'error': 'Documentation non trouvée'}), 404
    
    
@app.route('/telecharger_documentation', methods=['POST'])
def telecharger_documentation():
    data = request.json
    documentation = data.get('documentation')
    file_name = data.get('file_name', 'documentation')
    file_format = data.get('file_format', 'txt')
    
    if not documentation:
        return jsonify({'error': 'Documentation non trouvée'}), 400

    if file_format == 'txt':
        file_path = os.path.join('downloads', f"{file_name}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(documentation)
    elif file_format == 'docx':
        file_path = os.path.join('downloads', f"{file_name}.docx")
        doc = Document()
        doc.add_paragraph(documentation)
        doc.save(file_path)
    elif file_format == 'md':
        file_path = os.path.join('downloads', f"{file_name}.md")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(documentation)
    else:
        return jsonify({'error': 'Format non supporté'}), 400

    return send_file(file_path, as_attachment=True)




def get_all_documents():
    conn = connect_to_database()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents 


@app.route('/historique')
def historique():
    documents = get_all_documents()
    return render_template('historique.html', documents=documents)


@app.route('/voir_document/<int:id>')
def voir_document(id):
    conn = connect_to_database()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM documents WHERE id = %s", (id,))
    document = cursor.fetchone()
    cursor.close()
    conn.close()

    if not document:
        return jsonify({'error': 'Document non trouvé'}),404
    
    return render_template('voir_document.html', document=document)





def supprimer_document(id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du document: {e}")
        return False

@app.route('/supprimer_document', methods=['POST'])
def supprimer_document_route():
    data = request.get_json()
    doc_id = data.get('id')
    
    if supprimer_document(doc_id):
        return jsonify(success=True)
    else:
        return jsonify(success=False), 400
    


if __name__ == '__main__':
    app.run(debug=True)
