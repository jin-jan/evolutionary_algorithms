#!/usr/bin/python
import random

POPULATION_X = 100
POPULATION_SIZE = 10
POPULATION_COUNT = 0


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
    return (x**3)


def get_key(item):
    return item[3]


def fittest_algorithm(gene, pheno):
    results = []
    generation = []
    print "Fittest Algorithm: Generation>{0}".format(gene)
    _delta = round(random.uniform(-1, 1), 1)
    for index, id_num, p, _ in pheno:
        qual_result = quality_function(p)
        evaluation = (index, id_num, p, qual_result)
        results.append(evaluation)
    print results
    sorted_results = sorted(results, key=get_key)
    index_eval, id_num_eval, _ind_2_change, qual = sorted_results[-1]
    _new_ind = _ind_2_change + _delta
    sorted_results[-1] = (index_eval, id_num_eval, _new_ind, qual)
    best_generation = (gene, sorted_results[-1])
    generation.append(best_generation)
    print sorted_results
    return best_generation, generation, sorted_results


if __name__ == "__main__":
    best_solu = 0
    generation = []
    initpop = init_population()
    b_g, generation, popu = fittest_algorithm(0, initpop)
    for i in range(0, 200):
        b_g, generation, sorted_results = fittest_algorithm(i+1, popu)
        popu = sorted_results
        print "Found the best solution> {0}".format(b_g)
