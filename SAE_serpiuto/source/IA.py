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
    nouveau_li=ligne.copy()
    nouveau_co=colonne.copy()
    for dir in liste:
        if dir =="N":
            ligne-=1
        if dir =="S":
            ligne+=1
        if dir =="O":
            colonne-=1
        if dir =="E":
            colonne+=1
    return (nouveau_li,nouveau_co)

def direction_possible_2(l_arene,x,y):
    mat=arene["matrice"]
    nb_lig=matrice.get_nb_lignes(mat)
    nb_col=matrice.get_nb_colonnes(mat)
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
            if x+1<nb_col:
                if not arene.est_mur(l_arene,x,y+1):
                    res+=dir
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
    x,y=arene.get_serpent(l_arene,num_joueur)[0]   #position de la tete
    res_dict=dict()
    chemin_liste=[[]]
    for _ in range(dist_max):
        nouvelle_liste=[]
        for chemin in chemin_liste:
            nouveau_x,nouveau_y=deplacement(chemin,x,y)
            if len(chemin_liste)==1:
                direction=directions_possibles(l_arene,num_joueur)   ##appel de fonction pas encore pret
            if len(chemin_liste)>1:
                direction=direction_possible_2(l_arene,nouveau_x,nouveau_y)
            for dir in direction:
                nouvelle_liste.append([chemin]+[dir])
        chemin_liste+=nouvelle_liste


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