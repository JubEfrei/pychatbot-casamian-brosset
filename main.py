import os
import math as m


def list_of_files(directory, extension="txt"):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def is_letter(char):
    if 96 < char < 123 or 231 <= char <= 234 or char == 224 or char == 249 or char == 244 or char == 226:
        return True
    return False

def clean_txt(new_directory="./cleaned"):
    directory = "./speeches"
    files_names = list_of_files(directory, "txt")
    for i in files_names:
        file = directory + "/" + i
        new_file = new_directory + "/" + i
        with open(file=file, mode="r", encoding="UTF8") as read, open(file=new_file, mode="w", encoding="UTF8") as write:
            text = read.readlines()
            cln = ""
            for j in text:
                j = j.strip().lower()
                for n in range(len(j)):
                    char = ord(j[n])
                    if char == 32 or is_letter(char):
                        cln += chr(char)
                    elif char == 45 or char == 39:
                        if is_letter(ord(j[n-1])) and is_letter(ord(j[n+1])):
                            cln += " "

                cln += " "
            write.write(cln)



directory = "./speeches"
files_names = list_of_files(directory, "txt")
liste_noms = []
nom_discours = []
for i in files_names:
    nom = i.strip("Nomination_").strip(".txt")
    while ord(nom[-1]) > 47 and ord(nom[-1]) < 58:
        nom = nom.strip(nom[-1])
    if nom not in liste_noms:
        liste_noms.append(nom)
    nom_discours.append(nom)

liste_prenoms=["Jacques","Valérie","François","Emmanuel","François","Nicolas"]
dico_nomp={}
for i in range(len(liste_noms)):
    dico_nomp[liste_noms[i]]=liste_prenoms[i]




def count_mots(txt):
    count = {}
    txt = txt.split()
    for i in txt:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return count

def count_IDF(directory = "./cleaned"):
    files_names = list_of_files(directory, "txt")
    count = {}
    for i in files_names:
        file = directory + "/" + i
        with open(file=file, mode="r", encoding="UTF8") as read:
            txt = read.readline().strip()
            txt = txt.split()
            mots = []
            for j in txt:
                if not j in mots:
                    if j in count:
                        count[j] += 1
                    else:
                        count[j] = 1
                    mots.append(j)

    for key, value in count.items():
            count[key] = m.log10(1/(value/8))
    return count


def tableau_TFIDF(directory = "./cleaned"):
    files = list_of_files(directory)
    l = len(files)
    IDF = count_IDF(directory)
    matrice_TFIDF = {}
    for key in IDF.keys():
        matrice_TFIDF[key] = [0 for i in range(l)]
    i = 0
    for x in files:
        file = directory + '/' + x
        with open(file=file, mode="r", encoding="UTF8") as read:
            TF = count_mots(read.readline().strip())
        for key,value in TF.items():
            matrice_TFIDF[key][i] = IDF[key] * value
        i += 1
    return matrice_TFIDF

def no_imp_mot(dico):
    L=[]
    for c,value in dico.items():
        i=0
        for valeur in value:
            i+=valeur
        if i==0:
            L.append(c)
    return(L)

def imp_mot(dico):
    max=0
    mot_max=None
    for c,value in dico.items():
        i=0
        for valeur in value:
            i+=valeur
        if i>max:
            mot_max=c
    return(mot_max)


def mot_chirac():
    with open("./cleaned/Nomination_Chirac1.txt", "r") as f1:
        with open("./cleaned/Nomination_Chirac2.txt") as f2:
            a=f1.readline()
            b=f2.readline()
            f=a+" "+b
    dico=count_mots(f)
    max = 0
    mot_max = None
    for c, value in dico.items():
        if value > max:
            mot_max = c
    return(c)

def nation(dico, l_p = nom_discours):
    na = dico["nation"]
    president = {}
    for i in l_p:
        president[i] = 0
    for i in range(len(na)):
        president[l_p[i]] += na[i]
    max = 0
    nom = ""
    for key, value in president.items():
        if max < value:
            max = value
            nom = key
    return (list(president.keys()), nom)

def president_eco(dico, l_p = nom_discours):
    climat = dico["climat"]
    for i in range(len(climat)):
        if climat[i] != 0:
            return l_p[i]

def Pcleaned(directory = "./cleaned", n_directory = "./PCleaned", liste_nom=liste_noms, liste_p=nom_discours):
    files_names = list_of_files(directory, "txt")
    i = 0
    j = 0
    l = len(liste_p) - 1
    a = ""
    nouv_liste = []
    for y in range(len(liste_noms)):
        mot = ""
        for v in range(len(liste_noms[y])):
            if liste_nom[y][v] != " ":
                mot += liste_noms[y][v]
            else:
                mot += "_"
        nouv_liste.append(mot)

    for f in files_names:
        file = directory + "/" + f
        with open(file=file, mode="r", encoding="UTF8") as read:
            txt = read.readline().strip()
            a += " " + txt
            if i < l and liste_p[i] != liste_p[i + 1]:
                n_f = n_directory + "/" + liste_nom[j]
                with open(file=n_f, mode="w", encoding="UTF8") as write:
                    write.write(a)
                a = ""
                j += 1
        i += 1
        n_f = n_directory + "/" + nouv_liste[j]
        with open(file=n_f, mode="w", encoding="UTF8") as write:
            write.write(a)

    matrice = tableau_TFIDF(directory="./PCleaned")
    print(matrice)
    noimp = no_imp_mot(tableau_TFIDF())
    liste_mot = no_imp_mot(matrice)
    for j in range(len(noimp)):
        if noimp[j] in liste_mot:
            liste_mot.remove(noimp[j])
    return liste_mot

def question(phrase):
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
    mots_present = []
    for i in mots:
        if i in matrice:
            mots_present.append(i)
    return mots_present

def score_quetion(mots, mots_present, matrice_IDF):
    matrice_mots = {}
    for i in mots:
        if i in mots_present:
            if i in matrice_mots:
                matrice_mots[i] += 1
            else:
                matrice_mots[i] = 1
    for key, value in matrice_IDF.items():
        if key in matrice_mots:
            matrice_mots[key] *= value
        else:
            matrice_mots[key] = 0
    return matrice_mots

def matrice_TFIDF(matrice):
    new_matrice = {}

    for key, values in matrice.items():
        for i, value in enumerate(values):
            doc_key = f"Doc {i+1}"
            if doc_key not in new_matrice:
                new_matrice[doc_key] = {}
            new_matrice[doc_key][key] = value

    return new_matrice

def produit_scalaire(a, b):
    res = 0
    for key in a.keys():
        res += a[key] * b[key]
    return res

def norme_vecteur(a):
    res = 0
    for value in a.values():
        res += value ** 2
    return m.sqrt(res)

def calcul_similarite(a, b):
    return produit_scalaire(a, b) / (norme_vecteur(a) * norme_vecteur(b))

def doc_pertinent(questionTFIDF, matriceTFIDF):
    score_max = (0, 0)
    for key, value in matriceTFIDF.items():
        print(value)
        simil = calcul_similarite(questionTFIDF, value)
        if simil > score_max[0]:
            score_max = (simil, key)
    return score_max[1]

b = matrice_TFIDF(tableau_TFIDF())

question = question(input("Poser une question"))
matrice = tableau_TFIDF()
score_idf = count_IDF()
mots_present = identif_quest(question, matrice)
a = score_quetion(question, mots_present, score_idf)
print(a)
print(doc_pertinent(a, b))



"""def mot_evo_hors_no_imp():
    files = list_of_files(directory)
    l = len(files)
    IDF = count_IDF(directory)
    matrice_TFIDF = {}
    for key in IDF.keys():
        matrice_TFIDF[key] = [0 for i in range(l)]
    i = 0
    with open("./cleaned/Nomination_Chirac1.txt", "r", encoding="UTF8") as f1:
        with open("./cleaned/Nomination_Chirac2.txt") as f2:
            a=f1.readline()
            b=f2.readline()
            fc=a+" "+b
    with open("./cleaned/Nomination_Mitterrand1.txt", "r", encoding="UTF8") as f3:
        with open("./cleaned/Nomination_Mitterrand2.txt") as f4:
            a=f3.readline()
            b=f4.readline()
            fmi=a+" "+b
    with open("./cleaned/Nomination_Giscard dEstaing.txt", "r", encoding="UTF8") as f5:
        fg=f5.readline()
    with open("./cleaned/Nomination_Hollande.txt", "r", encoding="UTF8") as f6:
        fh=f6.readline()"""
""" 
question = question(input("Poser une question"))
matrice = tableau_TFIDF()
score_idf = count_IDF()
mots_present = identif_quest(question, matrice)
print(question, mots_present)
print(score_quetion(question, mots_present, score_idf))


#########################################################################################################
############################################ PROGRAMME PRINCIPAL ########################################
run=0
while run==0:
    fonction=input("entrez le nom d'une fonction pour accéder à celle-ci, entrez '?' pour voir le catalogue des commandes disponibles, ou entrez 'end' pour arreter le programme. ")
    if fonction=="no_imp_mot()":
        print(no_imp_mot(tableau_TFIDF()))
    elif fonction=="imp_mot()":
        print(imp_mot(tableau_TFIDF()))
    elif fonction=="mot_chirac()":
        print(mot_chirac())
    elif fonction=="nation()":
        print(nation(tableau_TFIDF()))
    elif fonction=="president_eco()":
        print(president_eco(tableau_TFIDF()))
    elif fonction=="president_TFIDF()":
        print(president_TFIDF())
    elif fonction=="Pcleaned()":
        print(Pcleaned())
    elif fonction == "matrice()":
        print(tableau_TFIDF())
    elif fonction=="?":
        print("Voici le catalogue des fonctions disponibles:", " \n"
              "matrice() : Affiche la matrice TF-IDF"
              "no_imp_mot() : Affiche la liste des mots les moins importants dans le corpus de documents", " \n"
              "imp_mot() : Affiche le(s) mot(s) ayant le score TD-IDF le plus élevé", " \n"
              "mot_chirac() : Indique le(s) mot(s) le(s) plus répété(s) par le président Chirac", " \n"
              "nation() : Indique le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois", " \n"
              "president_eco() : Indique le premier président à parler du climat et/ou de l’écologie, \n"
              "president_TFIDF() : Hormis les mots dits « non importants », affiche le(s) mot(s) que tous les présidents ont évoqués", " \n"
              "Pcleaned() : Hormis les mots dits « non importants », affiche le(s) mot(s) que tous les présidents ont évoqués", " \n")
    elif fonction=="end":
        run=1
    else:
        print("Désolé, cette commande n'existe pas veuillez réessayer ou bien consulter le catalogue des commandes en entrant '?' ")







#print(mot_chirac())
#print(president_eco(tableau_TFIDF()))
#print(mot_chirac())
#print(nation(tableau_TFIDF()))
#print(no_imp_mot(tableau_TFIDF()))
#print(president_TFIDF())
print(tableau_TFIDF())

clean_txt()
"""

