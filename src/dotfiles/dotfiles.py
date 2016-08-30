#! /usr/bin/env python

import argparse
import logging
import os
import subprocess
import shlex
from dot_mechanism import setup_links, check_slashes, read_dotfile


# Constants

DEF_DOTFILE = '.dotfile'

# Description and misc docstrings:

DESCRIPT = """
Makes symlinks to working directories and public git directories as specified
in ~/.dotfile.
"""


###########
# Logging #
###########

def logr(args):
    try:
        import coloredlogs
    except Error:
        pass

    if args.verbose == None:
        coloredlogs.install(level='ERROR')
    elif args.verbose == 1:
        coloredlogs.install(level='INFO')
    elif args.verbose >= 2:
        coloredlogs.install(level='DEBUG')

    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger('dotfiles')
    log_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'dotfiles.log'
    fh = logging.FileHandler(log_path)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    log.addHandler(fh)
    return log


################################
# Argument and dotfile parsing #
################################

# Argparsing


def def_args():
    parser = argparse.ArgumentParser(description=DESCRIPT)
    parser.add_argument('-d', '--dotfile',
                        help='Define alternative dotfile for this run')
    parser.add_argument('-s', '--setup', action='store_true', default=False)
    parser.add_argument('--private', '-p', choices=['true', 'false'], default='true',
                        help="If True, then doesn't make public folders and symlinks. Defaults to True.")
    parser.add_argument('--verbose', '-v', action='count',
                        help='Increase output verbosity.')
    return parser


def parse_cl_args():
    parser = def_args()
    args = parser.parse_args()
    return args


########
# Main #
########

def main():

    args = parse_cl_args()
    log = logr(args)
    log.debug(args.dotfile)
    cnf = read_dotfile(args.dotfile, DEF_DOTFILE, log)
    # If there is a public repo, pull it to the public dir
    # if args.private == False:
    #     github_sync()
    if args.setup == True:
        setup_links(cnf['backup-folders'], cnf['repositories'], args.private, log)
    else:
        log.info('Not running setup.')
        log.debug(args.setup)
    # If there is a public repo, sync it with the symlinks in it




if __name__ == '__main__':
    main()
