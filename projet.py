import numpy as np
from collections import deque

#PARTIE 1 
# Lecture d'un tableau de contraintes à partir d'un fichier texte
def lire_contraintes(fichier_txt):
    contraintes = {}
    with open(fichier_txt, 'r') as fichier:
        for ligne in fichier:
            elements = list(map(int, ligne.strip().split()))
            if elements:
                contraintes[elements[0]] = {'duree': elements[1], 'pred': elements[2:]}
    return contraintes

#PARTIE 2
# Création de la matrice des valeurs (graphe)
def creer_matrice(contraintes):
    N = len(contraintes)
    taille = N + 2
    matrice = np.full((taille, taille), '*', dtype=object)

    for i in range(taille):
        for j in range(taille):
            matrice[i][j] = '*'

    # Ajouter les arcs depuis le sommet fictif initial (0)
    for tache, info in contraintes.items():
        if not info['pred']:
            matrice[0][tache] = 0

    # Ajouter les arcs normaux
    for tache, info in contraintes.items():
        for pred in info['pred']:
            matrice[pred][tache] = contraintes[pred]['duree']

    # Identifier explicitement toutes les tâches sans successeurs
    successeurs = set()
    for tache, info in contraintes.items():
        successeurs.update(info['pred'])

    for tache in contraintes:
        if tache not in successeurs:
            matrice[tache][N+1] = contraintes[tache]['duree']

    return matrice

# Affichage propre et aligné de la matrice
def afficher_matrice(matrice):
    N = len(matrice)
    largeur_colonne = 4
    entete = " " * largeur_colonne + "".join(f"{i:>{largeur_colonne}}" for i in range(N))
    print("\nMatrice des valeurs :")
    print(entete)
    for idx, ligne in enumerate(matrice):
        ligne_affichee = "".join(f"{str(elem):>{largeur_colonne}}" for elem in ligne)
        print(f"{idx:<{largeur_colonne}}{ligne_affichee}")


#PARTIE 3
# Vérification de circuit par la méthode de suppression des points d'entrée
def verifier_circuit_suppression(matrice):
    N = len(matrice)
    indegres = [0] * N

    for i in range(N):
        for j in range(N):
            if matrice[i][j] != '*':
                indegres[j] += 1

    restants = set(range(N))
    print("\nDetection de circuit par suppression des points d'entree :")
    while restants:
        entrees = [i for i in restants if indegres[i] == 0]
        if not entrees:
            print("-> Circuit detecte")
            return False

        print("Points d'entree :", " ".join(map(str, entrees)))
        print("Suppression des points d'entree")
        for entree in entrees:
            restants.remove(entree)
            for succ in range(N):
                if matrice[entree][succ] != '*':
                    indegres[succ] -= 1

        print("Sommets restant :", " ".join(map(str, sorted(restants))) if restants else "Aucun")

    print("-> Il n'y a pas de circuit")
    return True

#PARTIE 4
# Calcul des rangs des sommets
def calculer_rangs(matrice):
    N = len(matrice)
    indegres = [0] * N
    rangs = [0] * N

    for i in range(N):
        for j in range(N):
            if matrice[i][j] != '*':
                indegres[j] += 1

    queue = deque([i for i in range(N) if indegres[i] == 0])

    while queue:
        sommet = queue.popleft()
        for succ in range(N):
            if matrice[sommet][succ] != '*':
                indegres[succ] -= 1
                if indegres[succ] == 0:
                    rangs[succ] = rangs[sommet] + 1
                    queue.append(succ)

    return rangs

# Calcul des calendriers et marges
def calculer_calendriers_et_marges(matrice):
    N = len(matrice)
    tot = [0] * N

    # Calcul des dates au plus tôt
    for i in range(N):
        for j in range(N):
            if matrice[i][j] != '*':
                tot[j] = max(tot[j], tot[i] + matrice[i][j])

    # Initialiser tard avec la durée totale du projet
    duree_totale = max(tot)
    tard = [duree_totale] * N

    # Calcul des dates au plus tard
    for i in reversed(range(N)):
        if all(matrice[i][k] == '*' for k in range(N)):
            tard[i] = duree_totale
        for j in range(N):
            if matrice[i][j] != '*':
                tard[i] = min(tard[i], tard[j] - matrice[i][j])

    # Calcul des marges
    marges = [tard[i] - tot[i] for i in range(N)]

    return tot, tard, marges


#PARTIE 6
# Calcul du chemin critique
def chemins_critiques(marges):
    return [i for i, marge in enumerate(marges) if marge == 0]

if __name__ == "__main__":

    #PARTIE 1
    fichier = "Tables de contraintes/table 14.txt" 
    contraintes = lire_contraintes(fichier)
    print("Contraintes stockees en memoire :")
    for k, v in contraintes.items():
        print(f"Tache {k}: Duree = {v['duree']}, Predecesseurs = {v['pred']}")

    #PARTIE 2
    matrice = creer_matrice(contraintes)
    afficher_matrice(matrice)

    #PARTIE 3
    print("\nVerification du graphe :")
    valide = verifier_circuit_suppression(matrice)
    if valide:
        print("Il n'y a pas d'arcs negatifs\n-> C'est un graphe d'ordonnancement")
        #PARTIE 4
        rangs = calculer_rangs(matrice)
        print("\nRangs des sommets :")
        for idx, rang in enumerate(rangs):
            print(f"Sommet {idx} : Rang {rang}")
        #PARTIE 5
        tot, tard, marges = calculer_calendriers_et_marges(matrice)
        print("\nCalendrier au plus tot :", tot)
        print("Calendrier au plus tard :", tard)
        print("Marges :", marges)

        #PARTIE 6
        critique = chemins_critiques(marges)
        print("\nChemin(s) critique(s) :", critique)