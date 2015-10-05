#!/usr/bin/env python

import sys
import os
import subprocess
import re
import ast
import shutil
from lib.logger import LOG
from lib.evolutionary_strategy import search_es
from lib.genetic_algorithm import search_ga
from lib.plot_graph import plot_data
import xml.etree.ElementTree as ElementTree
from optparse import OptionParser, OptionGroup

LOG_NAME = 'assign3.log'


class OptsError(Exception):
    pass


class ExtraParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog


def read_algorithm_config(config_file):
    """Read config file and return a list of values"""
    LOG.info("Reading config file ...")
    config_data = ()
    with open(config_file, "r") as f:
        data = f.read()
    out_re = data.replace("\r", "").replace(" ", "")
    out_ind = out_re.split('\n')
    config_data = (out_ind[0].split(':')[1], out_ind[1].split(':')[1],
                   out_ind[2].split(':')[1], out_ind[3].split(':')[1])
    # config_data (Population_Range, Termination, Adaptive_Mutation_Step,
    #              Survivor_Selection)
    LOG.info("{0}".format(config_data))
    return config_data


if __name__ == '__main__':
    parser = OptionParser()

    parser = ExtraParser(epilog=
"""
***GA default configuration file parameters***
    Population_Size:        30,
    Termination:            10000,
    Adaptive_Mutation_Step: False
    Survivor_Selection:     False
***ES default configuration file parameters***
    Population_Range:       30,
    Termination:            15000,
    Adaptive_Mutation_Step: True
    Survivor_Selection:     False
""")

    parser.add_option("-g", "--ga-conf", dest="ga_conf",
                      action="store", help="Configuration file of the" \
                      "genetic algorithm")

    parser.add_option("-e", "--es-conf", dest="es_conf", action="store",
                      help="Configuration file of the evolutionary strategy")

    opts = parser.parse_args()[0]

    try:
        if len(sys.argv) < 2:
            raise OptsError("Missing arguments")

        if opts.ga_conf:
            algorithm_name = 'GA behavior'
            LOG.info("Starting GA")
            pop_size, term, ad_mut_stp, mu_lambda = read_algorithm_config(opts.ga_conf)
            search_ga(int(term), int(pop_size), ast.literal_eval(ad_mut_stp),
                      ast.literal_eval((mu_lambda)))
            plot_data(algorithm_name, LOG_NAME)
            LOG.info("Finish GA")

        if opts.es_conf:
            algorithm_name = 'ES behavior'
            LOG.info("Starting ES")
            pop_range, term, ad_mut_stp, mu_lambda = read_algorithm_config(opts.es_conf)
            search_es(int(term), int(pop_range), ast.literal_eval(ad_mut_stp),
                      ast.literal_eval((mu_lambda)))
            plot_data(algorithm_name, LOG_NAME)
            LOG.info("Finish ES")


    except OptsError as e:
        parser.print_help()
        sys.stderr.write("\nError: %s\n" % str(e))
        sys.exit(-1)

    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.exit(-1)