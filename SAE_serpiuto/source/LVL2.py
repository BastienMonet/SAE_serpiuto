# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module IA.py
    Ce module implémente toutes les fonctions ainsi que l'IA de votre serpent
"""

import partie
import argparse
import client
import random
import arene
import case
import serpent
import matrice

direction_prec='X' # variable indiquant la décision précédente prise par le joueur. A mettre à jour soi-même

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

def directions_possibles(l_arene:dict,num_joueur:int)->str:
    """Indique les directions possible pour le joueur num_joueur
        c'est à dire les directions qu'il peut prendre sans se cogner dans
        un mur, sortir de l'arène ou se cogner sur une boîte trop grosse pour sa tête

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur

    Returns:
        str: une chaine composée de NOSE qui indique les directions
            pouvant être prise par le joueur. Attention il est possible
            qu'aucune direction ne soit possible donc la fonction peut retourner la chaine vide
    """ 
    res = ""
    pos_x, pos_y = arene.get_serpent(l_arene, num_joueur)[0]
    mat = l_arene['matrice']

    if est_sur_le_plateau(mat, pos_x-1, pos_y) and not case.est_mur(matrice.get_val(mat, pos_x-1, pos_y)):
        res += "N"
    if est_sur_le_plateau(mat, pos_x+1, pos_y) and not case.est_mur(matrice.get_val(mat, pos_x+1, pos_y)):
        res += "S"
    if est_sur_le_plateau(mat, pos_x, pos_y+1) and not case.est_mur(matrice.get_val(mat, pos_x, pos_y+1)):
        res += "E"
    if est_sur_le_plateau(mat, pos_x, pos_y-1) and not case.est_mur(matrice.get_val(mat, pos_x, pos_y-1)):
        res += "O"
    return chemin_sans_prec(res,direction_prec)

def unique_liste(liste):
    """permet d'enlever les elements commun dans une liste

    Args:
        liste (list): liste de liste

    Returns:
        list: _description_
    """
    vue = set()
    liste_unique = []
    for chaine in liste:
        if chaine not in vue:
            vue.add(chaine)
            liste_unique.append(chaine)
    return liste_unique

def deplacement(chemin,ligne,colonne):
    """calcule la nouvelle position en fonction d'un chemin de caractère NSEO de deplacement et d'un 
    etat initial

    Args:
        chemin (str): une suite de carractère NSEO
        ligne (int): la position x
        colonne (int): la position y

    Returns:
        tuple: _description_
    """    
    for dir in chemin:
        if dir =="N":
            ligne-=1
        if dir =="S":
            ligne+=1
        if dir =="O":
            colonne-=1
        if dir =="E":
            colonne+=1
    return (ligne,colonne)

def direction_possible_2(l_arene,x,y):
    """calcul les direcion possible mais a partir d'une coordonné

    Args:
        l_arene (_type_): _description_
        x (_type_): _description_
        y (_type_): _description_

    Returns:
        str: _description_
    """
    nb_lig,nb_col=arene.get_dim(l_arene)
    res=str()
    for dir in 'NSEO':
        if dir =='N':
            if not x-1<0:
                if not arene.est_mur(l_arene,x-1,y):
                    res+=dir
        if dir =='S':
            if x+1<nb_lig:
                if not arene.est_mur(l_arene,x+1,y):
                    res+=dir
        if dir =='O':
            if not y-1<0:
                if not arene.est_mur(l_arene,x,y-1):
                    res+=dir
        if dir =='E':
            if y+1<nb_col:
                if not arene.est_mur(l_arene,x,y+1):
                    res+=dir
    return res
    

def est_sur_le_plateau(la_matrice, pos_x, pos_y):
    """Indique si la position est bien sur le plateau

    Args:
        le_plateau (plateau): un plateau de jeu
        position (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 

    Returns:
        [boolean]: True si la position est bien sur le plateau
    """
    if pos_x >= 0 and pos_x <= matrice.get_nb_lignes(la_matrice)-1  and pos_y>= 0 and pos_y <= matrice.get_nb_colonnes(la_matrice)-1:
        return True
    else:
        return False


def chemin_sans_prec(chemin,prec):
    """renvoi la liste des direction possible sans la direction opposé, pour ne pas se manger soit meme

    Args:
        chemin (_type_): _description_
        prec (_type_): _description_

    Returns:
        _type_: _description_
    """
    res=''
    if prec=='X':   #initialisation du debut, lors du premier deplacement
        return chemin
    for lettr in chemin:
        if prec=='N':
            if not lettr=='S':
                res+=lettr
        if prec=='S':
            if not lettr=='N':
                res+=lettr
        if prec=='O':
            if not lettr=='E':
                res+=lettr
        if prec=='E':
            if not lettr=='O':
                res+=lettr
    return res


def mon_IA(num_joueur:int, la_partie:dict)->str:
    """Fonction qui va prendre la decision du prochain coup pour le joueur de numéro ma_couleur

    Args:
        num_joueur (int): un entier désignant le numero du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    # print(objets_voisinage(la_partie["arene"], num_joueur, 8))    
    direction=random.choice("NSEO")
    direction_prec=direction #La décision prise sera la direction précédente le prochain tour
    dir_pos=arene.directions_possibles(partie.get_arene(la_partie),num_joueur)
    if dir_pos=='':
        direction=random.choice('NOSE')
    else:
        direction=random.choice(dir_pos)
    return direction


if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu,_=le_client.prochaine_commande()
        if ok:
            la_partie=partie.partie_from_str(le_jeu)
            actions_joueur=mon_IA(int(id_joueur),la_partie)
            le_client.envoyer_commande_client(actions_joueur)
    le_client.afficher_msg("terminé")