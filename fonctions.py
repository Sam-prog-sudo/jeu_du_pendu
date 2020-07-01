import string
import random as rand

def quel_mot():
    """quel_mot permet de convertir toutes les lignes d'un fichier texte,/
    en une liste de mots, puis choisit un mot au hasard, dans cette liste."""
    
    with open("mots8.txt", "r") as f:
        x=f.readline()
    return rand.choice(x)   

    
        
def recup_lettre():
    """recup_lettre demande à l'utilisateur une lettre, puis verifie /
    que l'input est bien une lettre, et pas un cochon d'inde."""
    
    lettre = input("Entrez une lettre:")
    
    if lettre in string.ascii_letters and len(lettre)==1:
        return lettre
    
    else:
        print("Mets une lettre batard !")
        return recup_lettre()