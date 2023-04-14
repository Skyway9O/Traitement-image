"""Léo Gaspari, 12/02/2022
Programme garphique de traitement d'image.
"""

"""Si les image ne s'affichent pas, il faut changer les chemin d'accès des images ou modifier l'emplacement d'où on exécute le scripte."""


from tkinter import *
import traitement_image_moteur as moteur
import os
path = os.path.dirname(__file__)


def reset():
    """Cette fonction permet de rénitialiser l'image"""
    moteur.Recup_px()
    afficher_image()


def recup_couleur():
    """Cette fonction permet récupérer les valeur des barres permettant de changer les composants des pixels."""
    luminosite = int(barre_valeur.get())
    valeur_rouge = int(barre_rouge.get())
    valeur_vert = int(barre_vert.get())
    valeur_bleu = int(barre_bleu.get())
    if valeur_rouge != 0:
        moteur.modifie_couleur("R", valeur_rouge)
    if valeur_vert != 0:
        moteur.modifie_couleur("V", valeur_vert)
    if valeur_bleu != 0:
        moteur.modifie_couleur("B", valeur_bleu)
    if luminosite !=0:
        moteur.lumiere(luminosite)

    barre_rouge.set(0)
    barre_vert.set(0)
    barre_bleu.set(0)
    barre_valeur.set(0)
    afficher_image()


def charger_image():
    """Cette fonction permet de sélectionner l'image et d'activer tous les boutons quand une image valable a été choisi."""
    resultat = moteur.open_file()
    
    if resultat != None:
        label_info.configure(text=resultat+" Choisissez une autre image.")

    else:
        afficher_image()
        bouton_selection.configure(bg="#e6e6e6", text="Changer d'image")
        bouton_inverse.configure(state=NORMAL)
        bouton_tourne_droite.configure(state=NORMAL)
        bouton_tourne_gauche.configure(state=NORMAL)
        bouton_retourner.configure(state=NORMAL)
        bouton_enregistre.configure(state=NORMAL)
        barre_valeur.configure(state=NORMAL)
        bouton_valide_couleur.configure(state=NORMAL)
        bouton_reset.configure(state=NORMAL)
        barre_rouge.configure(state=DISABLED)
        barre_vert.configure(state=DISABLED)
        barre_bleu.configure(state=DISABLED)
        label_info.configure(text="Choisissez un ou plusieurs traitements d'image.")

        if moteur.info_image[0] == "P3":
            
            barre_rouge.configure(state=NORMAL)
            barre_vert.configure(state=NORMAL)
            barre_bleu.configure(state=NORMAL)
        


def enregistre():
    """Cette fonction permet d'appeler la fonction permettant d'enregistrer les modifications."""
    moteur.enregistrer()


def inverse_couleur():
    moteur.inverse()
    afficher_image()


def tourne_droite():
    moteur.tourne("D")
    afficher_image()


def tourne_gauche():
    moteur.tourne("G")
    afficher_image()


def reverse_image():
    moteur.reverse()
    afficher_image()


def ecrire():
    """Cette fonction permet d'écrire l'image modifiée dans un fichier au format P5 car le format P2 n'est pas prit en compte dans tkinter. Tout cela à pour but de l'afficher dans l'interface graphique."""

    format = moteur.info_image[2].split(" ")
    color = "P5" if moteur.info_image[0] == "P2" else "P6"
    entete = bytes(("{} {} {} 255 ".format(color, int(format[0]), int(format[1]))).encode("utf-8"))

    liste_bytes = []
    for k in range(len(moteur.pixels_image)):
        if moteur.info_image[0] == "P3":
            for i in range(len(moteur.pixels_image[k])):
                liste_bytes += [int(moteur.pixels_image[k][i])]
        elif moteur.info_image[0] == "P2":
            liste_bytes += [int(moteur.pixels_image[k])]

    fichier = entete + bytes(liste_bytes)

    f = open((path + "/image/image_apercu.pgm" if moteur.info_image == "P2" else path + "/image/image_apercu.ppm"), 'wb')
    f.write(fichier)
    f.close()
    


def afficher_image():
    """Permet d'afficher l'image d'aperçu dans le canvas"""
    global image_apercu
    ecrire()
    image_apercu = PhotoImage(file=(path + "/image/image_apercu.pgm" if moteur.info_image == "P2" else path + "/image/image_apercu.ppm"))
    canvas_image.delete("all")
    canvas_image.create_image(0,0, anchor=NW, image=image_apercu)



#création de la fenêtre
fenetre = Tk()
fenetre.title("traitement image")
fenetre.geometry("1200x1000")
fenetre.minsize(1200, 1000)

#charge les images
image_vide = PhotoImage(file= path + "/image/visuel_non_disponible.gif")
image_tourne_droite = PhotoImage(file= path + "/image/droite_tourne.gif")
image_tourne_gauche = PhotoImage(file= path + "/image/gauche_tourne.gif")


#cree une frame
frame = Frame(fenetre)

#pack la fenêtre
frame.pack(expand=YES)

#création d'un canvas 
canvas_image = Canvas(frame, width=700, height=700)
canvas_image.grid(row=2, column=0, rowspan=10, sticky=NW)

canvas_image.create_image(250, 250, image=image_vide)

#ajoute l'emplacement de l'aperçu d'image
label_info = Label(frame, text="Appuyez sur : 'Sélectionner une image' et sélectionnez une image en .pgm ou .ppm.", font=("Helvetica, 20"), borderwidth=3, relief="solid", justify= "center")
label_info.grid(row=0, column=0, columnspan=4, pady=10)

label_apercu = Label(frame, text="Aperçu de l'image :", font=("Helvetica, 15"))
label_apercu.grid(row=1, column=0, pady=10, sticky=W)

label_tourne = Label(frame, text="Tourner : ", font=("Helvetica, 18"))
label_tourne.grid(row=3, column=1, pady=10, sticky=E)

label_lumière = Label(frame, text="Vous pouvez modifier la\nluminosité (.pgm et.ppm)\net la couleur (.ppm) :", font=("Helvetica, 18"))
label_lumière.grid(row=5, column=1, columnspan=3, pady=10, padx=30)


#ajoute les boutons
bouton_selection = Button(frame, text="Sélectionner une image", command=charger_image, font=("Helvetica, 18"), bg="#ffddad")
bouton_selection.grid(row=1, column=1, columnspan=3, pady=10, padx=30)

bouton_inverse = Button(frame, text="Inverser les couleurs", command=inverse_couleur, font=("Helvetica, 18"), state=DISABLED, bg="#e6e6e6")
bouton_inverse.grid(row=2, column=1, columnspan=3, pady=10, padx=30)

bouton_tourne_droite = Button(frame, image=image_tourne_droite, command=tourne_droite, state=DISABLED, bg="#e6e6e6")
bouton_tourne_droite.grid(row=3, column=3, pady=10, padx= 10)

bouton_tourne_gauche = Button(frame, image=image_tourne_gauche, command=tourne_gauche, state=DISABLED, bg="#e6e6e6")
bouton_tourne_gauche.grid(row=3, column=2, pady=10, padx= 10, sticky=E)

bouton_retourner = Button(frame, text="Retourner l'image", font=("Helvetica, 18"), command=reverse_image, state=DISABLED, bg="#e6e6e6")
bouton_retourner.grid(row=4, column=1, columnspan=3, pady=20, padx=30)

barre_valeur = Scale(frame, from_=-255, to=255, orient=HORIZONTAL, width=26, length=300, sliderlength=10, state=DISABLED, label="Luminosité")
barre_valeur.grid(row=6, column=1, columnspan=3, pady=10)

bouton_quitter = Button(frame, text="Quitter", font=("Helvetica, 17"), bg= "#f78888", command=fenetre.destroy)
bouton_quitter.grid(row=12, column=0)

barre_rouge = Scale(frame, from_=-255, to=255, width=26, length=100, sliderlength=15, state=DISABLED, label="Rouge")
barre_rouge.grid(row=7, column=1)

barre_vert = Scale(frame, from_=-255, to=255, width=26, length=100, sliderlength=15, state=DISABLED, label="Vert")
barre_vert.grid(row=7, column=2)

barre_bleu = Scale(frame, from_=-255, to=255, width=26, length=100, sliderlength=15, state=DISABLED, label="Bleu")
barre_bleu.grid(row=7, column=3)

bouton_valide_couleur = Button(frame, text="Valider", font=("Helvetica, 13"), state=DISABLED, command=recup_couleur, bg="#e6e6e6")
bouton_valide_couleur.grid(row=8, column=1, columnspan=3, pady=10, padx=10)

bouton_enregistre = Button(frame, text="Enregistrer les\nmodifications", bg="#e4ffa5", font=("Helvetica, 18"), command=enregistre, state=DISABLED)
bouton_enregistre.grid(row=12, column=2, columnspan=2, pady=20)

bouton_reset = Button(frame, text="Rénitialiser l'image", font=("Helvetica, 17"), command=reset, bg="#ffc380", state=DISABLED)
bouton_reset.grid(row=9, column=1, pady=10, columnspan=3)


fenetre.mainloop()

