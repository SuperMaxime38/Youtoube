import sqlite3, hashlib
def ouvrir_connexion():
    cnx = None
    try:
        cnx = sqlite3.connect('Projet/db/bd_youtube.db')
    except BaseException as e:
        print(e)
    return cnx

def selectionner_livre():
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM livre")
    rows = cur.fetchall()
    cnx.close()
    return rows

def mettre_a_jour_table_livre(resultat):
    
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("INSERT INTO livre VALUES (?, ?, ?, ?)",(resultat['titre'], \
                    resultat['editeur'], resultat['annee'], resultat['isbn']))
    cnx.commit()
    cnx.close()


def getTopVideos():

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Videos")
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
    cur.execute("SELECT * FROM Videos WHERE title LIKE ?", (f"%{query}%",))
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