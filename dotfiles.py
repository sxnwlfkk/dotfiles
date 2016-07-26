#!/bin/python

import argparse
import subprocess
import os
import yaml

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


descript = """
Makes symlinks to working directories and public git directories as specified 
in ~/.dotfile.
"""

def main():

    home_dir = os.path.expanduser('~')

    args = parse_them_args()
    cnf = read_dotfile(args.dotfile)

    for section in cnf:
        print(section)
        print(cnf[section])


def read_dotfile(path):
    if path == None:
        dot_path = home_dir + '/.dotfile'
        return load_dotfile(dot_path)

    return load_dotfile(path)


def load_dotfile(path):
    with open(path, 'r') as ymlfile:
        return yaml.load(ymlfile)


def parse_them_args():
    "Parses the provided args with argparse."

    parser = argparse.ArgumentParser(description=descript)
    parser.add_argument('-d', '--dotfile',
                        help='Define alternative dotfile for this run')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()























