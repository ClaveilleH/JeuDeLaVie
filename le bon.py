# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 16:43:56 2022

@author: claveille
"""

import pygame 		# import de la bibliothÃ¨que pygame
from random import randint, choice
from time import sleep


"""
--------------------------CONTROLS------------------------------------------------
maintenir espace pour mettre en pause
utiliser la souris lorsque le jeu est en pause afin de creer ou suprimer des cases
----------------------------------------------------------------------------------
"""
#fenetre = pygame.display.set_mode((500,500)) # instance fenÃªtre graphique

class Cellule:
    def __init__(self, idd = 0, couleur = (100,100,100), voisins = []):
        self.actuel = False
        self.futur = False
        self.couleur = couleur
        self.idd = idd
        self.voisins = voisins
                    
    def get_id(self):
        return self.idd
    
    def set_coul(self,coul):
        self.couleur = coul
        
    def get_coul(self):
        return self.couleur
    
    def est_vivant(self):
        return self.actuel
    
    def set_voisins(self, liste):
        self.voisins = liste.copy()
        #print(self.voisins)

    def get_voisins(self):
        return self.voisins
    
    def naitre(self):
        self.futur = True
        self.set_coul(self.calcul_coul( ))
    
    def mourir(self):
        self.futur = False
    
    def basculer(self):
        self.actuel = self.futur
    
    def calcul_coul(self):
        """Methode qui calcule la couleur en fonction des """
        couls = []
        for cell in self.get_voisins():
            if cell.est_vivant():
                couls.append(cell.get_coul())
        return moyenneCoul(couls)
    
    def afV(self):
        count = 0
        for cell in self.get_voisins():
            if cell.est_vivant():
                count += 1
        return str(count) if count != 0 else '_'  # and self.est_vivant()

    def calcule_etat_futur(self):
        """Methode qui calcule le prochain etat en fonction du nombre de voisins en vie"""
        count = 0
        couls = []
        for cell in self.get_voisins():
            if cell.est_vivant():
                count += 1
                couls.append(cell.get_coul())
        if count == 3 and not self.actuel:
            self.naitre()
            self.set_coul(moyenneCoul(couls))
            return count
        elif not count in [2,3]:
            self.mourir()
            return count
        
        return count
    
    def __str__(self):
        return 'X' if self.actuel else '_'
        return 'X' if self.voisins == None else '_'

def moyenneCoul(liste):
    """Fonction qui calcule la moyenne des couleurs donnes
    :liste: list - liste des couleurs"""
    dico = {(255,0,0):0,(0,255,0):0,(0,0,255):0}
    if len(liste)==1:
        return liste[0]
    for coul in liste:
        dico[coul] += 1
    dico2 = {elem:key for key,elem in dico.items()}
    return dico2[max(dico2.keys())]
    

class Grille():
    def __init__(self, largeur = 0, hauteur = 0):
        self.largeur = largeur
        self.hauteur = hauteur
        self.matrix = []#[[Cellule() for _ in range(hauteur)] for _ in range(largeur)]
        i = 0
        for x in range(largeur):
            liste = []
            for y in range(hauteur):
                liste.append(Cellule(idd = i))
                i += 1
            self.matrix.append(liste)
    
    
    def get_cellule(self, i, j):
        #print(self.matrix)
        return self.matrix[i][j]
    
    def get_largeur(self):
        return self.largeur
    
    def get_hauteur(self):
        return self.hauteur
    
    def get_voisins(self, i, j):
        cell = self.get_cellule(i, j)
        return cell.get_voisins()
    
    def affecte_voisins(self):
        casesBase = [[-1,1],[0,1],[1,1],
                [-1,0],       [1,0],
                [-1,-1],[0,-1],[1,-1]]
        coins = [[0,0], [0,self.largeur-1], [self.hauteur-1,0], [self.hauteur-1,self.largeur-1]]
        dico = {tuple(coins[0]):[[0,1],[1,1],[-1,0],[1,0],[-1,-1],[0,-1],[1,-1]],
                tuple(coins[1]):[[-1,1],[0,1],[1,1],[-1,0],[1,0],[-1,-1],[0,-1],[1,-1]],
                tuple(coins[2]):[[-1,1],[0,1],[1,1],[-1,0],[1,0],[0,-1],[1,-1]],
                tuple(coins[3]):[[-1,1],[0,1],[1,1],[-1,0],[-1,-1],[0,-1]]}
        for x in range(self.largeur):
            for y in range(self.hauteur):
                liste = []
                if [x,y] in coins and False:
                    cases = dico[(x,y)]
                else:
                    cases = casesBase
                for c in cases:
                    a, b = c
                    xa = x+a
                    yb = y+b
                        
                    if xa > self.largeur-1:
                        xa = 0
                    elif xa < 0:
                        xa = self.largeur-1
                    #------------------------------ pas forcement besoin
                    if yb > self.hauteur-1:
                        yb = 0
                    elif yb < 0:
                        yb = self.hauteur-1
                    #------------------------------
                    #print(xa,yb)
                    liste.append(self.matrix[xa][yb])
                self.matrix[x][y].set_voisins(liste)
        
    def jeux(self):
        """"""
        for x in range(self.largeur):#self.matrix:
            for y in range(self.hauteur):
                self.matrix[x][y].calcule_etat_futur()
    
    def actualise(self):
        """Fonction qui actualise toutes les cellules"""
        for ligne in self.matrix:
            for cell in ligne:
                cell.basculer()
    
    def remplir_alea(self,x):
        """Fonction qui remplis aléatoirement la grille a un certain pourcentage
        :x: int-qté de case en %"""
        couls = [(255,0,0),(0,255,0),(0,0,255)]
        print(self.hauteur*self.largeur)
        print(int(self.hauteur*self.largeur/100*x))
        for i in range(int(self.hauteur*self.largeur/100*x)):
            c = self.get_cellule(randint(0, self.largeur-1), randint(0, self.hauteur-1))
            c.naitre()
            c.set_coul(choice(couls))

    def afV(self):
        """Fonction de test qui renvoi le nombre de voisins en vie tel un demineur"""
        chaine = str()
        for ligne in self.matrix:
            for case in ligne:
                chaine += case.afV()
            chaine += '\n'
        return chaine

    def __str__(self):
        chaine = str()
        for ligne in self.matrix:
            for case in ligne:
                chaine += str(case)
            chaine += '\n'
        return chaine

def dessin_grille(g,cote,jeu):
    """ dessine les ligne de la grille """
    xfin = pygame.display.get_window_size()[0]
    #yfin = pygame.display.get_window_size()[1]
    for pos in range(len(g.matrix)):
        if jeu:
            pygame.draw.line(fenetre,(10,10,10),(pos*cote,0),(pos*cote,xfin),2) # dÃ©finition d'une ligne
            pygame.draw.line(fenetre,(10,10,10),(0,pos*cote),(xfin,pos*cote),2) # dÃ©finition d'une ligne
        else:
            pygame.draw.line(fenetre,(100,10,10),(pos*cote,0),(pos*cote,xfin),2) 
            pygame.draw.line(fenetre,(100,10,10),(0,pos*cote),(xfin,pos*cote),2) # dÃ©finition d'une ligne
        

def des_carre(x,y,coul,cote):
    """dessine la couleur du carrÃ© de coordonnÃ©e x,y"""
    pygame.draw.rect(fenetre, coul,(x*cote,y*cote,cote,cote))
    

def dessin_cellules(g,cote):
    """ dessine les carrÃ©s de la grille soit allumÃ© soit eteint"""
    for celX in range(len(g.matrix)):           # chaque verticale
        for celY in range(len(g.matrix[0])) :   # chaque cellule de la verticale
            if g.matrix[celX][celY].est_vivant():
                des_carre(celX,celY,g.matrix[celX][celY].get_coul(),cote)
            else :
                des_carre(celX,celY,(220,220,220),cote)
                
taille = 30
fenetre = pygame.display.set_mode((25*taille,25*taille)) # instance fenÃªtre graphique

def main1(taille = 20):     # fonction principale
    g = Grille(taille,taille)                           # largeur, hauteur
    g.affecte_voisins()
    fenetre.fill((250,250,150))                 # couleur
    run = True                                  # boucke du script pour l'arret
    jeu = True
    click = False
    precedentID = None
    cote = int(pygame.display.get_window_size()[0]/taille) # nbre de pixel d'un cotÃ©
    g.remplir_alea(30)
    g.actualise()
    mode = 0 #0,1 ou 2 0: pas innitialisÃ© 1:mode naissance 3:mode mort
    while run:                                  # boucle sans fin!!
        for event in pygame.event.get():        # parcours les Ã©vÃ©ments pygame
            if event.type == pygame.QUIT:       # croix en haut Ã  droite de la fenetre (True or False)
                run = False                             # ne fain rien 
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    jeu = False
                if event.key == pygame.K_ESCAPE :
                    run = False                    # fin du while
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_SPACE :
                    jeu = True
 
            if not jeu:
                if event.type == pygame.MOUSEBUTTONUP:  # evement lacher bouton
                    click = False  
                if event.type == pygame.MOUSEBUTTONDOWN:        # evenement appui

                    if pygame.mouse.get_pressed() == (1,0,0):   # dÃ©tection button gauche
                        click = True
                        
                        
        if click:
            i = pygame.mouse.get_pos()[0] // cote   # coordonnÃ©e x de la souris
            j = pygame.mouse.get_pos()[1] // cote   # sur y # 
            if not precedentID == g.matrix[i][j].get_id():
                if mode == 0:
                    if g.matrix[i][j].est_vivant():
                        g.matrix[i][j].mourir()
                        precedentID = g.matrix[i][j].get_id()
                        mode = 2
                    else: 
                        g.matrix[i][j].naitre()
                        precedentID = g.matrix[i][j].get_id()
                        mode = 1
                elif mode == 1:
                    if not g.matrix[i][j].est_vivant():
                        g.matrix[i][j].naitre()
                        precedentID = g.matrix[i][j].get_id()
                elif mode == 2:
                    if g.matrix[i][j].est_vivant():
                        g.matrix[i][j].mourir()
                        precedentID = g.matrix[i][j].get_id()
                g.actualise()
                dessin_cellules(g,cote)
                dessin_grille(g,cote,jeu)
        else:
            mode = 0
            precedentID = None
            
        if jeu:
            fenetre.fill((250,250,150))         # efface la fenetre avec la couleur
            g.jeux()
            g.actualise()
            dessin_cellules(g,cote)             # dessinne les cellules
            sleep(0.7)
        
        dessin_grille(g,cote,jeu)               # dessine la grille        
        
        pygame.display.flip()               # affiche des prÃ©sentations graphiques (nÃ©cessaire)
    pygame.quit()                           # mÃ©thode de fermeture de l'instance fenÃªtre



if __name__ == "__main__" :    
    main1(taille)