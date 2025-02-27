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
    return chemin_sans_prec(res,direction_prec)    #condition suplémentaire, pour eviter de revenir sur le chemin et par conséquant de se manger soi-meme


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
    #matrice.affiche(calque)     permet d'afficher le calque
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


def trouve_serpent(num_joueur, l_arene):
    """trouve le serpent qui a le numero de joueur indiquer

    Args:
        num_joueur (int): numero du joueur dont on veut verifier la protection
        l_arene (dict): l'arène

    Returns:
        dict: retourne le serpent voulu
    """
    for serp in l_arene["serpents"]:
        if serpent.get_num_joueur(serp) == num_joueur:
            return serp
    return serp



def is_protection(num_joueur,l_arene):
    """true si un adversaire possede une protection 

    Args:
        num_joueur (int): numero du joueur dont on veut verifier la protection
        l_arene (dict): l'arène
    return bool
    """
    return serpent.get_temps_protection(trouve_serpent(num_joueur, l_arene))>0 


def is_surpuissance(num_joueur,l_arene):
    """permet de savoir si le serpent possede le bonus surpuissance

    Args:
        num_joueur (_type_): _description_
        l_arene (_type_): _description_

    Returns:
        bool: _description_
    """
    return serpent.get_temps_surpuissance(trouve_serpent(num_joueur, l_arene))>0 


def get_val_tete(num_joueur, l_arene):
    """get la valeur de la tête du serpent du joueur num_joueur

    Args:
        num_joueur (int): le numero du joueur dont on souhaite évalué la tête
        l_arene (dict): l'arène

    Returns:
        _type_: _description_
    """
    pos_x, pos_y = arene.get_serpent(l_arene, num_joueur)[0] # get la position de la tête du serpent
    #print(arene.get_val_boite(l_arene,pos_x,pos_y))
    return arene.get_val_boite(l_arene,pos_x,pos_y)

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

def car_inverse(prec):
    """renvoi la direction impossible a prendre, utile pour revinir en arriere lors d'une impasse

    Args:
        prec (_type_): _description_

    Returns:
        str: _description_
    """
    res=''
    if prec=='N':
        res= 'S'
    elif prec=='S':
        res= 'N'
    elif prec=='O':
        res= 'E'
    elif prec=='E':
        res= 'O'
    return res


def mini_chemin_boite(liste,val_tete):
    """renvoi le plus petit chemin pour aller vers une boite , en fontion de la valeur de la tete
    le dico est trié par rapport au clé, donc du chemin le plus rapide au plus long
    Args:
        liste (_type_): _description_
    """
    if val_tete>1:
        cible=2
    else:
        cible=1
    for chemin,spec in liste.items():
        _,val,propri=spec
        if val==cible and propri==0:
            return chemin


def get_case_from_chemin(chemin, pos_x, pos_y, l_arene):
    """retrouve la case arrivée à partir d'une position de départ et d'un chemin

    Args:
        chemin (str): une suite de caractère NSEO  
        pos_x (int): la position en x
        pos_y (int): la position en y

    Returns:
        dict: retourne la case ou l'objet ce situe
    """

    pos_final_x , pos_final_y = deplacement(chemin, pos_x, pos_y)
    # print(matrice.get_val(l_arene["matrice"], pos_final_x, pos_final_y))
    return matrice.get_val(l_arene["matrice"], pos_final_x, pos_final_y)

def mon_IA(num_joueur:int, la_partie:dict)->str: 
    """cette fonction renvoie la direction a prendre, en fonction de la position du joueur et de l'invironement

    Args:
        num_joueur (int): _description_
        la_partie (dict): _description_

    Returns:
        str: _description_
    """
    res=''              #sauvargde la solution afin de modifier la variable direction_prec
    l_arene=la_partie["arene"]      #recupere le 'arene
    val_tete=get_val_tete(num_joueur,l_arene)  #permet de recuperer la valeur de la tete    
    pos_x, pos_y = arene.get_serpent(l_arene, num_joueur)[0]
    dico_val=objets_voisinage(l_arene,num_joueur,9) #valeur 9 car c'est la distance maximum que l'on peut parcourir avant que l'objet disparraisse
    global direction_prec       
    if val_tete>16:   #defini le niveau d'agréssivité du serpent, soit la distance pour aller chercher les autres joueur
        agressivite=3
    else:
        agressivite=1
    if dico_val=={}:    # si il n'y a pas d'objet dans un rayon de 9, alors le serpent prend une direction aléatoire possible
        res=random.choice(directions_possibles(l_arene,num_joueur))
        direction_prec=res         
        return res
    for chemin,spec in dico_val.items():        # permet de parcourir les objets de la plus proche a la plus longue
        distance,valeur_case,numero_joueur=spec       
        if num_joueur==numero_joueur:       #passe les objets qui correspondent a notre serpent
            continue
        if valeur_case == -5:
            continue
        if not chemin[0]==car_inverse(direction_prec) or len(arene.get_serpent(l_arene,num_joueur))==1:   #permet de ne pas se manger
            if valeur_case == 1  or valeur_case == -1 or valeur_case == -2 and val_tete == 1 and numero_joueur==0:
                if case.get_val_temps(get_case_from_chemin(chemin, pos_x, pos_y, l_arene))[1]>=distance: 
                    res=chemin[0]
                    direction_prec=res                     
                    return res
            if distance<=agressivite and numero_joueur > 0:     
                if valeur_case<=val_tete or is_surpuissance(num_joueur,l_arene) and not is_protection(numero_joueur,l_arene):    #condition pour manger un serpent a une certaine distance, si les conditions sont reunies
                    res=chemin[0]
                    direction_prec=res                     
                    return res
            if len(arene.get_serpent(l_arene,num_joueur))==1 or valeur_case == -1 or valeur_case == -2:    #permet de focus les multiplications et addition si la on a que la tete 
                 if case.get_val_temps(get_case_from_chemin(chemin, pos_x, pos_y, l_arene))[1]>=distance:
                    res=chemin[0]
                    direction_prec=res                     
                    return res
            if 1<=valeur_case<=2 and numero_joueur == 0 and val_tete>=valeur_case or is_surpuissance(num_joueur,l_arene):            # condition , si on peut et on a le temps de manger une boite de valeur 1 ou 2 
                if case.get_val_temps(get_case_from_chemin(chemin, pos_x, pos_y, l_arene))[1]>=distance:  
                    res=chemin[0]
                    direction_prec=res                     
                    return res
            if valeur_case==-4 and distance<=2 and not is_surpuissance(num_joueur,l_arene):         #condition , si l'objet le plus proche est un protection et que celui ci est toujours dispo
                if case.get_val_temps(get_case_from_chemin(chemin, pos_x, pos_y, l_arene))[1]>=distance:                    
                    res=chemin[0]
                    direction_prec=res                     
                    return res   
            if valeur_case==-2 and distance==1:
                 if case.get_val_temps(get_case_from_chemin(chemin, pos_x, pos_y, l_arene))[1]>=distance:           #prend un bonus multiplication si il est a coté de nous
                    res=chemin[0]
                    direction_prec=res                     
                    return res   
            if valeur_case==-1 and distance==1:
                 if case.get_val_temps(get_case_from_chemin(chemin, pos_x, pos_y, l_arene))[1]>=distance:       #prend un bonus addition si il est a coté de nous
                    res=chemin[0]
                    direction_prec=res                     
                    return res 
    if res == '':               #si le serpent se retouve dans une impasse
        if directions_possibles(l_arene,num_joueur)=='':
            res=car_inverse(direction_prec)
            direction_prec=res             
            return res
        else:               #evite d'avoir une fonction qui renvoie None
            res=random.choice(directions_possibles(l_arene,num_joueur))
            direction_prec=res             
            return res



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
