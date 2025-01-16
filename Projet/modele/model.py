import sqlite3
def ouvrir_connexion():
    cnx = None
    try:
        cnx = sqlite3.connect('Projet/db/livres.db')
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