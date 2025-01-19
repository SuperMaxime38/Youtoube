from flask import Flask, render_template, url_for, request, redirect
from .modele import selectionner_livre, mettre_a_jour_table_livre, getTopVideos
app = Flask(__name__)
@app.route('/')
def index():
    videos = getTopVideos()
    print(videos)
    return render_template('index.html', videos = videos)
@app.route('/afficher/livre/')
def afficher_livre():
    liste_livre = selectionner_livre()
    return render_template('affiche_livre.html', liste_des_livres = liste_livre)
@app.route('/ajouter/livre/')
def ajouter_livre():
    return render_template('ajouter_livre.html')


@app.route('/admin/enregistrer/livre', methods=['POST'])
def enregistrer_livre():
    print("test !")
    resultat = request.form #permet de récupérer les données POST
    #sous forme d'un dictionnaire resultat
    mettre_a_jour_table_livre(resultat) #appel le modèle à utiliser
    return redirect(url_for('index'))


@app.route("/video", methods=['POST'])
def video():
    result = request.form
    video = result['video']
    print("opened video " + video)
    return render_template('displayVid.html', video = video)

# @app.route('/video/watch', methods=['POST'])
# def watch():
#     result = request.form
#     print(result)
#     return redirect(url_for('video'))