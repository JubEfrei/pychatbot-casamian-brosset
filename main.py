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
            count[key] = m.log(1/(value/8))

    return count

def count_IDF_pres(directory="./cleaned", liste_nom=liste_noms, liste_p = nom_discours):
    files_names = list_of_files(directory, "txt")
    count = {}
    l = len(liste_nom)
    a = ""
    x = 0
    for i in files_names:
        file = directory + "/" + i
        with open(file=file, mode="r", encoding="UTF8") as read:
            txt = read.readline().strip()
            a += " " + txt
            if x < l and not liste_p[x] == liste_p[x + 1]:
                a = a.split()
                mots = []
                for j in a:
                    if not j in mots:
                        if j in count:
                            count[j] += 1
                        else:
                            count[j] = 1
                        mots.append(j)
                a = ""
        x += 1

    for key, value in count.items():
            count[key] = m.log(1/(value/8))

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




def president_TFIDF(directory = "./cleaned", liste_p = nom_discours, liste_nom=liste_noms):
    files = list_of_files(directory)
    l = len(liste_nom)
    IDF = count_IDF_pres(directory)
    matrice_TFIDF = {}
    for key in IDF.keys():
        matrice_TFIDF[key] = [0 for i in range(l)]
    i = 0
    a = ""
    for x in files:
        file = directory + '/' + x
        with open(file=file, mode="r", encoding="UTF8") as read:
            TF = read.readline().strip()
            a += " " + TF
            if i < l and not liste_p[i] == liste_p[i+1]:
                TF = count_mots(a)
                for key,value in TF.items():
                    matrice_TFIDF[key][i] = IDF[key] * value
                a = ""
            i += 1
    noimp=no_imp_mot(tableau_TFIDF())
    liste_mot = no_imp_mot(matrice_TFIDF)
    for j in range(len(noimp)):
        if noimp[j] in liste_mot:
            liste_mot.remove(noimp[j])
    return




def mot_evo_hors_no_imp():
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
    with open("./cleaned/Nomination_Mitterand1.txt", "r", encoding="UTF8") as f3:
        with open("./cleaned/Nomination_Mitterand2.txt") as f4:
            a=f3.readline()
            b=f4.readline()
            fmi=a+" "+b
    with open("./cleaned/Nomination_Giscard dEstaing.txt", "r", encoding="UTF8") as f5:
        fg=f5.readline()
    with open("./cleaned/Nomination_Hollande.txt", "r", encoding="UTF8") as f6:
        fh=f6.readline()




#print(mot_chirac())
#print(president_eco(tableau_TFIDF()))
#print(mot_chirac())
#print(nation(tableau_TFIDF()))
print(no_imp_mot(tableau_TFIDF()))
print(president_TFIDF())
#print(tableau_TFIDF())

clean_txt()


