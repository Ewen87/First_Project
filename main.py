# pip install ollama langchain_community langgraph duckduckgo-search

from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3"
)





prompt = f"""
    Vous allez créer la documentation complète pour un projet. Cette documentation inclut l'expression des besoins, le cahier des charges, et le backlog. Vous recevrez deux éléments pour chaque projet : le nom du projet et une description détaillée du projet.

    Inputs :
    - Nom du projet : Site Web
    - Description du projet : Site Web pour une application de gestion de stock

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
    """
print(llm.invoke(prompt))