import sqlite3
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

    counter=0
    videos = [[]]
    while counter < len(rows):
        row = []
        for i in range(6):
            if counter < len(rows):
                row.append(rows[counter])
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