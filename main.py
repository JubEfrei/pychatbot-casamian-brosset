
from Fonctions import *


run=0
matrice_TF_IDF = tableau_TFIDF()


while run==0:
    fonction=input("entrez le nom d'une fonction pour accéder à celle-ci, entrez '?' pour voir le catalogue des commandes disponibles, ou entrez 'end' pour arreter le programme. ")
    if fonction == "mots non importants":
        print(no_imp_mot(matrice_TF_IDF))
    elif fonction == "mot important":
        print(imp_mot(matrice_TF_IDF))
    elif fonction == "mot de Chirac":
        print(mot_chirac(no_imp_mot(matrice_TF_IDF)))
    elif fonction == "importance de la nation":
        print(nation(matrice_TF_IDF))
    elif fonction == "importance de l'écologie":
        print(president_eco(tableau_TFIDF()))
    elif fonction == "répétiton des présidents":
        print(Pcleaned())
    elif fonction == "matrice":
        print(matrice_TF_IDF)
    elif fonction == "actualiser":
        clean_txt("./cleaned")
        matrice_TF_IDF = tableau_TFIDF()
        print("La matrcie TF-IDF à été actualisé")
    elif fonction == "?":
        print("Voici le catalogue des fonctions disponibles:", " \n"
              "'matrice' : Affiche la matrice TF-IDF", " \n"
              "'mots non importants' : Affiche la liste des mots les moins importants dans le corpus de documents", " \n"
              "'atualiser' : Actualise la matrice TF-IDF apres ajout d'un texte dans le corpus", " \n"                                                                                                    
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
                nouv_matrice = matrice_TFIDF(matrice_TF_IDF)
                discours = doc_pertinent(score_quetion(question, mots_present, score_idf), nouv_matrice)
                mot_important = mot_score_eleve(score_quetion(question, mots_present, score_idf), nouv_matrice[discours])
                print(reponse(QUESTION_STARTER, question), phrase_mot(discours, mot_important))
            else:
                continu = False

    else:
        print("Désolé, cette commande n'existe pas veuillez réessayer ou bien consulter le catalogue des commandes en entrant '?' ")


