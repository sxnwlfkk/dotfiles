#! /usr/bin/env python

import argparse
import logging
import os
import shlex
import subprocess

from dot_mechanism import check_slashes, read_dotfile, setup_links
from git_funcitons import git_clone

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

    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger('dotfiles')
    log_path = os.path.dirname(
        os.path.realpath(__file__)) + '/' + 'dotfiles.log'
    fh = logging.FileHandler(log_path)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    log.addHandler(fh)
    return log


################################
# Argument and dotfile parsing #
################################

# Argparsing
def def_args():
    parser = argparse.ArgumentParser(description=DESCRIPT)
    # Define the configuration file
    parser.add_argument('-d', '--dotfile',
                        help='Define alternative dotfile for this run')
    # Initial symlinking and copying
    parser.add_argument('-s', '--setup', action='store_true', default=False,
                        help='Set up the symlinks and first copies to public repository, if any.')
    # Set if there should be public repository
    parser.add_argument('--private', '-p', choices=['true', 'false'],
                        default='true',
                        help="If True, then doesn't make public folders and symlinks. Defaults to True.")
    # Set verbosity
    parser.add_argument('--verbose', '-v', action='count',
                        help='Increase output verbosity.')
    return parser


def parse_cl_args():
    parser = def_args()
    args = parser.parse_args()
    return args


###############
# Usage modes #
###############

def setup():
    "Makes symlinks from private repo to working directories for dotfiles. \
    IF public argument set, makes directory for public repo, if not present \
    clones repo, if URL present in ~/.dotfiles, copies the public files to it \
    and commit/pushes it, as if to test."
    pass


def backup():
    "Commits every change in private repo, then commits it. IF public is set \
    copies public files from private repo, to public dir, then commits and \
    pushes."
    pass

########
# Main #
########

def main():

    args = parse_cl_args()
    log = logr(args)
    log.debug(args.dotfile)
    cnf = read_dotfile(args.dotfile, DEF_DOTFILE, log)
    # TODO If there is a public repo and relevant args, pull it to the public
    # dir
    # if args.private == False:
    #     github_sync()
    if args.setup == True:
        setup_links(cnf['backup-folders'],
                    cnf['repositories'], args.private, log)
    else:
        log.info('Not running setup.')
        log.debug(args.setup)
    # TODO If there is a public repo, sync it with the symlinks in it


if __name__ == '__main__':
    main()
