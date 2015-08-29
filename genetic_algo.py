#!/usr/bin/python
import random

POPULATION_X = 100
POPULATION_SIZE = 10
POPULATION_COUNT = 0
TARGET = 50


def init_population():
    phenotype = []
    global POPULATION_COUNT
    for i in range(0, POPULATION_SIZE):
        POPULATION_COUNT = POPULATION_COUNT + 1
        new_individual = (i, POPULATION_COUNT, \
                          random.randint(-POPULATION_X, POPULATION_X), 0)
        phenotype.append(new_individual)
    return phenotype


def quality_function(x):
    return TARGET-(x*x)


def get_key(item):
    x = item[3]
    return


def random_algorithm(gene, pheno):
    results = []
    generation = []
    _rand_index_change = random.randint(0, POPULATION_SIZE-1)
    _rand_index_kill = random.randint(0, POPULATION_SIZE)
    _delta = round(random.uniform(-1, 1), 1)
    _, _, _ind_2_change, _ = pheno[_rand_index_change]
    _new_ind = _ind_2_change + _delta
    pheno.append((POPULATION_SIZE, POPULATION_COUNT+1, _new_ind, 0))
    print "Generation>{0}".format(gene)
    print pheno
    for index, id_num, p, _ in pheno:
        qual_result = quality_function(p)
        evaluation = (index, id_num, p, qual_result)
        results.append(evaluation)
    sorted_results = sorted(results, key=lambda x: abs(x[3]-TARGET))
    sorted_results.pop(POPULATION_SIZE)
    best_generation = (gene, sorted_results[0])
    generation.append(best_generation)
    print "Mutation>"
    print sorted_results
    return best_generation, generation, sorted_results



def fittest_algorithm():
    return


if __name__ == "__main__":
    best_solu = 0
    generation = []
    initpop = init_population()
    b_g, generation, popu = random_algorithm(0, initpop)
    for i in range(0, 100):
        b_g, generation, sorted_results = random_algorithm(i+1, popu)
        popu = sorted_results
        _, best_ind = b_g
        _, _, _, goal = best_ind
        if goal == TARGET:
            print "Found the best solution> {0}".format(b_g)
            break
