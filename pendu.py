from tkinter import *
import random as rd
from Pendu_class import liste_boutons
from Pendu_class import *

with open('mots.txt','r') as f: #On récupère ici les mots du fichier .txt
    liste_mots = f.read().splitlines()

def resetscore():   #Commande associée au bouton Réinitialiser, dans la fenêtre des scores. Elle reset le tableau des scores
    with open('scores.txt','w') as f:
        for i in 'Scores :\n':  #On souhaite qu'il reste dans le fichier scores.txt uniquement 'Scores :\n'
            f.write(str(i))
        
def newgame():  #Commande associée au bouton de Nouvelle partie.
    global image_pendu,mot,boutons_lettres
    image_pendu.reset() #On remet l'image du pendu au début
    newmot=liste_mots[rd.randint(0,len(liste_mots)-1)]  #On choisit un nouveau mot
    mot.reset(newmot)   #Et on met à jour notre variable de type Mot
    activer_all(boutons_lettres)    #Puis on réactive toutes les touches du clavier

def scores():   #Commande associée au bouton Scores
    with open('scores.txt','r') as f:   #On récupère les scores dans le fichier .txt
        scores = f.read()
    fenscore = Toplevel(fen)    #On ouvre une nouvelle fenêtre
    fenscore.title=('Scores')
    affscores=Label(fenscore,text=scores,justify='left',width=25,height=30,anchor='nw') #On ajoute un Label avec les scores
    affscores.pack(side=LEFT)
    Button(fenscore, text='Quitter',command=fenscore.destroy).pack(side=BOTTOM,padx=5,pady=5)   #On met un bouton pour quitter cette fenêtre
    Button(fenscore, text='Réinitialiser',command=resetscore,).pack(side=BOTTOM,padx=5,pady=5)  #Et un bouton pour réinitialiser les scores (fonctionnel après la réouverture de la fenêtre)
    
    

fen=Tk()    #Création de la fenêtre
fen.title('Jeu du Pendu')

mot=Mot(liste_mots[rd.randint(0,len(liste_mots)-1)])    #On choisit un mot pour la première partie

canevas = Canvas(fen)   #Création du canevas

image_pendu=ImagePendu(canevas) #Création de l'objet qui servira d'image

frame = Frame(fen)  #Création de la frame qui accueillera les lettres
lettres = ['A','Z','E','R','T','Y','U','I','O','P','Q','S','D','F','G','H','J','K','L','M','W','X','C','V','B','N'] #Liste des lettres en AZERTY
boutons_lettres = []    #Lettre recensant tous les boutons (dans ce programme)
for i in range(26): #On parcourt les lettres pour créer les boutons
    l=lettres[i]
    bouton=MonBouton(frame,l,image_pendu,mot,fen)   #On crée chaque bouton en utilisant la classe MonBouton
    boutons_lettres.append(bouton)  #On remplit la liste de boutons
    liste_boutons.append(bouton)    #Pareil ici, mais pour le programme des classes
    bouton.grid(row=i//10,column=i%10)  #On place chaque bouton

frame.pack(side=BOTTOM) #Et on place la frame


canevas.pack(side=BOTTOM)   #Puis le canevas, dans un souci de meilleur placement dans l'interface (on veut le clavier en dessous du canevas)

Button(fen, text='Quitter',command=fen.destroy).pack(side=LEFT,padx=5,pady=5)   #Enfin, on place les 3 boutons de jeu
Button(fen, text='Nouvelle partie', command=newgame).pack(side=RIGHT,padx=5,pady=5)
Button(fen, text='Scores', command=scores).pack(side=TOP,padx=5,pady=5)
fen.mainloop()  #Et on lance la mainloop
