
import random
import math

# ==========================================
# DONNEES DU PROBLEME
# ==========================================
COUTS = [
    [0,    14,   15,   None, None, None, None, 17],
    [14,   0,    13,   14,   20,   None, None, 21],
    [15,   13,   0,    11,   21,   17,   9,    9],
    [None, 14,   11,   0,    11,   10,   8,   20],
    [None, 20,   21,   11,   0,    15,   18, None],
    [None, None, 17,   10,   15,   0,    9,   None],
    [None, None, 9,    8,    18,   9,    0,   13],
    [17,   21,   9,    20,   None, None, 13,   0]
]


def cout_tour(tour):
    total = 0

    for i in range(len(tour) - 1):
        ville1 = tour[i] - 1
        ville2 = tour[i + 1] - 1

        cout = COUTS[ville1][ville2]

        if cout is None:
            return math.inf

        total += cout

    return total


def afficher_tour(tour):
    return " -> ".join(map(str, tour))
def voisins_tabou(tour):
    resultat = []
    for i in range(1, len(tour) - 2):
        for j in range(i + 1, len(tour) - 1):
            nouveau = tour[:]
            nouveau[i], nouveau[j] = nouveau[j], nouveau[i]

            if cout_tour(nouveau) != math.inf:
                resultat.append(nouveau)

    return resultat


def recherche_taboue(iterations=100, taille_tabou=10):
    courant = [1, 2, 3, 4, 5, 6, 7, 8, 1]
    meilleure_solution = courant[:]
    liste_taboue = []

    print("\n===================================")
    print("QUESTION 1 : RECHERCHE TABOUE")
    print("===================================")
    print("Tour initial :", afficher_tour(courant))
    print("Cout initial :", cout_tour(courant))

    for iteration in range(1, iterations + 1):
        candidats = voisins_tabou(courant)

        candidats = [
            candidat for candidat in candidats
            if candidat not in liste_taboue
        ]

        if not candidats:
            break
        candidat = min(candidats, key=cout_tour)
        courant = candidat[:]

        liste_taboue.append(courant[:])

        if len(liste_taboue) > taille_tabou:
            liste_taboue.pop(0)

        if cout_tour(courant) < cout_tour(meilleure_solution):
            meilleure_solution = courant[:]

        print(
            "Iteration", iteration,
            "| Tour :", afficher_tour(courant),
            "| Cout :", cout_tour(courant)
        )

    print("\nMeilleure solution par recherche taboue :")
    print("Tour :", afficher_tour(meilleure_solution))
    print("Cout total :", cout_tour(meilleure_solution))

    return meilleure_solution

def voisin_aleatoire(tour):
    for _ in range(1000):
        nouveau = tour[:]

        i, j = random.sample(range(1, 8), 2)
        nouveau[i], nouveau[j] = nouveau[j], nouveau[i]

        if cout_tour(nouveau) != math.inf:
            return nouveau

    return tour[:]


def recuit_simule(iterations=5, temperature=50, alpha=0.8):
    random.seed(7)

    courant = [1, 2, 3, 4, 5, 6, 7, 8, 1]
    meilleure_solution = courant[:]

    print("\n===================================")
    print("QUESTION 2 : RECUIT SIMULE")
    print("===================================")
    print("Tour initial :", afficher_tour(courant))
    print("Cout initial :", cout_tour(courant))
    print("Temperature initiale :", temperature)

    for iteration in range(1, iterations + 1):
        candidat = voisin_aleatoire(courant)

        cout_courant = cout_tour(courant)
        cout_candidat = cout_tour(candidat)
        delta = cout_candidat - cout_courant
        if delta <= 0:
            accepter = True
        else:
            probabilite = math.exp(-delta / temperature)
            accepter = random.random() < probabilite

        if accepter:
            courant = candidat[:]

        if cout_tour(courant) < cout_tour(meilleure_solution):
            meilleure_solution = courant[:]

        print("\nIteration :", iteration)
        print("Tour candidat :", afficher_tour(candidat))
        print("Cout candidat :", cout_candidat)
        print("Variation du cout :", delta)
        print("Solution acceptee :", accepter)
        print("Cout courant :", cout_tour(courant))
        temperature = temperature * alpha
        print("Temperature suivante :", round(temperature, 2))

    print("\nMeilleure solution par recuit simule :")
    print("Tour :", afficher_tour(meilleure_solution))
    print("Cout total :", cout_tour(meilleure_solution))

    return meilleure_solution

if __name__ == "__main__":
    recherche_taboue()
    recuit_simule()
