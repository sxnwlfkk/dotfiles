#!/bin/python

import argparse
import subprocess
import os

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

    parser = argparse.ArgumentParser(
        description='Saves or restores dotfiles from dropbox and git.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-s', '--save',
                        action='store_true', default=False,
                        help='Saves the current dotfiles to the backup directory.')

    group.add_argument('-r', '--restore',
                       action='store_true', default=False,
                       help='Restores the dotfiles form the backup directory.')
    load_owndot()


def load_owndot():
    path = os.path.realpath(__file__)[: - len(__file__)] + '.dotfiles'
    if os.path.exists(path):
        owndot = open(path, 'r+')
    else:
        owndot = open(path, 'w+')
    return owndot


def close_owndot(file_obj):
    file_obj.close()


if __name__ == '__main__':
    main()























