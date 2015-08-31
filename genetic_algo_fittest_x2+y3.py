#!/usr/bin/python
import random
import math

POPULATION_X = 100
POPULATION_SIZE = 10
POPULATION_COUNT = 0


def init_population():
    phenotype = []
    global POPULATION_COUNT
    for i in range(0, POPULATION_SIZE):
        POPULATION_COUNT = POPULATION_COUNT + 1
        new_individual = (i, POPULATION_COUNT, \
                          random.randint(-POPULATION_X, POPULATION_X),
                          random.randint(-POPULATION_X, POPULATION_X), 0)
        phenotype.append(new_individual)
    return phenotype


def quality_function(x1, x2):
    return x1**2 + x2**3


def get_key(item):
    return item[4]


def fittest_algorithm(gene, pheno):
    results = []
    print "Fittest Algorithm: Generation>{0}".format(gene)
    print pheno
    _delta = round(random.uniform(-1, 1), 1)
    for index, id_num, p_x1, p_x2, _ in pheno:
        qual_result = quality_function(p_x1, p_x2)
        evaluation = (index, id_num, p_x1, p_x2, qual_result)
        results.append(evaluation)
    sorted_results = sorted(results, key=get_key)
    index_eval, id_num_eval, _ind_2_change_x1, _ind_2_change_x2, qual = sorted_results[-1]
    _new_ind_x1 = _ind_2_change_x1 + _delta
    _new_ind_x2 = _ind_2_change_x2 + _delta
    sorted_results[-1] = (index_eval, id_num_eval, _new_ind_x1, _new_ind_x2,
                         qual)
    best_generation = (gene, sorted_results[-1])
    print "Fittest Algorithm: Best Individual >{0}".format(sorted_results[-1])
    print sorted_results
    return best_generation, sorted_results


if __name__ == "__main__":
    best_solu = 0
    generation = []
    initpop = init_population()
    b_g, popu = fittest_algorithm(0, initpop)
    print "Found the best solution> {0}".format(b_g)
    for i in range(0, 200):
        b_g, sorted_results = fittest_algorithm(i+1, popu)
        popu = sorted_results
        generation.append(b_g)
        print "Found the best solution> {0}".format(b_g)
