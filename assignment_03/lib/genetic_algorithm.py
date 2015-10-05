import random
from common_algo import fitness_func
from logger import LOG

TARGET_VALUE = None


def init_population(pop_size):
    population = []
    min_limit = (pop_size / 2) * -1
    max_limit = (pop_size / 2)
    for count in range(0, pop_size):
        population.append(random.randint(1, max_limit))
    return population


def mutate_random(tuple_population):
    population = list(tuple_population)
    random_pos = random.randint(0, len(population)-1)
    random_delta = round(random.uniform(-1, 1), 2)
    population[random_pos] = population[random_pos] + random_delta
    return population


def search_ga(max_gens, pop_size, ad_mut_stp, mu_lambda):
    generation = 0
    population = init_population(pop_size)
    best = fitness_func(population)
    while generation < max_gens:
        new_population = mutate_random(tuple(population))
        new_best = fitness_func(new_population)
        if new_best <= best:
            LOG.debug("Better population>{0}".format(new_population))
            population = new_population
            best = new_best
        LOG.rbf("Generation>{0}:new best>{1}".format(generation, best))
        generation = generation + 1
