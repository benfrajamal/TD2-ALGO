# ==========================================
# EXERCICE 2 : PROBLEME DE TRANSPORT
# METHODE DE RECHERCHE TABOUE
# ==========================================
COUTS = [
    [5, 3, 4],
    [6, 7, 2]
]
CAPACITES = [8, 9]
DEMANDES = [4, 5, 8]

def cout_total(solution):
    total = 0

    for i in range(2):
        for j in range(3):
            total += solution[i][j] * COUTS[i][j]

    return total

def solution_valide(solution):
    # Verifier les capacites des depots
    for i in range(2):
        if sum(solution[i]) != CAPACITES[i]:
            return False
    for j in range(3):
        total_livre = solution[0][j] + solution[1][j]

        if total_livre != DEMANDES[j]:
            return False

    return True

def solution_initiale():
    return [
        [4, 4, 0],  # Depot D1
        [0, 1, 8]   # Depot D2
    ]
def generer_voisins(solution):
    voisins = []
    for j in range(3):
        for origine, destination in [(0, 1), (1, 0)]:

            if solution[origine][j] > 0:
                nouvelle_solution = [
                    solution[0][:],
                    solution[1][:]
                ]

                nouvelle_solution[origine][j] -= 1
                nouvelle_solution[destination][j] += 1

                if solution_valide(nouvelle_solution):
                    voisins.append(nouvelle_solution)

    return voisins
def recherche_taboue(iterations=100, taille_taboue=5):
    courant = solution_initiale()
    meilleure_solution = [
        courant[0][:],
        courant[1][:]
    ]

    liste_taboue = []

    print("===================================")
    print("EXERCICE 2 : RECHERCHE TABOUE")
    print("===================================")

    print("Solution initiale :")
    print("D1 :", courant[0])
    print("D2 :", courant[1])
    print("Cout initial :", cout_total(courant))

    for iteration in range(1, iterations + 1):
        candidats = generer_voisins(courant)
        candidats = [
            candidat for candidat in candidats
            if candidat not in liste_taboue
        ]

        if not candidats:
            break
        candidat = min(candidats, key=cout_total)

        courant = [
            candidat[0][:],
            candidat[1][:]
        ]

        liste_taboue.append([
            courant[0][:],
            courant[1][:]
        ])

        if len(liste_taboue) > taille_taboue:
            liste_taboue.pop(0)
        if cout_total(courant) < cout_total(meilleure_solution):
            meilleure_solution = [
                courant[0][:],
                courant[1][:]
            ]

        print(
            "Iteration", iteration,
            "- Cout :", cout_total(courant)
        )

    return meilleure_solution
solution = recherche_taboue()

print("\n===================================")
print("SOLUTION FINALE")
print("===================================")

print("Depot D1 :")
print("M1 =", solution[0][0], "conteneurs")
print("M2 =", solution[0][1], "conteneurs")
print("M3 =", solution[0][2], "conteneurs")

print("\nDepot D2 :")
print("M1 =", solution[1][0], "conteneurs")
print("M2 =", solution[1][1], "conteneurs")
print("M3 =", solution[1][2], "conteneurs")

print("\nCout total minimal :", cout_total(solution))
print("Solution valide :", solution_valide(solution))
