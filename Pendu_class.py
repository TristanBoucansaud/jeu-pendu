from tkinter import *
from math import *
import random as rd
from tkinter.messagebox import *

#On crée des phrases types de victoire/défaite (c'est plus sympa)
phrases_victoires=['Bravo, c\'est gagné !! Est-ce un coup de chance ?','Mes félicitations ! Encore une fois !','Haha bien joué ! Rééssayons','MAIS QUEL CHAMPION !! Remettons ton titre en jeu ;)']
phrases_defaites=['Mince, raté... On rééssaye ?','Ahhh, pas loin !! Il faut retenter ta chance !','C\'est perdu, mais ne te laisse pas abattre !','Dommage... La prochaine fois sera la bonne !']
liste_boutons=[]    #On crée une liste qui recensera les boutons des lettres dans ce programme


def lettre_into_mot(l,mot): #Ce programme cherche les positions d'une lettre dans un mot. Retourne une liste de positions, vide si la lettre n'apparaît pas
    L=[]
    for k in range(len(mot)):   #On parcourt les lettres du mot et on les compare à notre lettre initiale
        if l==mot[k]:
            L.append(k)
    return(L)

def griser_all(liste_boutons):  #Programme permettant de griser TOUS les boutons, en s'appuyant sur la liste des boutons compris dans CE programme
    for elt in liste_boutons:
        elt.griser_bouton()

def activer_all(liste_boutons): #Programme permettant d'activer TOUS les boutons, en s'appuyant sur la liste des boutons compris dans CE programme
    for elt in liste_boutons:
        elt.activer_bouton()
        

class MonBouton(Button):    #Création de la classe MonBouton, sous classe de Button

    def __init__(self,frame,lettre,image,mot,fen):  #Initialisation
        self.__fen=fen
        self.__image=image
        self.__mot=mot
        self.__lettre=lettre
        self.__frame=frame
        Button.__init__(self,frame,text=lettre,command=self.push)   #On crée le programme après avoir stocké les autres composantes du bouton

    def push(self): #Commande associée aux boutons des lettres. Il va modifier l'affichage du mot si la lettre y est dedans, et vérifier les conditions de victoire/défaite
        positions=lettre_into_mot(self.__lettre,self.__mot.get_mot())   #On cherche si la lettre est dans le mot
        self.griser_bouton()    #On grise le bouton dans tous les cas
        if len(positions) >0:   #Si la lettre apparaît, on met à jour l'affichage, grâce à la liste de positions
            self.__mot.nouvel_affichage(positions)
        else:   #Sinon, on met l'image suivante du pendu
            self.__image.image_suivante()
        if self.__mot.victoire():   #S'il y a victoire :
            vic = Toplevel(self.__fen)  #On ouvre la fenêtre annonçant la victoire
            vic.title('Victoire !!')
            aff=Label(vic,text=phrases_victoires[rd.randint(0,3)],justify='left',anchor='nw')   #On affiche une phrase aléatoire parmi le panel de phrases
            aff.pack(side=TOP)
            aff=Label(vic,text='\nEntrez votre nom :',justify='left',anchor='nw')   #On demande d'entrer le nom du joueur
            aff.pack(side=LEFT)
            nom=StringVar() #Variable qui va stocker le nom du joueur
            score=Score(nom,self.__image.get_erreur(),self.__mot.get_mot(),vic) #On crée l'objet de type Score qui sera rentré dans le .txt par la suite
            zone_nom=Entry(vic,textvariable=nom)    #On crée la zone d'entrée
            zone_nom.focus_set()
            zone_nom.pack(side=LEFT,padx=5,pady=5)
            Button(vic, text='Valider',command=score.ecrire).pack(side=LEFT,padx=5,pady=5)  #Puis on met un bouton pour valider
            griser_all(liste_boutons)   #Et on grise enfin toutes les lettres
        if self.__image.get_erreur() == 7:  #Si défaite (il y a 8 images, si on est à la 8eme, le joueur a perdu), tout pareil
            defe = Toplevel(self.__fen)
            defe.title('Défaite...')
            aff=Label(defe,text=phrases_defaites[rd.randint(0,3)],justify='left',anchor='nw')
            aff.pack(side=TOP)
            aff=Label(defe,text='Le mot était : '+self.__mot.get_mot(),justify='left',anchor='nw')  #Avec en plus l'affichage du mot à deviner
            aff.pack(side=TOP)
            aff=Label(defe,text='\nEntrez votre nom :',justify='left',anchor='nw')
            aff.pack(side=LEFT)
            nom=StringVar()
            score=Score(nom,self.__image.get_erreur(),self.__mot.get_mot(),defe)
            zone_nom=Entry(defe,textvariable=nom)
            zone_nom.focus_set()
            zone_nom.pack(side=LEFT,padx=5,pady=5)
            Button(defe, text='Valider',command=score.ecrire).pack(side=LEFT,padx=5,pady=5)
            griser_all(liste_boutons)

    def griser_bouton(self):    #Grise le bouton demandé
        self.config(state=DISABLED)

    def activer_bouton(self):   #Active le bouton demandé
        self.config(state='normal')


            

class ImagePendu:   #Classe de l'image du pendu. L'objet ne sera pas une image, mais plutôt une séquence d'images.

    def __init__(self,c):   #Initialisation
        self.__canevas=c
        pendu1 = PhotoImage(file='pendu1.gif')
        pendu2 = PhotoImage(file='pendu2.gif')
        pendu3 = PhotoImage(file='pendu3.gif')
        pendu4 = PhotoImage(file='pendu4.gif')
        pendu5 = PhotoImage(file='pendu5.gif')
        pendu6 = PhotoImage(file='pendu6.gif')
        pendu7 = PhotoImage(file='pendu7.gif')
        pendu8 = PhotoImage(file='pendu8.gif')
        self.__pendus=[pendu1,pendu2,pendu3,pendu4,pendu5,pendu6,pendu7,pendu8] #On crée la séquence d'images
        self.__etape=0  #On initialise le compteur d'étape à 0 (image du pendu de début de partie)
        self.__canevas.create_image(0,0, anchor=NW, image=self.__pendus[self.__etape])  #Puis on affiche l'image concernée (donc l'étape 0 ici)
        self.__canevas.config(height=self.__pendus[self.__etape].height(),width=self.__pendus[self.__etape].width())

    def image_suivante(self):   #Passe à l'image suivante du pendu
        if self.__etape+1<8:    #On vérifie quand même qu'on ne soit pas déjà à la dernière image, même si en réalité, cela n'arrive jamais
            self.__etape+=1
        self.__canevas.delete(ALL)  #On supprime l'ancienne image
        self.__canevas.create_image(0,0, anchor=NW, image=self.__pendus[self.__etape])  #Et on met la nouvelle image, correspondant à l'étape suivante
        self.__canevas.config(height=self.__pendus[self.__etape].height(),width=self.__pendus[self.__etape].width()) 

    def reset(self):    #Remet la première image du pendu (fonctionne comme image_suivante())
        self.__etape=0
        self.__canevas.delete(ALL)
        self.__canevas.create_image(0,0, anchor=NW, image=self.__pendus[self.__etape])
        self.__canevas.config(height=self.__pendus[self.__etape].height(),width=self.__pendus[self.__etape].width())

    def get_erreur(self):   #Renvoie la propriété correspondant à l'étape dans l'avancement du pendu
        return(self.__etape)

class Mot(Label):   #Classe du mot. Il s'agit d'une sous classe de la classe Label.

    def __init__(self,mot): #Initialisation
        Label.__init__(self)
        self.__mot=mot  #On stocke le mot à part dans une propriété de la classe
        self.__affichage='*'*len(mot)   #L'affichage correspond le même nombre de lettres que le mot, mais est pour l'instant entièrement constitué d'astérisques
        self.pack(side=TOP)
        self.config(text=self.__affichage)

    def get_mot(self):  #Retourne le mot stocké (et pas le mot affiché)
        return(self.__mot)

    def maj_mot(self):  #Met à jour l'affichage
        self.config(text=self.__affichage)

    def nouvel_affichage(self,positions):   #Lorsqu'une lettre du mot est trouvée, remplace les astérisques correspondantes par la vraie lettre
        for elt in positions:
            self.__affichage=self.__affichage[:elt]+self.__mot[elt]+self.__affichage[elt+1:]    #Slicing car on ne peut pas remplacer directement un caractère d'un str
        self.maj_mot()

    def reset(self,newmot): #Commande associée au bouton de Nouvelle partie. Enregistre le nouveau mot et met à jour l'affichage
        self.__mot=newmot
        self.__affichage='*'*len(self.__mot)
        self.maj_mot()

    def victoire(self): #Vérifie une victoire en regardant s'il reste des astérisques dans l'affichage.
        return('*' not in self.__affichage)

class Score:    #Classe du score d'un joueur.

    def __init__(self,joueur,erreurs,mot,fen):  #Initialisation
        self.__joueur=joueur
        self.__erreurs=erreurs
        self.__mot=mot
        self.__fen=fen
        
    def ecrire(self):   #Ecrit le score dans le fichier .txt
        with open('scores.txt','r') as f:   #On lit ce qu'il y a dans le fichier
            scores = f.read()
        i=0
        while scores[i]!='\n':  #On se positionne juste après le premier retour à la ligne (donc techniquement juste après 'Scores :\n')
            i+=1
        if self.__erreurs==7:   #Dans le cas d'une défaite
            scores=scores[:i+1]+self.__joueur.get()+' : '+'Défaite, mot : '+self.__mot+'\n'+scores[i+1:]    #Slicing
        else:   #Dans le cas d'une victoire
            scores=scores[:i+1]+self.__joueur.get()+' : '+str(self.__erreurs)+', mot : '+self.__mot+'\n'+scores[i+1:]   #Slicing
        with open('scores.txt','w') as f:   #Puis on réécrit le fichier entièrement, avec le nouveau texte écrit plus haut
            for i in scores:
                f.write(str(i))
        self.__fen.destroy()    #Et on ferme finalement la fenêtre de victoire/défaite
        








        
