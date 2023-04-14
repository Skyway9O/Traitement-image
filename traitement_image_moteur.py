"""Léo Gaspari, 12/02/2022
Programme moteur de traitement d'image.
"""

"""Les fonctions clean(), Recup_infos_image(), Recup_px() sont lancées automatiquement. Pas la peine de les appeler en mode console. Appeler la fonction d'enregistrement une fois avoir fait toues les modifications voulu."""


import explorateurFichiers as ex


contenu_image = None
pixels_image = None
info_image = None


def open_file():
    global contenu_image
    """Cette fonction permet d'ouvrir un fichier grâce à l'explorateur de fichier."""
    f = open(ex.choixFichier(), "r", encoding="utf_8") #ouvre un fichier choisi
    try:
        contenu_image = f.readlines() #récupère toutes les informations de l'image
        f.close()
        clean() #lance la fonction qui permet de "nétoyer" la liste contenu_image

    except:
        return "Image incorrecte."
    



def Recup_px():
    """Cette fonction permet de récupérer tous les pixels de l'image et de les isoler les un des autres. Ne pas exécuter cette fonction à la main : activation automatique."""
    global contenu_image, pixels_image
    
    format = info_image[2].split(" ") #récupère les dimensions de l'image
    if info_image[0] == "P2":
        pixels_image = [None for x in range(int(format[0])*int(format[1]))] #crée un tableau pouvant contenir tous les pixels à partir des dimension de l'image
    else: pixels_image_bis = []
    nb = 0
    for i in range(len(contenu_image[4:])):
        a = contenu_image[i+4][0].split(" ")
        while "" in a: #tant qu'il reste un espace dans la liste a 
            longueur = len(a)
            for k in range(longueur-1, -1, -1): #permet d'éviter de sortir du tableau car quand on supprime un élément, la taille de la liste diminue
                if a[k] == "": #si il y a une chaine de charactère vide ou un retour à la ligne à l'index k dans la liste a
                    del a[k]
        #permet de placer les pixels dans l'ordre dans la liste des pixels
        for x in range(len(a)):
            if info_image[0] == "P2":
                pixels_image[nb] = a[x]
            elif info_image[0] == "P3":
                pixels_image_bis.append(a[x])
            nb += 1

    if info_image[0] == "P3":
        pixels_image = []
        for k in range(0, len(pixels_image_bis), 3):
            pixels_image.append([pixels_image_bis[k],pixels_image_bis[k+1],pixels_image_bis[k+2]])
                


def Recup_infos_image():
    """Cette fonction permet de récupérer les information d'entête du fichier image. Ne pas exécuter cette fonction à la main : activation automatique."""
    global info_image

    info_image = contenu_image[:4]
    for k in range(len(info_image)):
        for i in range(len(info_image[k])):
            info_image[k] = info_image[k][i]
    info_image[1] = "#Created by Léo Gapsari with python"



def clean():
    """Cette fonction permet de supprimer tous les retours à la ligne du fichier ou les lignes vides afin de mieux traiter l'image par la suite. Ne pas exécuter cette fonction à la main : activation automatique."""
    
    global contenu_image

    longueur_contenu_image = len(contenu_image)
    for i in range(longueur_contenu_image):
        a = contenu_image[i].split("\n") #on sépare la chaîne de charactère à tous les retours à la ligne
        while "" in a or "\n" in a: #tant qu'il reste un espace ou un retour à la ligne dans la liste a 
            longueur = len(a)
            for k in range(longueur-1, -1, -1): #permet d'éviter de sortir du tableau car quand on supprime un élément, la taille de la liste diminue
                if a[k] == "" or a[k] == "\n": #si il y a une chaine de charactère vide ou un retour à la ligne à l'index k dans la liste a
                    del a[k] # on supprime cet élément
        contenu_image[i] = a #la liste a peu donc être replacé dans le contenu global de l'image

    #permet de supprimer toutes les listes vides afin de mieux traiter l'image pas la suite.
    for j in range(longueur_contenu_image-1, -1, -1): 
        if contenu_image[j] == [] :
            del contenu_image[j]
    
    Recup_infos_image()
    Recup_px()



def enregistrer():
    """Cette fonction permet d'enregistrer l'image sous un autre nom afin de pouvoir modifier l'image sans que cela soit la principale."""
    global new
    new = ex.sauveSous()
    ecrire()



def ecrire():
    """Cette fonction permet d'écrire dans le ficier enregistré auparavant. Conseil: Ne pas exécuter cette fonction à la main : activation automatique (possibilité tout de même d'exécuter cette fonction à la main mais seulement si la fonction enregister() a déjà été exécuté."""
    try:
        f = open(new, 'w', encoding="utf_8")
        for k in info_image:
            f.write(k + "\n")

        for k in range(len(pixels_image)):
            for i in range(len(pixels_image[k])):
                f.write(pixels_image[k][i] + "\n")
        f.close()

    except:
        return "Format d'image incorrect."



def inverse():
    """Cette fonction permet d'inverser les couleur de l'image."""
    global pixels_image
    if info_image[0] == "P3":
        for k in range(len(pixels_image)):
            for i in range(len(pixels_image[k])):
                pixels_image[k][i] = str(int(info_image[3]) - int(pixels_image[k][i])) #retire à info_image[3](la valeur maximale) la valeur du pixels afin de l'inverser
    elif info_image[0] == "P2":
        for k in range(len(pixels_image)):
                pixels_image[k] = str(int(info_image[3]) - int(pixels_image[k])) #retire à info_image[3](la valeur maximale) la valeur du pixels afin de l'inverser



def lumiere(valeur : int):
    """Cette fonction permet d'assombrir ou d'éclaircir l'image à partir d'une valeur"""
    global pixels_image
    if info_image[0] == "P3":
        for k in range(len(pixels_image)):
            for i in range(len(pixels_image[k])):
                if int(pixels_image[k][i]) + valeur > int(info_image[3]):  #pour ne pas dépasser les 255
                    pixels_image[k][i] = "255"
                elif int(pixels_image[k][i]) + valeur < 0: #pour ne pas être en dessous de 0
                    pixels_image[k][i] = "0"
                else:
                    pixels_image[k][i] = str(int(pixels_image[k][i]) + valeur)
    elif info_image[0] == "P2":
        for k in range(len(pixels_image)):
            if int(pixels_image[k]) + valeur > int(info_image[3]):  #pour ne pas dépasser les 255
                pixels_image[k] = "255"
            elif int(pixels_image[k]) + valeur < 0: #pour ne pas être en dessous de 0
                pixels_image[k] = "0"
            else:
                pixels_image[k] = str(int(pixels_image[k]) + valeur)



def reverse():
    """Cette fonction permet de retourner l'image."""
    global pixels_image

    format = info_image[2].split(" ") #récupère les dimensions de l'image
    liste_ligne = [[None for i in range(int(format[0]))] for k in range(int(format[1]))] #on crée un tableau vide avec les dimensions inverses à celles de l'image (car on tourne l'image : ex: 10 par 20 devient 20 par 10)

    for k in range(int(format[1])): 
        ligne = [x for x in pixels_image[k*int(format[0]): k*int(format[0]) + int(format[0])]] #on prend les pixels correspondant à la ligne k
        for i in range(int(format[0])):
            liste_ligne[k][int(format[0])-i-1] = ligne[i] #place le pixels à sa nouvelle position en fonction du sens dans liste_ligne

    #permet de remettre tous les pixels dans l'ordre dans la liste de pixel
    nb = 0
    for k in range(len(liste_ligne)):
        for i in range(len(liste_ligne[k])):
            pixels_image[nb] = liste_ligne[k][i]
            nb += 1



def tourne(cote : str):
    """Cette fonction permet de tourner l'image dans le sens voulu (D pour droite ou G pour gauche"""
    global pixels_image
    sens = cote.upper() #en prévision d'une erreur
    if sens == "G" or sens == "D": #vérifier que le sens existe
        format = info_image[2].split(" ") #récupère les dimensions de l'image
        liste_ligne = [[None for i in range(int(format[1]))] for k in range(int(format[0]))] #on crée un tableau vide avec les dimensions inverses à celles de l'image (car on tourne l'image : ex: 10 par 20 devient 20 par 10)

        for k in range(int(format[1])): 
            ligne = [x for x in pixels_image[k*int(format[0]): k*int(format[0]) + int(format[0])]] #on prend les pixels correspondant à la ligne k
            for i in range(int(format[0])):
                liste_ligne[i][k if sens == "G" else int(format[1])-k-1] = ligne[((int(format[0])-i-1 ) if sens == "G" else i)] #place le pixels à sa nouvelle position en fonction du sens dans liste_ligne

        #permet de remettre tous les pixels dans le nouvel ordre dans la liste de pixel
        nb = 0
        for k in range(len(liste_ligne)):
            for i in range(len(liste_ligne[k])):
                pixels_image[nb] = liste_ligne[k][i]
                nb += 1
        info_image[2] = format[1] + " " + format[0] #change les dimensions de l'image par les nouvelles

    else:
        return "Ce sens n'existe pas."


def modifie_couleur(couleur, valeur):
    """Cette fonction permet de modifier une couleur ( donc la valeur du pixels rouge vert ou bleu ) avec une valeur."""
    if info_image[0] == "P3":
        if couleur == "R":
            pixel_couleur = 0
        elif couleur == "V":
            pixel_couleur = 1
        elif couleur == "B":
            pixel_couleur = 2
        for k in range(len(pixels_image)):
            if int(pixels_image[k][pixel_couleur]) + valeur > int(info_image[3]):  #pour ne pas dépasser les 255
                pixels_image[k][pixel_couleur] = "255"
            elif int(pixels_image[k][pixel_couleur]) + valeur < 0: #pour ne pas être en dessous de 0
                pixels_image[k][pixel_couleur] = "0"
            else:
                pixels_image[k][pixel_couleur] = str(int(pixels_image[k][pixel_couleur]) + valeur)