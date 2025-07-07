from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from .modele import getTopVideos, getVideo, research, db_identification, comment_update, addUser, getUser, changePassword, handleView, likeVideo, isVideoLiked, getComments, countLikes, countViews, updateViews, uploadVideo, getVideosByUser, getVideosHistory, getTendances, updateVideo, updatePrivateMembers, addMember, getPrivateMembers, removeMember, deleteVideo, canUserWatch, getMailFromUser
import uuid,os
app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    isLogged = False
    if('ID' in session):
        isLogged = True
        videos = getTopVideos(session['ID'])
    else:
        videos = getTopVideos()

    return render_template('index.html', videos = videos, isLogged = isLogged, mainSelected = True)


@app.route("/trends", methods=['GET', 'POST'])
def trends():
    isLogged = False
    if('ID' in session):
        isLogged = True
        videos = getTendances(session['ID'])
    else:
        videos = getTendances()

    return render_template('index.html', videos = videos, isLogged = isLogged, mainSelected = False)

@app.route("/video", methods=['POST', 'GET'])
def video():
    isLiked = False
    video_id = -1
    video = []
    if request.method == 'POST':
        result = request.form
        id = result['video']
        video = getVideo(id)
        session['watching'] = video
        video_id = id
        print("request: " , video)
    else:
        if 'video' in request.args:
            id = request.args.get('video')
            video_id = id
            video = getVideo(id)
            session['watching'] = video
        elif 'watching' in session:
            video = session['watching']
            video_id = video[0]
        else:
            redirect(url_for('index'))
        isLiked = request.args.get('liked')

    isLogged = False
    if ('ID' in session): #If logged, should add video into 'Historique'
        handleView(video_id, session['ID'])
        isLiked = isVideoLiked(video_id, session['ID'])
        isLogged = True
        
    if isLiked is None:
        isLiked = False
    comments = getComments(video_id)

    likes = countLikes(video_id)
    views = countViews(video_id)
    updateViews(video_id)

    print(video)
    
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
    isLogged = False
    if('ID' in session):
        isLogged = True
    if request.method == 'POST':
        query = request.form['query']
        if isLogged:
            videos = research(query, session['ID'])
        else:
            videos = research(query)
        session['videos'] = videos
        session['query'] = query
    else:
        videos = session['videos']
        query = session['query']

    return render_template('search.html', videos = videos, query = query, isLogged = isLogged)

@app.route("/login", methods=['GET', 'POST'])
def login():

    message = ""

    if 'ID' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
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

        return render_template('account.html', user = user, msg = msg, color = color, isLogged = True)


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
            return redirect(url_for('upload'), message = message)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            message = "No selected file"
            return redirect(url_for('upload'), message = message)
        if file and allowed_file(file.filename):

            videoID = str(uuid.uuid4())

            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = videoID + '.' + extension
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            # save the video in DB
            userID = session['ID']
            author = session['username']
            url = 'videos/' +filename
            title = request.form['title']
            description = request.form['description']
            
            checkbox_value = request.form.get('is_private')
            if checkbox_value:
                isPrivate = True
                addMember(videoID, getMailFromUser(userID)) #the author can see his own video
            else:
                isPrivate = False


            print("is private: ", isPrivate)

            uploadVideo(videoID, author, url, title, description, userID, isPrivate)

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
        return render_template('myVideos.html', videos = videos, isLogged = True)
    
@app.route("/manage", methods=['GET', 'POST'])
def manage_video():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="my_videos"))

    if request.method == 'POST':

        videoID = request.form['video']
    else:
        videoID = session['watching'][0]

    video = getVideo(videoID)
    session['watching'] = video

    members = []
    for id in getPrivateMembers(videoID):
        print(id)
        members.append(getUser(id))

    return render_template('manage_video.html', video = video, isLogged = True, members = members)
    


@app.route("/manage/update", methods=['GET', 'POST'])
def update_video():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="my_videos"))
    
    if request.method == 'POST':
        videoID = request.form['id']
        title = request.form['title']
        description = request.form['description']
        
        checkbox_value = request.form.get('is_private')
        if checkbox_value:
            isPrivate = True
        else:
            isPrivate = False

        print("is private: ", isPrivate)

        updateVideo(videoID, title, description, isPrivate)

    else:
        videoID = session['watching'][0]

    members = []
    for id in getPrivateMembers(videoID):
        members.append(getUser(id))


    print("updated video !")

    return redirect(url_for('manage_video', video = getVideo(videoID), members = members))
    
@app.route("/manage/addMember", methods=['GET', 'POST'])
def add_member():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="my_videos"))
    
    if request.method == 'POST':
        videoID = request.form['video']
        email = request.form['email']

        addMember(videoID, email)
        video = getVideo(videoID)
        members = []
        for id in getPrivateMembers(videoID):
            members.append(getUser(id))

        return redirect(url_for('manage_video', video = video, members = members))

@app.route("/manage/removeMember", methods=['GET', 'POST'])
def remove_member():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="my_videos"))
    
    if request.method == 'POST':
        videoID = request.form['video']
        email = request.form['email']

        removeMember(videoID, email)
        video = getVideo(videoID)
        members = []
        for id in getPrivateMembers(videoID):
            members.append(getUser(id))

        return redirect(url_for('manage_video', video = video, members = members))

@app.route("/manage/delete", methods=['GET', 'POST'])
def delete_video():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="my_videos"))
    
    if request.method == 'POST':
        data = request.get_json()
        videoID = data['video']

        video = getVideo(videoID)
        filename = video[2].split("/", 1)[1]

        deleteVideo(videoID)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(path):
            os.remove(path)

        return jsonify({'success': True})

@app.route("/history", methods=['GET', 'POST'])
def history():
    if 'ID' not in session:
        return redirect(url_for('login', nextURL="history"))
    
    userID = session['ID']
    videos = getVideosHistory(userID)
    return render_template('history.html', videos = videos, isLogged = True)