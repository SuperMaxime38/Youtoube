from flask import Flask, render_template, url_for, request, redirect, session
from .modele import getTopVideos, getVideo, research, db_identification, comment_update, addUser, getUser, changePassword, handleView, likeVideo, isVideoLiked, getComments, countLikes, countViews, updateViews, uploadVideo, getVideosByUser, getVideosHistory
import uuid,os
app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    videos = getTopVideos()
    isLogged = False
    if('ID' in session):
        isLogged = True
    
    return render_template('index.html', videos = videos, isLogged = isLogged)


@app.route("/video", methods=['POST', 'GET'])
def video():
    isLiked = False
    if request.method == 'POST':
        result = request.form
        id = result['video']
        video = getVideo(id)
        session['watching'] = video
    else:
        if 'video' in request.args:
            id = request.args.get('video')
            video = getVideo(id)
        elif 'watching' in session:
            video = session['watching']
        else:
            redirect(url_for('index'))
        isLiked = request.args.get('liked')

    isLogged = False
    if ('ID' in session): #If logged, should add video into 'Historique'
        handleView(video[0], session['ID'])
        isLiked = isVideoLiked(video[0], session['ID'])
        isLogged = True
        
    if isLiked is None:
        isLiked = False

    video_id = video[0]
    comments = getComments(video_id)

    likes = countLikes(video_id)
    views = countViews(video_id)
    updateViews(video_id)
    
    return render_template('displayVid.html', video = video, isLiked = isLiked, comments = comments, isLogged = isLogged, likes = likes, views = views, autresvideos = getTopVideos())


@app.route("/video/like", methods=['GET','POST'])
def like():
    if request.method == 'POST':
        result = request.form
        id = result['videoID']

        print("vid id:", id)

        if 'ID' in session:
            userID = session['ID']
            isLiked = likeVideo(id, userID)

            return redirect(url_for('video', liked = isLiked))
        
        #Si pas log va dans page de connexion
        return redirect(url_for('login', nextURL = 'video'))

    #Si request pas POST, bah redirige vers index
    return redirect(url_for('index')) 

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

    message = ""

    if 'ID' in session:
        return redirect(url_for('index'))

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
                return redirect(url_for('video', video = session['watching']))
            if nextURL == 'search':
                return redirect(url_for('search', query = session['query']))
            return redirect(url_for(nextURL))

        message = "User not found or wrong password"
        
    
    else: #IF request is GET
        nextURL="index"
        if 'nextURL' in request.args:
            nextURL = request.args['nextURL']
        if 'error' in request.args:
            message = request.args['error']

    # DO A LOGIN PAGE
    return render_template('login.html', nextURL = nextURL, message = message)


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
            return redirect(url_for('login'))
        else:
            video = session['watching']
            texte = request.form['story']
            pseudo = session['username']
            comment_id = str(uuid.uuid4())
            comment_update(comment_id, video, pseudo, texte)
            return redirect(url_for('video', video = video[0]))
            

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


        #Log in
        session['ID'] = userID
        session['username'] = username

        if nextURL == 'video':
            return redirect(url_for('video'), video = session['watching'])
        if nextURL == 'search':
            return redirect(url_for('search'), query = session['query'])

        return redirect(url_for('index'))
    
    message = request.args.get('msg')
    if message is None:
        message = ""
    return render_template('signup.html', msg = message)

# UPLOAD Files stuff
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    
    if 'ID' not in session:
        return redirect(url_for('login', nextURL = 'upload'))

    message = ""

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            message = "No file part"
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            message = "No selected file"
            return redirect(request.url)
        if file and allowed_file(file.filename):

            videoID = str(uuid.uuid4())

            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = videoID + '.' + extension
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            # save the video in DB
            userID = session['ID']
            author = session['username']
            url = "videos/" + filename
            title = request.form['title']
            description = request.form['description']

            uploadVideo(videoID, author, url, title, description, userID)

            return redirect(url_for('index'))
    return render_template('uploadVideo.html', message = message)


#Profile related stuff
@app.route("/my/videos", methods=['GET', 'POST'])
def my_videos():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="my_videos"))
    else:
        userID = session['ID']
        videos = getVideosByUser(userID)
        return render_template('myVideos.html', videos = videos)
    
@app.route("/history", methods=['GET', 'POST'])
def history():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="history"))
    
    userID = session['ID']
    videos = getVideosHistory(userID)
    print('histry: ', videos)
    return render_template('history.html', videos = videos)