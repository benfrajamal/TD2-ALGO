import random
# ==========================================
# 1. DONNEES DU PROBLEME
# ==========================================

CAPACITES = [20, 15, 35, 40, 15, 15, 10]
DEMANDES = [80, 90, 65, 70]

CAPACITE_TOTALE = sum(CAPACITES)

# Configurations autorisees pour chaque centrale
OPTIONS = [
    ["1100", "0110", "0011"],  # U1
    ["1100", "0110", "0011"],  # U2
    ["1000", "0100", "0010", "0001"],  # U3
    ["1000", "0100", "0010", "0001"],  # U4
    ["1000", "0100", "0010", "0001"],  # U5
    ["1000", "0100", "0010", "0001"],  # U6
    ["1000", "0100", "0010", "0001"]   # U7
]

# ==========================================
# 2. PARAMETRES DE L'AG
# ==========================================

TAILLE_POPULATION = 50
NB_GENERATIONS = 200
PROBA_CROISEMENT = 0.8
PROBA_MUTATION = 0.15
NB_ELITES = 2
random.seed(42)

# 3. CREATION D'UN CHROMOSOME
def creer_chromosome():
    chromosome = []
    for options in OPTIONS:
        gene = random.choice(options)
        chromosome.append(gene)
    return chromosome

# 4. FONCTION D'EVALUATION (FITNESS)
def evaluer(chromosome):
    pertes = [0, 0, 0, 0]
    for i, gene in enumerate(chromosome):
        for j in range(4):
            if gene[j] == "1":
                pertes[j] += CAPACITES[i]
    reserves = []
    for j in range(4):
        reserve = CAPACITE_TOTALE - pertes[j] - DEMANDES[j]
        reserves.append(reserve)
    # Maximiser la reserve minimale
    if min(reserves) > 0:
        fitness = min(reserves)
    else:
        fitness = 0
    return fitness, reserves, pertes

# 5. SELECTION PAR LOTERIE
def selection_loterie(population):
    fitnesses = [evaluer(ch)[0] for ch in population]
    total = sum(fitnesses)
    if total == 0:
        return random.choice(population)[:]
    tirage = random.uniform(0, total)
    cumul = 0
    for chromosome, fitness in zip(population, fitnesses):
        cumul += fitness
        if cumul >= tirage:
            return chromosome[:]
    return population[-1][:]

# 6. CROISEMENT A UN POINT
def croisement(parent1, parent2):
    if random.random() > PROBA_CROISEMENT:
        return parent1[:], parent2[:]
    point = random.randint(1, len(parent1) - 1)
    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]
    return enfant1, enfant2

# 7. MUTATION PAR INVERSION
def mutation_inversion(chromosome):
    mutant = chromosome[:]
    for i in range(len(mutant)):
        if random.random() < PROBA_MUTATION:
            mutant[i] = mutant[i][::-1]
    return mutant

# 8. MUTATION PAR REMPLACEMENT
def mutation_remplacement(chromosome):
    mutant = chromosome[:]
    for i in range(len(mutant)):
        if random.random() < PROBA_MUTATION:
            choix = [
                gene for gene in OPTIONS[i]
                if gene != mutant[i]
            ]
            if choix:
                mutant[i] = random.choice(choix)
    return mutant

# 9. AFFICHAGE DE LA MEILLEURE SOLUTION
def afficher_solution(chromosome):
    fitness, reserves, pertes = evaluer(chromosome)
    print("\n========== MEILLEURE SOLUTION ==========")
    for i, gene in enumerate(chromosome):
        print("Unite U", i + 1, ":", gene)
    print("\nPuissance perdue pendant la maintenance :")
    for j in range(4):
        print("Intervalle I", j + 1, ":", pertes[j], "MW")
    print("\nReserves de puissance :")
    for j in range(4):
        print(
            "Intervalle I", j + 1,
            ":", CAPACITE_TOTALE,
            "-", pertes[j],
            "-", DEMANDES[j],
            "=", reserves[j], "MW"
        )
    print("\nFitness finale :", fitness, "MW")
    print("========================================")

# 10. ALGORITHME GENETIQUE
def algorithme_genetique(utiliser_remplacement=False):
    # Initialisation de la population
    population = [
        creer_chromosome()
        for _ in range(TAILLE_POPULATION)
    ]
    meilleur_global = None
    meilleure_fitness = -1

    # Evolution sur plusieurs generations
    for generation in range(NB_GENERATIONS):
        population.sort(
            key=lambda ch: evaluer(ch)[0],
            reverse=True
        )
        fitness_actuelle = evaluer(population[0])[0]
        if fitness_actuelle > meilleure_fitness:
            meilleure_fitness = fitness_actuelle
            meilleur_global = population[0][:]

        # Elitisme
        nouvelle_population = [
            ch[:] for ch in population[:NB_ELITES]
        ]
        while len(nouvelle_population) < TAILLE_POPULATION:

            # Selection
            parent1 = selection_loterie(population)
            parent2 = selection_loterie(population)

            # Croisement
            enfant1, enfant2 = croisement(parent1, parent2)

            # Mutation
            if utiliser_remplacement:
                enfant1 = mutation_remplacement(enfant1)
                enfant2 = mutation_remplacement(enfant2)
            else:
                enfant1 = mutation_inversion(enfant1)
                enfant2 = mutation_inversion(enfant2)
            nouvelle_population.append(enfant1)
            if len(nouvelle_population) < TAILLE_POPULATION:
                nouvelle_population.append(enfant2)
        population = nouvelle_population
        if generation % 20 == 0 or generation == NB_GENERATIONS - 1:
            print(
                "Generation", generation,
                "| Meilleure fitness :",
                meilleure_fitness, "MW"
            )

    # Verification de la derniere population
    population.sort(
        key=lambda ch: evaluer(ch)[0],
        reverse=True
    )
    if evaluer(population[0])[0] > meilleure_fitness:
        meilleur_global = population[0][:]
        meilleure_fitness = evaluer(meilleur_global)[0]
    afficher_solution(meilleur_global)
    return meilleur_global


# 11. PROGRAMME PRINCIPAL
if __name__ == "__main__":
    print("ALGORITHME GENETIQUE - LSI3")
    print("Probleme d'ordonnancement des taches")
    print("Methode de selection : Loterie")
    print("Methode de mutation : Inversion")
    solution = algorithme_genetique()


