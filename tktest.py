import tkinter as tk
import random   

def generer_sequence():
    liste_mots = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    list_con = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
    list_voy = ["a", "e", "i", "o", "u"]

    nombre_con = int(nombre_consonnes.get())
    nombre_voy = int(nombre_voyelles.get())

    result = []

    for i in range(nombre_con):
        con = random.choice(list_con)
        result.append(con)

    for i in range(nombre_voy):
        voy = random.choice(list_voy)
        result.append(voy)

    random.shuffle(result)
    sequence = ''.join(result)

    resultat_label.configure(text=sequence)

fenetre = tk.Tk()
fenetre.title("Générateur de séquence de lettres")

nombre_consonnes_label = tk.Label(fenetre, text="Nombre de consonnes :")
nombre_consonnes_label.pack()

nombre_consonnes = tk.Entry(fenetre)
nombre_consonnes.pack()

nombre_voyelles_label = tk.Label(fenetre, text="Nombre de voyelles :")
nombre_voyelles_label.pack()

nombre_voyelles = tk.Entry(fenetre)
nombre_voyelles.pack()

generer_bouton = tk.Button(fenetre, text="Générer", command=generer_sequence)
generer_bouton.pack()

resultat_label = tk.Label(fenetre, text="")
resultat_label.pack()

fenetre.mainloop()
