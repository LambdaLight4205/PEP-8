def verifier_longueur(texte):
    if len(texte) > 78:
        return False
    
    return True

def verifier_virgules(texte):
    for i, char in enumerate(texte):
        if char == "," and texte[i + 1] != " ":
            return False
        
    return True

def verifier_parentheses(texte):
    for i, char in enumerate(texte):
        if char == "(" and texte[i - 1] == " ":
            return False
        
    return True

def verifier_deux_points(texte):
    for i, char in enumerate(texte):
        if char == ":" and texte[i - 1] == " ":
            return False
        
    return True

def verifier_pep8(nom_fichier):
    with open (nom_fichier, "r") as fichier:
        texte = fichier.read()

    liste_lignes = texte.splitlines()
    print(liste_lignes)

    for i in range(len(liste_lignes)):
        ligne = liste_lignes[i]

        if not verifier_longueur(ligne):
            return i + 1
        
        if not verifier_virgules(ligne):
            return i + 1
        
print(verifier_pep8("test.py"))