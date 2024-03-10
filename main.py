import TetrisAI
from NN_GA import Population
from joblib import Parallel, delayed
from copy import deepcopy


# Parallel execution using Joblib
# Function to be parallelized
def run_tetris(model):
    return TetrisAI.comenzar_tetris(ai_model=model)


n_cores = 8

# Neur
input_size = 13
output_size = 1
weights_init_min = -1
weights_init_max = 1

GENERATIONS = 10
GENERATIONS_SIZE = 50
old_population = None
current_population = Population(
    input_size, output_size, weights_init_min, weights_init_max, size=GENERATIONS_SIZE
)
for i in range(GENERATIONS):
    print(f"Generation {i}")
    fitness_scores = []
    old_population = deepcopy(current_population)
    # Serie
    # for model in old_population.models:
    #     score = run_tetris(model)
    #     fitness_scores.append(score)
    # Paralelo
    fitness_scores = Parallel(n_jobs=n_cores)(
        delayed(run_tetris)(model) for model in old_population.models
    )
    old_population.fitnesses = fitness_scores
    current_population = Population(
        input_size,
        output_size,
        weights_init_min,
        weights_init_max,
        size=GENERATIONS_SIZE,
        old_population=old_population,
    )
    print(max(fitness_scores))
    print(
        old_population.models[
            fitness_scores.index(max(fitness_scores))
        ].output.weight.data[0]
    )
