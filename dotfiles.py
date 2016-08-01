

import argparse
import subprocess
import shlex
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
    make_symlinks(cnf['backup-folders'], cnf['repositories'], args)


#############
# Functions #
#############


# Argparsing


# TODO Might be prudent, if neccessary to make separate argparser for the CLI
# and the run-command file
def def_args():
    parser = argparse.ArgumentParser(description=DESCRIPT)
    parser.add_argument('-d', '--dotfile',
                        help='Define alternative dotfile for this run')
    parser.add_argument('--private', '-p', action='store_true',
                        default=False,
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
        if key == 'private' and (value == "True" or value != "False" and value != ''):
            arg_str += '--' + key
# TODO

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


# Symlinking
#
def make_symlinks(backup_folders, repositories, args):
    #make_private_symlinks(backup_folders, repositories)
    print(args.private)
    if args.private != True:
        print('megy')
        make_public_symlinks(backup_folders, repositories)


def make_private_symlinks(backup_folders, repositories):

    for foldername, folder in backup_folders.items():

        from_dir = check_dir(repositories['private']['dir'] + '/' + foldername
                            + '/')
        # Debug
        #print("The state of from_dir: ", from_dir)

        if 'target' not in backup_folders[foldername]:
            backup_folders[foldername]['target'] = '~/'

        # Debug
        #print("The state of backup_folders[foldername]['target']: ",
        #      backup_folders[foldername]['target'])

        to_dir = ensure_dir(backup_folders[foldername]['target'])

        # Debug
        #print("The state of to_dir: ", to_dir)

        for status, st_dir in folder.items():
            if status == 'target':
                continue
            for dotfile in st_dir:
                from_file, to_file = generate_target_filenames(from_dir, to_dir, dotfile)
                make_symlink(from_file, to_file)
                # print('{0} is symlinked to {1}'.format(dotfile, to_file))


def make_public_symlinks(backup_folders, repositories):

    for foldername, folder in backup_folders.items():
        from_dir = check_dir(repositories['private']['dir'] + '/' + foldername 
                             + '/')
        print(from_dir)
        target_public = repositories['public']['dir']
        if 'target' in backup_folders[foldername]:
            target_public += strip_unneeded(backup_folders[foldername]['target'])
        print(target_public)


def strip_unneeded(filename):
    if filename[0] == '~':
        filename = filename[1:]
    if filename[0] == '/':
        return filename[1:]


def generate_target_filenames(from_dir, to_dir, dotfile):
    try:
        assert isinstance(dotfile, str)
        from_file = from_dir + '/' + dotfile
        to_file = to_dir + '/' + dotfile
        return from_file, to_file

    except AssertionError:
        if len(dotfile) == 2:
            from_file = from_dir + '/' + dotfile[0]
            to_file = ensure_dir(dotfile[1]) + '/' + os.path.basename(dotfile[1])
            return from_file, to_file


def make_symlink(from_file, to_file):
    call_command('ln -sf {0} {1}'.format(from_file, to_file))

def expand_user(path):
    if path[0] == '~':
        path = os.path.expanduser('~') + path[1:]
    return path


def check_dir(path):
    path = expand_user(path)
    path = os.path.dirname(path)
    if os.path.exists(path):
        return path
    raise NameError("No such path exists: {0} Check config and try again.".format(path))


def ensure_dir(path):
    try:
        value = check_dir(path)
        return value
    except NameError:
        path = expand_user(path)
        os.makedirs(path)
        return path


def call_command(command):
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=False,)
    return process.communicate()


if __name__ == '__main__':
    main()























