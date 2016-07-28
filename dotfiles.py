#!/bin/python

import argparse
import subprocess
import os
import yaml


# Constants

DEF_DOTFILE = '.dotfile'

# Description and misc docstrings:

DESCRIPT = """
Makes symlinks to working directories and public git directories as specified 
in ~/.dotfile.
"""


# Main features
# - Read from config file (~/.dotfiles)
#   - Specify another dotfile to use (one use)
# - Distinguish between public and private repos
# - Make symlinks for usage and for public repo

# Git syncer
# - Make a separate git syncer (maybe with inotify reminder)
# - Separate syncing action for private and public repos
# - Action to set up public repo (pull from github, then symlink with force
#   from private dir

# Contents of config file (~/.dotfiles):
# - Private repo url
# - Public repo url
# - Absolute path to private repository dir
# - All sections have two parts a general, and a private
# - Section for main config files (.zshrc, .vimrc, oh-my-zsh.sh, etc.)


def main():

    args = parse_cl_args()
    cnf = read_dotfile(args.dotfile)
    args = parse_dot_args(args, cnf['settings'])


    print(args)

#############
# Functions #
#############


# Argparsing
#

# TODO Might be prudent, if neccessary to make separate argparser for the CLI
# and the run-command file
def def_args():
    parser = argparse.ArgumentParser(description=DESCRIPT)
    parser.add_argument('-d', '--dotfile',
                        help='Define alternative dotfile for this run')
    parser.add_argument('--private', '-P', action='store_true',
                        help="Don't make public folder")
    return parser


def parse_cl_args():
    parser = def_args()
    args = parser.parse_args()
    return args


def parse_dot_args(old_args, settings):
    if settings == None:
        pass
    else:
        parser = def_args()
        read_args = build_args_str(settings)
        new_args = parser.parse_args(args=[read_args], namespace=old_args)
        return new_args


def build_args_str(settings_dict):
    arg_str = ''
    for key, value in settings_dict.items():
        if value == "True" or value != "False" and value != '':
            arg_str += '--' + key

    return arg_str




# Loading and reading dotfiles
#
def read_dotfile(path):
    "Decides if there is a custom dotfile or use default."
    if path == None:
        dot_path = os.path.expanduser('~') + DEF_DOTFILE
        return load_dotfile(dot_path)

    return load_dotfile(path)


def load_dotfile(path):
    "Loads given dotfile, with `with`."
    try:
        with open(path, 'r') as ymlfile:
            return yaml.load(ymlfile)
    except:
        print("No dotfiles specified, or ~/{0} not present".format(DEF_DOTFILE))



if __name__ == '__main__':
    main()























