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
for i in files_names:
    nom = i.strip("Nomination_").strip(".txt")
    while ord(nom[-1]) > 47 and ord(nom[-1]) < 58:
        nom = nom.strip(nom[-1])
    if nom not in liste_noms:
        liste_noms.append(nom)

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


print(count_IDF())
print(tableau_TFIDF())
clean_txt()


