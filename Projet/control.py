from flask import Flask, render_template, url_for, request, redirect
from .modele import selectionner_livre, mettre_a_jour_table_livre
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/afficher/livre/')
def afficher_livre():
    liste_livre = selectionner_livre()
    return render_template('affiche_livre.html', liste_des_livres = liste_livre)
@app.route('/ajouter/livre/')
def ajouter_livre():
    return render_template('ajouter_livre.html')
@app.route('/admin/enregistrer/livre', methods=['POST'])
def enregistrer_livre():
    resultat = request.form #permet de récupérer les données POST
    #sous forme d'un dictionnaire resultat
    mettre_a_jour_table_livre(resultat) #appel le modèle à utiliser
    return redirect(url_for('index'))
