from flask import Flask, render_template, url_for, request, redirect, session
from .modele import selectionner_livre, mettre_a_jour_table_livre, getTopVideos, getVideo, research, db_identification
app = Flask(__name__)


# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')

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
    id = result['video']

    video = getVideo(id)
    session['watching'] = video

    return render_template('displayVid.html', video = video)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        videos = research(query)
        session['videos'] = videos
        session['query'] = query
    else:
        videos = session['videos']
        query = session['query']
    return render_template('search.html', videos = videos, query = query)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        print('request: ', request.form)
        resultat = request.form
        rows = db_identification(resultat)
        nextURL = resultat['current']
        print("session videos : " , session['videos'])
        if len(rows) == 1:
            session['ID'] = rows[0][0]
            session['username'] = rows[0][2]

        if nextURL == 'video':
            return redirect(url_for('video'), video = session['watching'])
    return redirect(url_for(nextURL)) #renvoie sur la route '/'


