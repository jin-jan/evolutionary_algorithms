#!/usr/bin/env python

import sys
import os
import subprocess
import re
from lib.logger import LOG
import xml.etree.ElementTree as ElementTree
from optparse import OptionParser, OptionGroup


class OptsError(Exception):
    pass


class ExtraParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog


def read_algorithm_config(config_file, setup_algo):
    """Read config file and return a list of values"""
    LOG.info("Reading config file ...")
    config_data = ()
    with open(config_file, "r") as f:
        data = f.read()
    out_re = data.replace("\r", "").replace(" ", "")
    out_ind = out_re.split('\n')
    if setup_algo:
        config_data = (out_ind[0].split(':')[1], out_ind[1].split(':')[1],
                       out_ind[2].split(':')[1], out_ind[3].split(':')[1],
                       out_ind[4].split(':')[1], out_ind[5].split(':')[1])
    else:
        config_data = (out_ind[0].split(':')[1], out_ind[1].split(':')[1],
                       out_ind[2].split(':')[1], out_ind[3].split(':')[1],
                       out_ind[4].split(':')[1], out_ind[5].split(':')[1],
                       out_ind[6].split(':')[1])
    # config_data (Population_Size, Population_Range, Parent_Selection,
    #              Reproduction, Competition, Termination)
    LOG.info("{0}".format(config_data))
    return config_data


if __name__ == '__main__':
    parser = OptionParser()

    parser = ExtraParser(epilog=
"""
***GA default configuration file parameters***
    Population_Size:        50,
    Population_Range:       30,
    Parent_Selection:       Age,
    Reproduction:           Mutation,
    Competition:            10,
    Termination:            100,
***ES default configuration file parameters***
    Population_Size:        50
    Population_Range:       30
    Parent_Selection:
    Reproduction:           Mutation
    Competition:
    Termination:
    Adaptive_Mutation_Step: True
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
            setup_algo = True
            config_data = read_algorithm_config(opts.ga_conf, setup_algo)

        if opts.es_conf:
            setup_algo = False
            config_data = read_algorithm_config(opts.es_conf, setup_algo)

    except OptsError as e:
        parser.print_help()
        sys.stderr.write("\nError: %s\n" % str(e))
        sys.exit(-1)

    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.exit(-1)