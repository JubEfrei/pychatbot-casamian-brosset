import os
import math as m

def list_of_files(dossier, extension="txt"):
    """Renvoie la liste des fichiers dans le dossier donné"""
    files_names = []
    for filename in os.listdir(dossier):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


QUESTION_STARTER={
    'pourquoi':'Car,',
    'peux tu':'Oui, bien sûr !',
    'comment':'Après analyse,'
}
liste_noms = list_of_files("./speeches")
liste_prenoms = ["Jacques","Jacques","Valérie","François","Emmanuel","François","François","Nicolas"]
dico_nomp = {}
nom_discours=[]

def is_letter(char):
    if 96 < char < 123 or 231 <= char <= 234 or char == 224 or char == 249 or char == 244 or char == 226:
        return True
    return False

def clean_txt(nouveau_dossier="./cleaned"):
    """Prend en entré un dossier dans lequel il va réécrire tous les textes du fichier principale
    sous la forme d'une liste de mots"""
    dossier = "./speeches"
    files_names = list_of_files(dossier, "txt")
    for i in files_names:
        fichier = dossier + "/" + i
        nouv_fichier = nouveau_dossier + "/" + i
        with open(file=fichier, mode="r", encoding="UTF8") as read, open(file=nouv_fichier, mode="w", encoding="UTF8") as write:
            text = read.readlines()
            clean = ""
            for j in text:
                j = j.strip().lower()
                for n in range(len(j)):
                    char = ord(j[n])
                    if char == 32 or is_letter(char):
                        clean += chr(char)
                    elif char == 45 or char == 39:
                        if is_letter(ord(j[n-1])) and is_letter(ord(j[n+1])):
                            clean += " "

def count_mots(txt):
    """Prend une liste de mots et renvoie un dictionnaire avec comme clé chaque mots du texte et comme valeur
    leur nombre d'appariton dans la liste"""
    compte = {}
    txt = txt.split()
    for i in txt:
        if i in compte:
            compte[i] += 1
        else:
            compte[i] = 1
    return compte

def count_IDF(dossier ="./cleaned"):
    """Prend comme entrée un corpus de document et renvoie un dictionnaire avec chaque mot du corpus
    comme clé et comme valeur leur score IDF"""
    files_names = list_of_files(dossier, "txt")
    compte = {}
    for i in files_names:
        file = dossier + "/" + i
        with open(file=file, mode="r", encoding="UTF8") as read:
            txt = read.readline().strip()
            txt = txt.split()
            mots = []
            for j in txt:
                if not j in mots:
                    if j in compte:
                        compte[j] += 1
                    else:
                        compte[j] = 1
                    mots.append(j)

    for cle, value in compte.items():
            compte[cle] = m.log10(1/(value/8))
    return compte


def tableau_TFIDF(dossier ="./cleaned"):
    """Prends comme entrée un dossier et renvoie la matrice TF-IDF de ce dossier sous forme de dictionnaire"""
    fichiers = list_of_files(dossier)
    l = len(fichiers)
    IDF = count_IDF(dossier)
    matrice_TFIDF = {}
    for cle in IDF.keys():
        matrice_TFIDF[cle] = [0 for i in range(l)]
    i = 0
    for x in fichiers:
        fichier = dossier + '/' + x
        with open(file=fichier, mode="r", encoding="UTF8") as read:
            TF = count_mots(read.readline().strip())
        for cle,valeur in TF.items():
            matrice_TFIDF[cle][i] = IDF[cle] * valeur
        i += 1
    return matrice_TFIDF

def no_imp_mot(dico):
    """Prends une matrice TF-IDF comme entrée et renvoie la liste des mots non importants."""
    L=[]
    for c,value in dico.items():
        i=0
        for valeur in value:
            i+=valeur
        if i==0:
            L.append(c)
    return(L)

def imp_mot(dico):
    """Prend comme entrée une matrice TF-IDF et renvoie le mot avec le score TF-IDF le plus élevé"""
    max=0
    mot_max=None
    for c,value in dico.items():
        i=0
        for valeur in value:
            i+=valeur
        if i>max:
            mot_max=c
    return(mot_max)


def mot_chirac(liste_mot_no_imp):
    """Prend comme entrée une liste de mot non important et renvoi le moty le plus dit par Chirac
    (qui n'est pas un moit dit non important)"""
    with open("./cleaned/Nomination_Chirac1.txt", "r") as f1:
        with open("./cleaned/Nomination_Chirac2.txt") as f2:
            a=f1.readline()
            b=f2.readline()
            f=a+" "+b
    dico=count_mots(f)
    max = 0
    mot_max = None
    for cle, valeur in dico.items():
        if valeur > max and cle not in liste_mot_no_imp:
            mot_max = cle
            max = valeur
    return(mot_max)

def nation(dico, l_p = nom_discours):
    """Prend comme paramètre la matrice TFIDF et la liste des présidents puis renvoie le président qui parle le
    plus de la nation et combien de fois il en parle"""
    TFIDF_nation = dico["nation"]
    president = {}
    for i in l_p:
        president[i] = 0
    for i in range(len(TFIDF_nation)):
        president[l_p[i]] += TFIDF_nation[i]
    max = 0
    nom = ""
    for cle, valeur in president.items():
        if max < valeur:
            max = valeur
            nom = cle
    return (list(president.keys()), nom)

def president_eco(dico, l_p = nom_discours):
    """Pend comme paramètre l matrice TF-IDf et la liste des président et renvoie ceux qui
    parle de climat ou d'ecologie"""
    climat = dico["climat"]
    ecologie = dico["écologie"]
    liste_pres = []
    for i in range(len(climat)):
        if climat[i] != 0:
            liste_pres.append(l_p[i])
    for i in range(len(ecologie)):
        if ecologie[i] != 0:
            if l_p[i] not in liste_pres:
                liste_pres.append(l_p[i])
    return liste_pres

def Pcleaned(dossier ="./cleaned", nouv_dossier ="./PCleaned", liste_nom=liste_noms, liste_p=nom_discours):
    """Prend en paramètre le dossier des texte déja traité, un nouveau dossier de sortie, la liste des président et
    la liste qui associe chaque discours à un président pui regroupe tout les discours différents des même président
    sous un même dossier permettant la création d'un nouveau corpus de documents ou chaque fichier ne correspond plus
    à un discour mais à un président"""
    files_names = list_of_files(dossier, "txt")
    i = 0
    j = 0
    longeur = len(liste_p) - 1
    discours = ""
    nouv_liste = []

    for y in range(len(liste_noms)):           #Remplace le " " de Giscard dEstaing par un tiret
        mot = ""
        for v in range(len(liste_noms[y])):
            if liste_nom[y][v] != " ":
                mot += liste_noms[y][v]
            else:
                mot += "_"
        nouv_liste.append(mot)

    for f in files_names:
        fichier = dossier + "/" + f
        with open(file=fichier, mode="r", encoding="UTF8") as read:    #regroupe les discours sous le même président
            txt = read.readline().strip()
            discours += " " + txt
            if i < longeur and liste_p[i] != liste_p[i + 1]:
                n_f = nouv_dossier + "/" + liste_nom[j]
                with open(file=n_f, mode="w", encoding="UTF8") as write:
                    write.write(discours)
                discours = ""
                j += 1
        i += 1
        n_f = nouv_dossier + "/" + nouv_liste[j]                     #ajoute les discours dans le nouveau dossier
        with open(file=n_f, mode="w", encoding="UTF8") as write:
            write.write(discours)

    matrice = tableau_TFIDF(dossier="./PCleaned")                   #Fait la liste des mots dits par tous les présidents
    noimp = no_imp_mot(tableau_TFIDF())                             #qui ne sont pas dans les mots dit non important
    liste_mot = no_imp_mot(matrice)

    for j in range(len(noimp)):
        if noimp[j] in liste_mot:
            liste_mot.remove(noimp[j])
    return liste_mot

def traitement_question(phrase):
    """Prend en paramètre une phrase, une question par exemple, et renvoi la liste des mots de la question"""
    mots = phrase.lower().split()
    res = []
    for i in range(len(mots)):
        mot = ""
        for j in range(len(mots[i])):
            if is_letter(ord(mots[i][j])):
                mot += mots[i][j]
            else:
                if mot != "":
                    res.append(mot)
                    mot = ""
        if mot != "":
            res.append(mot)
    return res

def identif_quest(mots:list, matrice:dict):
    """Prend en paramètre une liste de mots et une matrice TF-IDF et renvoi la liste des mots
    non présent dans la matrice TF-IDF"""
    mots_present = []
    for i in mots:
        if i in matrice:
            mots_present.append(i)
    return mots_present

def score_quetion(mots, mots_present, matrice_IDF):
    """Prend en paramètre une liste de mot, la liste de ces mots présents dans la matrice TF-IDF et la matrice elle même
    et retourne un vecteur de cette matrice avec les scores TF-IDF de la question"""
    matrice_mots = {}
    for i in mots:
        if i in mots_present:
            if i in matrice_mots:
                matrice_mots[i] += 1
            else:
                matrice_mots[i] = 1
    for cle, value in matrice_IDF.items():
        if cle in matrice_mots:
            matrice_mots[cle] *= value
        else:
            matrice_mots[cle] = 0
    return matrice_mots

def matrice_TFIDF(matrice,files_names=liste_noms):
    """Prend en paramètre une matrice TF-IDF sous sa forme losrs de sa création et renvoi cette matrice sous la nouvelle
    forme qui est un documentaire avec comme clé les différents documents et comme valeurs un autre dictionnaire
    contenant comme clé les différents mots et comme valeur leur score TF-IDF"""
    new_matrice = {}
    for cle, values in matrice.items():
        for i, value in enumerate(values):
            cle_doc = files_names[i]
            if cle_doc not in new_matrice:
                new_matrice[cle_doc] = {}
            new_matrice[cle_doc][cle] = value

    return new_matrice

def produit_scalaire(a, b):
    """Prend deux vecteurs et renvoi leur produit scalaire"""
    res = 0
    for cle in a.keys():
        res += a[cle] * b[cle]
    return res

def norme_vecteur(a):
    """Prend comme paramètre un vecteur et renvoi sa norme"""
    res = 0
    for value in a.values():
        res += value ** 2
    return m.sqrt(res)

def calcul_similarite(a, b):
    """Calcul la similarité cosinus entre deux vecteurs"""
    return produit_scalaire(a, b) / (norme_vecteur(a) * norme_vecteur(b))

def doc_pertinent(questionTFIDF, matriceTFIDF):
    """Prend comme entrée le vecteur TF-IDF de la question et la matrice TF-IDF sous sa deuxième forme et retourne le
    document avec la plus similarité cosinus"""
    score_max = (0, 0)
    for cle, value in matriceTFIDF.items():
        simil = calcul_similarite(questionTFIDF, value)
        if simil > score_max[0]:
            score_max = (simil, cle)
    return score_max[1]

b = matrice_TFIDF(tableau_TFIDF())
def mot_score_eleve(matrice):
    """Renvoie le mot ayant le score le + élevé dans la matrice, et prend en parametre la matrice"""
    max=0
    mot=""
    for cle, value in matrice.items():
            if value>max:
                max=value
                mot=cle
    return mot

def phrase_mot(doc,mot_imp):
    """Retrouve la 1ere phrase dans un discours dans lequel apparait le mot ayant le + haut score
    de la question et la renvoie"""
    ch="./Speeches/"
    doc=ch + doc
    with open(doc, "r", encoding='utf-8') as f:
        for l in f:
            if mot_imp in l:
                return str(l.strip())



def reponse(dico, quest):
    """Mise en forme des réponses, prend en parametre la question et le dico "question_starters"""
    for cle, val in dico.items():
        if cle in quest:
            return str(val)
        else:
            return ""


#########################################################################################################
#########################################################################################################
#Attribution des noms aux présiendents, avec un liste de noms, une liste de nom par rapport aux discours
# et un dictionnaire de nom et de prénom

for i in range(len(liste_noms)):
    dico_nomp[liste_noms[i]]=liste_prenoms[i]

for i in liste_noms:
    nom = i.strip("Nomination_").strip(".txt")
    while 47 < ord(nom[-1]) < 58:
        nom = nom.strip(nom[-1])
    if nom not in liste_noms:
        liste_noms.append(nom)
    nom_discours.append(nom)

#########################################################################################################
############################################ PROGRAMME PRINCIPAL ########################################
run=0
while run==0:
    fonction=input("entrez le nom d'une fonction pour accéder à celle-ci, entrez '?' pour voir le catalogue des commandes disponibles, ou entrez 'end' pour arreter le programme. ")
    if fonction=="mot non importants":
        print(no_imp_mot(tableau_TFIDF()))
    elif fonction=="mot important":
        print(imp_mot(tableau_TFIDF()))
    elif fonction=="mot de Chirac":
        print(mot_chirac(no_imp_mot(tableau_TFIDF())))
    elif fonction=="importance de la nation":
        print(nation(tableau_TFIDF()))
    elif fonction=="importance de l'écologie":
        print(president_eco(tableau_TFIDF()))
    elif fonction=="répétiton des présidents":
        print(Pcleaned())
    elif fonction == "matrice":
        print(tableau_TFIDF())
    elif fonction=="?":
        print("Voici le catalogue des fonctions disponibles:", " \n"
              "'matrice' : Affiche la matrice TF-IDF"
              "'mot non importants' : Affiche la liste des mots les moins importants dans le corpus de documents", " \n"
              "'mot important' : Affiche le(s) mot(s) ayant le score TD-IDF le plus élevé", " \n"
              "'mot de Chirac' : Indique le(s) mot(s) le(s) plus répété(s) par le président Chirac", " \n"
              "'importance de la nation' : Indique le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois", " \n"
              "'importance de l'écologie' : Indique le premier président à parler du climat et/ou de l’écologie, \n"
              "'répétiton des présidents' : Hormis les mots dits « non importants », affiche le(s) mot(s) que tous les présidents ont évoqués", " \n"
              "'ChatBot' : Ouvre le mode Chat bot, entrée end pour en sortir", " \n")
    elif fonction=="end":
        run=1
    elif fonction == "Chatbot":
        continu = True
        while continu:
            demande = input("Poser une question ('end' pour quitter le Chatbot): ")
            if demande != "end":
                question = traitement_question(demande)
                matrice = tableau_TFIDF()
                score_idf = count_IDF()
                mots_present = identif_quest(question, matrice)
                print(reponse(QUESTION_STARTER, question), phrase_mot(
                    doc_pertinent(score_quetion(question, mots_present, score_idf), matrice_TFIDF(tableau_TFIDF())),
                    mot_score_eleve(score_quetion(question, mots_present, score_idf))))
            else:
                continu = False

    else:
        print("Désolé, cette commande n'existe pas veuillez réessayer ou bien consulter le catalogue des commandes en entrant '?' ")


