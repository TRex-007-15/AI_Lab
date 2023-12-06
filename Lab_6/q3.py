import random

# Define the size of the chessboard and population size
board_size = 8
population_size = 1000
mutation_rate = 0.1

# Function to initialize a random board state
def initialize_board():
    return [random.randint(0, board_size - 1) for _ in range(board_size)]

# Function to calculate the fitness of a board state
def calculate_fitness(board_state):
    conflicts = 0
    for col1 in range(board_size):
        for col2 in range(col1 + 1, board_size):
            row1, row2 = board_state[col1], board_state[col2]
            if row1 == row2 or abs(row1 - row2) == col2 - col1:
                conflicts += 1
    return conflicts

# Function for selection (tournament selection)
def select_parents(population):
    tournament_size = 5
    selected_parents = []
    for _ in range(population_size):
        tournament = random.sample(population, tournament_size)
        selected_parents.append(min(tournament, key=lambda x: calculate_fitness(x)))
    return selected_parents

# Function for crossover (single-point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, board_size - 2)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Function for mutation
def mutate(board_state):
    if random.random() < mutation_rate:
        index_to_mutate = random.randint(0, board_size - 1)
        new_row = random.randint(0, board_size - 1)
        board_state[index_to_mutate] = new_row
    return board_state

# Function for replacement (generational replacement)
def replace_population(population, children):
    population.extend(children)
    population.sort(key=lambda x: calculate_fitness(x))
    return population[:population_size]

# Main Genetic Algorithm loop
# Main Genetic Algorithm loop
def genetic_algorithm():
    population = [initialize_board() for _ in range(population_size)]
    generation = 0

    while True:
        population = select_parents(population)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = replace_population(population, new_population)
        generation += 1

        # Check for termination
        best_board_state = population[0]
        if calculate_fitness(best_board_state) == 0:
            print(f"Solved in {generation} generations!")
            return best_board_state

# Ask the user for the number of solutions required
num_solutions = int(input("The number of solutions required: "))
solutions = []

while len(solutions) < num_solutions:
    solution = genetic_algorithm()
    if solution not in solutions:
        solutions.append(solution)
        print("Solution:", solution)

print(f"Found {len(solutions)} unique solutions.")