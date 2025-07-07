import sqlite3, hashlib, time
def ouvrir_connexion():
    cnx = None
    try:
        cnx = sqlite3.connect('Projet/db/bd_youtube.db')
    except BaseException as e:
        print(e)
    return cnx


def getTopVideos():

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Videos")
    rows = cur.fetchall()
    cnx.close()

    return getVideoTable(rows)

def getTendances():

    cnx = ouvrir_connexion()
    cur = cnx.cursor() 
    cur.execute("SELECT * FROM Videos ORDER BY views DESC")
    rows = cur.fetchall()
    cnx.close()

    return getVideoTable(rows)

def getVideoTable(videoList: list):
    
    
    counter=0
    videos = [[]]
    while counter < len(videoList):
        row = []
        for _ in range(6):
            if counter < len(videoList):
                row.append(videoList[counter])
                counter += 1
            else:
                break
        videos.append(row)

    return videos

def getVideo(videoId):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Videos WHERE id = ?", (videoId,))
    rows = cur.fetchall()
    cnx.close()

    return rows[0]


def research(query):

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Videos WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%"))
    rows = cur.fetchall()
    cnx.close()

    print(getVideoTable(rows))

    return getVideoTable(rows)

def db_identification(resultat):
    #hachage du mot de passe
    password = hashlib.sha256()
    password.update(bytes(resultat['password'], 'utf-8'))
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * \
    FROM Utilisateurs\
    WHERE pseudo = ? AND password = ?",\
    (resultat['login'], password.hexdigest()))
    rows = cur.fetchall()
    cnx.close()
    return rows

def comment_update(comment_id, video, pseudo, texte):
    
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("INSERT INTO Commentaires VALUES (?, ?, ?, ?)",(comment_id, \
                    video[0], pseudo, texte))
    cnx.commit()
    cnx.close()

def addUser(uuid, pseudo, mail, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    
    cnx = ouvrir_connexion()
    cur = cnx.cursor()

    cur.execute("SELECT * FROM Utilisateurs WHERE adr_mail = ?", (mail,))
    rows = cur.fetchall()
    if len(rows) != 0:
        return False

    cur.execute("INSERT INTO Utilisateurs VALUES (?, ?, ?, ?)",(uuid, \
                    mail, pseudo, password.hexdigest()))
    cnx.commit()
    cnx.close()
    return True


def getUser(uuid):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Utilisateurs WHERE userID = ?", (uuid,))
    rows = cur.fetchall()
    cnx.close()
    return rows[0] # retourne UN tuple (sinon renvoie une liste de 1 tuple donc c'est useless)

def changePassword(uuid, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    print("old psswrd: ", password.hexdigest())
    print("uid: ", uuid)

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("UPDATE Utilisateurs SET password = ? WHERE userID = ?", (password.hexdigest(), uuid))
    cnx.commit()
    cnx.close()

def handleView(videoID, userID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Historique WHERE userID = ? AND videoID = ?", (userID, videoID))
    rows = cur.fetchall()

    print("if it exists it's printed here", rows)
    date = time.time()//1

    if len(rows) == 0:
        cur.execute("INSERT INTO Historique VALUES (?, ?, ?, ?)", (videoID, userID, date, False))
        cnx.commit()
    else:
        cur.execute("UPDATE Historique SET date = ? WHERE userID = ? AND videoID = ?", (date, userID, videoID))
        cnx.commit()
    
    cur.execute("SELECT * FROM Historique WHERE userID = ? AND videoID = ?", (userID, videoID))
    rows = cur.fetchall()
    cnx.close()
    return rows

def likeVideo(videoID, userID):
    vid = handleView(videoID, userID)

    cnx = ouvrir_connexion()
    cur = cnx.cursor()

    isVidLiked = False
    print(vid)
    if vid[0][3] == False: # Si la vidéo n'est pas likée
        
        cur.execute("UPDATE Historique SET like = ? WHERE userID = ? AND videoID = ?", (True, userID, videoID))
        isVidLiked = True
    else:
        cur.execute("UPDATE Historique SET like = ? WHERE userID = ? AND videoID = ?", (False, userID, videoID))
    
    cnx.commit()
    cnx.close()
    return isVidLiked


def isVideoLiked(videID, userID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Historique WHERE userID = ? AND videoID = ?", (userID, videID))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return False

    return rows[0][3]

def getComments(id):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT* FROM Commentaires WHERE id_video = ?", (id,))
    rows = cur.fetchall()
    cnx.close()
    return rows

def countViews(videoID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT COUNT(*) FROM Historique WHERE videoID=?", (videoID,))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return 0

    return rows[0][0] # ya qu'un élément qui est le nombre de vues


def updateViews(videoID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    views = countViews(videoID)
    cur.execute("UPDATE Videos SET views = ? WHERE id = ?", (views, videoID))
    cnx.commit()
    cnx.close()

def countLikes(videoID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT COUNT(*) FROM Historique WHERE videoID=? and like = 1", (videoID,))
    rows = cur.fetchall()
    cnx.close()

    
    if len(rows) == 0:
        return 0

    return rows[0][0] # ya qu'un élément qui est le nombre de likes


def uploadVideo(videoID, author, url, title, description, userID, isPrivate):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("INSERT INTO Videos VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (videoID, author, url, title, 0, description, userID, isPrivate))
    cnx.commit()
    cnx.close()

def updateVideo(videoID, title, description, isPrivate):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("UPDATE Videos SET title = ?, description = ?, isPrivate = ? WHERE id = ?", (title, description, isPrivate, videoID))

    if isPrivate == True:
        cur.execute("SELECT userID FROM Videos WHERE id = ?", (videoID,))
        rows = cur.fetchall()

        if len(rows) == 0:
            return

        userID = rows[0][0]

        cur.execute("INSERT INTO PrivateVideosAuthorization VALUES (?, ?)", (videoID, userID))
    else:
        cur.execute("DELETE FROM PrivateVideosAuthorization WHERE videoID = ?", (videoID,))

    cnx.commit()
    cnx.close()

def getUserFromMail(mail):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT userID FROM Utilisateurs WHERE adr_mail = ?", (mail,))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return None

    return rows[0][0]

def getMailFromUser(userID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT adr_mail FROM Utilisateurs WHERE userID = ?", (userID,))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return None

    return rows[0][0]

def addMember(videoID, mail):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    
    userID = getUserFromMail(mail)

    if len(userID) == None:
        return

    cur.execute("INSERT INTO PrivateVideosAuthorization VALUES (?, ?)", (videoID, userID))
    cnx.commit()
    cnx.close()

def updatePrivateMembers(videoID, members):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("DELETE FROM PrivateVideosAuthorization WHERE videoID = ?", (videoID,))
    for member in members:
        cur.execute("INSERT INTO PrivateVideosAuthorization VALUES (?, ?)", (videoID, member))
    cnx.commit()
    cnx.close()

def getPrivateMembers(videoID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT userID FROM PrivateVideosAuthorization WHERE videoID = ?", (videoID,))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return []

    return rows[0]

def removeMember(videoID, mail):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()

    userID = getUserFromMail(mail)

    if len(userID) == None:
        return

    cur.execute("DELETE FROM PrivateVideosAuthorization WHERE videoID = ? AND userID = ?", (videoID, userID))
    cnx.commit()
    cnx.close()

def deleteVideo(videoID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("DELETE FROM Videos WHERE id = ?", (videoID,))
    cur.execute("DELETE FROM Historique WHERE videoID = ?", (videoID,))
    cur.execute("DELETE FROM Commentaires WHERE id_video = ?", (videoID,))
    cur.execute("DELETE FROM PrivateVideosAuthorization WHERE videoID = ?", (videoID,))
    cnx.commit()
    cnx.close()

def getVideosByUser(userID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Videos WHERE userID = ?", (userID,))
    rows = cur.fetchall()
    cnx.close()
    return rows

def getVideosHistory(userID):
    """
    gets the video locations
    """
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT videoID FROM Historique WHERE userID = ? ORDER BY CAST(\"DATE\" AS INTEGER) DESC;", (userID,))
    rows = cur.fetchall()
    cnx.close()

    result = []
    for row in rows:
        result.append(getVideo(row[0]))
    return result