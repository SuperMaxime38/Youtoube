from flask import Flask, render_template, url_for, request, redirect, session
from .modele import selectionner_livre, mettre_a_jour_table_livre, getTopVideos, getVideo, research, db_identification, comment_update, addUser, getUser, changePassword
app = Flask(__name__)
import uuid

# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    videos = getTopVideos()
    isLogged = False
    if('ID' in session):
        isLogged = True
    
    return render_template('index.html', videos = videos, isLogged = isLogged)
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


@app.route("/video", methods=['POST', 'GET'])
def video():
    if request.method == 'POST':
        result = request.form
        id = result['video']
        video = getVideo(id)
        session['watching'] = video
    else:
        video = session['watching'] 
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

    isLogged = False
    if('ID' in session):
        isLogged = True

    return render_template('search.html', videos = videos, query = query, isLogged = isLogged)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('request: ', request.form)
        resultat = request.form
        rows = db_identification(resultat)

        nextURL = 'index'
        if 'current' in resultat:
            nextURL = resultat['current']

        
        if len(rows) == 1:
            session['ID'] = rows[0][0]
            session['username'] = rows[0][2]

            if nextURL == 'video':
                return redirect(url_for('video'), video = session['watching'])
            if nextURL == 'search':
                return redirect(url_for('search'), query = session['query'])
            
            return redirect(url_for(nextURL)) #renvoie sur la route '/'
        
    # DO A LOGIN PAGE
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('ID', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'ID' not in session:
        return redirect(url_for('login'))
    else:
        ID = session['ID']
        user = list(getUser(ID))

        msg = request.args.get('msg')
        color = request.args.get('color')
        if msg is None:
            msg = ""
        if color is None:
            color = "red"

        return render_template('account.html', user = user, msg = msg, color = color)


@app.route("/change/password", methods=['POST'])
def change_password():
    if request.method == 'POST':
        if 'ID' not in session:
            return redirect(url_for('index'))
        else:
            result = request.form
            password = result['password']
            new_password = result['new_password']
            new_password_confirm = result['new_password_confirm']

            if new_password != new_password_confirm:
                return redirect(url_for('account', msg = "Passwords don't match", color = "red"))
            else:
                thing = {
                    'login': session['username'],
                    'password': password
                }
                result = db_identification(thing)
                print("result", result, " len res:", len(result))
                if len(result) != 1:
                    return redirect(url_for('account', msg = "Wrong password", color = "red"))
                
                changePassword(session['ID'],new_password)

            return redirect(url_for('account', msg = "Password changed !", color = "green"))

@app.route("/comment", methods=['POST'])
def comment():
    if request.method == 'POST':
        if 'ID' not in session:
            return redirect(url_for('index'))
        else:
            video = session['watching']
            texte = request.form['story']
            pseudo = session['username']
            comment_id = str(uuid.uuid4())
            comment_update(comment_id, video, pseudo, texte)
            return redirect(url_for('video', video = video))
            

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        result = request.form
        username = result['username']
        mail = result['mail']
        password = result['password']
        userID = str(uuid.uuid4())
        success = addUser(userID, username, mail, password)


        msg = "This email has been already used"
        if not success:
            return redirect(url_for('signup', msg = msg))
        nextURL = result['current']
        if nextURL == 'video':
            return redirect(url_for('video'), video = session['watching'])
        if nextURL == 'search':
            return redirect(url_for('search'), query = session['query'])

        return redirect(url_for('index'))
    
    message = request.args.get('msg')
    if message is None:
        message = ""
    return render_template('signup.html', msg = message)