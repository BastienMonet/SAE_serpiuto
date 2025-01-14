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
    return arene.directions_possibles(l_arene,num_joueur)

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

def deplacement(liste,ligne,colonne):
    """calcule la nouvelle position en fonction d'une liste de deplacement et d'un 
    etat initial

    Args:
        liste (_type_): _description_
        ligne (_type_): _description_
        colonne (_type_): _description_

    Returns:
        tuple: _description_
    """    
    nouveau_li=ligne
    nouveau_co=colonne
    if liste is not None:
        for dir in liste:
            if dir =="N":
                nouveau_li-=1
            if dir =="S":
                nouveau_li+=1
            if dir =="O":
                nouveau_co-=1
            if dir =="E":
                nouveau_co+=1
    return (nouveau_li,nouveau_co)

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


def getvoisins(la_matrice, pos_x, pos_y):
    """Renvoie l'ensemble des positions cases voisines accessibles de la position renseignées
       Une case accessible est une case qui est sur le plateau et qui n'est pas un mur
    Args:
        matrice (plateau): une matrice de jeu
        position (tuple): un tuple de deux entiers de la forme (pos_x, pos_y) 

    Returns:
        set: l'ensemble des positions des cases voisines accessibles
    """
    les_voisins = set()
    if est_sur_le_plateau(la_matrice, pos_x, pos_y+1):
        les_voisins.add((pos_x, pos_y+1))
    if est_sur_le_plateau(la_matrice, pos_x, pos_y-1):
        les_voisins.add((pos_x, pos_y-1))
    if est_sur_le_plateau(la_matrice, pos_x+1, pos_y):
        les_voisins.add((pos_x+1, pos_y))
    if est_sur_le_plateau(la_matrice, pos_x-1, pos_y):
        les_voisins.add((pos_x-1, pos_y))
    return les_voisins 



def calque_a_mur(l_arene:dict):
    """crée un calque de l'arène

    Args:
        l_arene (dict): l'arène de la partie

    Returns:
        [list]: retourne la matrice calque avec les mur noté "M" et toute les autres cases à None
    """

    nb_ligne,nb_colonne  = arene.get_dim(l_arene)
    calque = matrice.Matrice(nb_ligne, nb_colonne)
    for x in range(nb_ligne):
        for y in range(nb_colonne):
            if arene.est_mur(l_arene, x, y):
                matrice.set_val(calque, x, y, "M")
    return calque


def pos_a_distance(l_arene:dict, num_joueur, dist_max:int)->list:
    """effectue l'inondation sur le calque en fonction de la distance max pris en paramètre 

    Args:
        l_arene (dict): l'arène de la partie
        num_joueur (int): le joueur dont on souhaite évaluer la position
        dist_max (int): la distance max a respecter

    Returns:
        tuple (liste_position, calque): retourne une liste de tuple contenant toutes les positions 
        présentant un objet ou une presence d'un joueur avec le calque effectif
    """
    liste_positions = []
    pos_init_x, pos_init_y=arene.get_serpent(l_arene,num_joueur)[0]

    nb_ligne,nb_colonne  = arene.get_dim(l_arene)
    calque = calque_a_mur(l_arene)
    matrice.set_val(calque, pos_init_x, pos_init_y, 0)
    compteur = 0

    voisin_act = [(pos_init_x, pos_init_y)]
    voisin_suiv = []
    
    while compteur < dist_max:
        # for x in range(nb_ligne):
        #     for y in range(nb_colonne):
        for x, y in voisin_act:
            if matrice.get_val(calque, x, y) == compteur:
                voisins = getvoisins(calque, x ,y)
                for (voisin_x, voisin_y) in voisins:
                    if matrice.get_val(calque, voisin_x, voisin_y) is None:
                        voisin_suiv.append((voisin_x, voisin_y))
                        matrice.set_val(calque, voisin_x, voisin_y, compteur+1)
                        if arene.get_val_boite(l_arene, voisin_x, voisin_y) != 0 or arene.get_proprietaire(l_arene, voisin_x, voisin_y) != 0:
                            liste_positions.append((voisin_x, voisin_y))
                                
        compteur += 1
        voisin_act = voisin_suiv
    matrice.affiche(calque)
    #print(liste_positions)
    return liste_positions, calque

def fabrique_chemin(calque, position_arr):
    """Renvoie le plus court chemin entre position_depart position_arrivee

    Args:
        le_plateau (plateau): un plateau de jeu
        position_depart (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        position_arrivee (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 

    Returns:
        list: Une liste de positions entre position_arrivee et position_depart
        qui représente un plus court chemin entre les deux positions
    """
    chemin = [position_arr]
    valeur_act = matrice.get_val(calque, position_arr[0], position_arr[1])
    while valeur_act != 0:
        les_voisins = getvoisins(calque, chemin[-1][0], chemin[-1][1])
        for (voisin_x, voisin_y) in les_voisins:
            if matrice.get_val(calque, voisin_x, voisin_y) == valeur_act - 1:
                chemin.append((voisin_x, voisin_y))
                valeur_act -= 1
    return chemin[::-1]


def chemin_to_cardinal(chemin):
    """transforme une suite de position en suite de Nord Sud Est Ouest

    Args:
        chemin (list(tuple)): une liste de position

    Returns:
        str: retourne une suite d'instruction NSEO a réaliser pour réaliser le chemin
    """
    res = ""
    for i in range(len(chemin)-1):
        x, y = chemin[i]
        if chemin[i+1] == (x+1, y):
            res+= "S"
        elif chemin[i+1] == (x-1, y):
            res+= "N"
        elif chemin[i+1] == (x, y+1):
            res+= "E"
        elif chemin[i+1] == (x, y-1):
            res+= "O"
    return res


def objets_voisinage(l_arene:dict, num_joueur, dist_max:int):  # au minimum 1
    """Retourne un dictionnaire indiquant pour chaque direction possibles, 
        les objets ou boites pouvant être mangés par le serpent du joueur et
        se trouvant dans voisinage de la tête du serpent 

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        dist_max (int): le nombre de cases maximum qu'on s'autorise à partir du point de départ
    Returns:
        dict: un dictionnaire dont les clés sont des directions  et les valeurs une liste de triplets
            (distance,val_objet,prop) où distance indique le nombre de cases jusqu'à l'objet et id_objet
            val_obj indique la valeur de l'objet ou de la boite et prop indique le propriétaire de la boite
    """

    res={}
    liste_pos, calque = pos_a_distance(l_arene, num_joueur, dist_max)
    for position in liste_pos:
        chemin = fabrique_chemin(calque, position)
        cardinal = chemin_to_cardinal(chemin)
        res[cardinal] = [matrice.get_val(calque, position[0], position[1]), arene.get_val_boite(l_arene, position[0], position[1]), arene.get_proprietaire(l_arene, position[0], position[1])]
    return res



def mon_IA2(num_joueur:int, la_partie:dict)->str:
    return 'N'

def mon_IA(num_joueur:int, la_partie:dict)->str:
    """Fonction qui va prendre la decision du prochain coup pour le joueur de numéro ma_couleur

    Args:
        num_joueur (int): un entier désignant le numero du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    print(objets_voisinage(la_partie["arene"], num_joueur, 3))    
    direction=random.choice("NSEO")
    direction_prec=direction #La décision prise sera la direction précédente le prochain tour
    dir_pos=arene.directions_possibles(partie.get_arene(la_partie),num_joueur)
    if dir_pos=='':
        direction=random.choice('NOSE')
    else:
        direction=random.choice(dir_pos)
    return direction

def mon_IA3(num_joueur:int, la_partie:dict)->str: 
    res=''
    val_tete=0





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