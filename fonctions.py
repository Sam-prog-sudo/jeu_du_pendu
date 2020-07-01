#-*- coding: utf8 -*-

import string
import random as rand
import pickle as pkl
import os
from donnees import *
from affichage import *


#--------------------------------SCORE------------------------------#

def scores_existes_tu(): 
    """Cette fonction récupère les scores enregistrés,
    et créer le fichier s'il n'exite pas.
    
    Dans tous les cas, elle retourne un dictionnaire: 
    -soit le dico contient l'objet dépicklé,
    -soit le dico est vide vide."""
    
    if os.path.exists('feuille_scores'):
        with open('feuille_scores', 'rb') as fichier_scores:
            depickle = pkl.Unpickler(fichier_scores)
            try:
                scores = depickle.load()
            except EOFError:
                scores = {}
    else:
        with open('feuille_scores', 'wb+') as fichier_scores:
            depickle = pkl.Unpickler(fichier_scores)
            try:
                scores = depickle.load()
            except EOFError:
                scores = {}
    return scores


def sauvez_le_score (scores): #Willy #orque
    """Cette fonction se charge d'enregistrer les scores dans le fichier
    feuille_scores.
    Elle reçoit en paramètre le dictionnaire des scores
    à enregistrer.
    
    ne retourne rien"""

    with open('feuille_scores', 'r+b') as fichier_scores:
        jetepickle = pkl.Pickler(fichier_scores)
        jetepickle.dump(scores)


#--------------------------------UTILISATEUR------------------------------#

def user_existes_tu (scores): #comique de repetition
    """Cette fonction invite l'utilisateur a saisir son nom.
    - vérifie que le nom saisie fais au moins 3 caractères alphanumériques
    - si le nom est déja présent dans le fichier binaire, affiche le nom et le score
    
    retourne le nom d'utilisateur"""
    
    user = input("Veuillez saisir votre nom (alphanumérique uniquement !): ").capitalize()
    if user in scores.keys():
        print("Ravi de vous revoir {0}. A ce jour, votre score est de {1}".format(user, scores[user]))
        return user
    elif user.isalnum() and len(user)>2:
        scores[user] = 0
        return user
    else:
        print("Veuillez saisir un identifiant correct.")
        return user_existes_tu()

def relance (continuer):
    quitter = input("Souhaitez-vous délaisser le pendu à son triste sort (o/n) ? ")
    if quitter == "o" or quitter == "O" or quitter == "0":
        continuer = False
        return continuer
    elif quitter == "credit":
        print (credit)
        return relance (continuer)


#--------------------------------LETTRES ET MOTS------------------------------#

def choix_du_mot(les_mots_bleus):
    """Cette fonction choisit un mot au hasard, dans la liste contenu dans donnees.py.
    
    retourne un mot"""
    return rand.choice(les_mots_bleus)


def recup_lettre(mot_trouve, dechets):
    """recup_lettre demande à l'utilisateur une lettre, puis verifie /
    que l'input est bien une lettre MINUSCULE,
    qu'elle n'a pas déjà été trouvée ou saisie.
    
    retourne la lettre"""

    lettre = input("\nEntrez une lettre:")
    if lettre in string.ascii_lowercase and len(lettre)==1 and lettre not in mot_trouve:
        if lettre in dechets:
            print("Vous avez déjà entrée cette lettre non-valide, veuillez en essayer une autre !")
            return recup_lettre(mot_trouve, dechets)
        else:
            return lettre
    elif lettre in mot_trouve:
        print("Vous avez déjà trouvé cette lettre, veuillez en essayer une autre !")
        return recup_lettre(mot_trouve, dechets)
    else:
        print("On a dit une lettre ...")
        return recup_lettre(mot_trouve, dechets)


def is_lettre_dans_mot_choisit(lettre, mot_choisit, dechets):
    """Verifie que la lettre entrée correspond à une lettre du mot choisit.
    
    retourne un booléen"""
    
    if lettre in mot_choisit:
        return True
    else:
        dechets.append(lettre)
        return False


def mot_trouve(mot_choisit, mot_trouve, lettre):
    """Cette fonction remplace les "étoiles" 
    (les lettres manquantes du mot à trouver),
    par la lettre saisie, autant de fois que nécessaire.
    
    retourne le mot complété
    """
    i=0
    while i < len(mot_choisit):
        if mot_choisit[i]==lettre:
            mot_trouve[i]=lettre
        i+=1
    print("Bravo, vous avez trouvé la lettre:", lettre )
    return mot_trouve


#--------------------------------MAIN------------------------------#

def main():

    poubelle = []                           #liste de lettre non compatible avec le mot à trouver

    scores=scores_existes_tu()
    print (separateur)
    utilisateur = user_existes_tu (scores)
    
    mot = choix_du_mot(les_mots)
    resultat = list( "*" * len(mot) )
    
    n=nbr_chances                           #incrementation nbr de chances
    p=0                                     #incrementation affichage
    j=1                                     #incrementation numéro du tour
    while n>0 and mot!=''.join(resultat):
        
        print ("##### Tour n°{0} #####".format(j))
        print (afficher_tours[p])
        print ("Mot à trouvé: ", ''.join(resultat))
        if poubelle:
            print("Lettres non-valide: ", *poubelle)
        y = recup_lettre(resultat, poubelle)
        
        if is_lettre_dans_mot_choisit (y , mot, poubelle) is True:
            mot_trouve(mot, resultat, y)
        else:
            p += 1
            n -= 1
        if n!= 0:
            print( "\n----------------------\n(il vous reste {0} chances)" .format(n) )
        j+=1
        
    print (separateur)
    if mot==''.join(resultat):
        print("Félicitations ! Vous avez trouvé le mot {0}.".format(mot))
    else:
        print(x8, "\n\"On le pendit un matin, à la foire de la mort\", Adamo") #Salvatore Adamo
    print (separateur)
    
    print("Votre score total dans cette partie: ",n)
    scores[utilisateur] += n
    sauvez_le_score (scores)
    print("Votre score total à ce jour: ",scores[utilisateur])