#! /usr/bin/env python
# Version 0.2.0

import subprocess
import shlex
import argparse
import logging
import os
from os import chdir, getcwd
import yaml

# Constants

DEF_DOTFILE = '.dotfile'

# Description and misc docstrings:

DESCRIPT = """
Makes symlinks to working directories and public git directories as specified
in ~/.dotfile.
"""


###################
# Command calling #
###################


def call_command(command):
    """Executes a shell command through the subprocess module. Returns
    a tuple (stdout, stderr)."""
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=False,)
    return process.communicate()


#################
# Git functions #
#################


def git_clone(source_url, dest_dir):
    "Calls git clone on source url and puts it in the destination directory. \
    Url and path should be checked before calling this function. Path should \
    be absolute. Returns the stdout and stderr."
    stdout, stderr = call_command(
        'git clone {0} {1}'.format(source_url, dest_dir))
    return stdout, stderr


def git_commit(dest_dir, message='', branch="master"):
    "Changes current dir to destination dir, calls `git add .` then `git ci` \
    or `git ci -m 'message'`, then changes back to the original dir."
    curr_dir = getcwd()
    chdir(dest_dir)
    stdout, stderr = call_command('git status')
    # print(stdout)
    stdout, stderr = call_command('git add .')
    # print("After git add called:\n", stdout, stderr)
    stdout, stderr = call_command('git status')
    # print(stdout)
    if message == '':
        stdout, stderr = call_command(
            'git commit -m "Backup from dotmanager.py"')
    else:
        stdout, stderr = call_command('git commit -m "{0}"'.format(message))

    # print('After commit:\n', stdout, stderr)

    out, _ = call_command('git push origin {0}'.format(branch))
    chdir(curr_dir)


#############
# Mechanism #
#############


# Major functions, called from the main file
def clone_public_repo(config):
    """Check if public directory exists and clone to it the public repo."""
    clone_dir = config['repositories']['public']['dir']
    ensure_dir(clone_dir)

    # Try to clone public repository, if directory has content, git will abort
    git_clone(config['repositories']['public']['url'], clone_dir)


def make_private_symlinks(backup_folders, repositories, log):
    """Reads the config and makes symlinks of all entries. Uses functions to \
    ensure folder availability."""

    for foldername, folder in backup_folders.items():

        from_dir = check_dir(repositories['private']['dir'] + '/' + foldername
                             + '/')

        if 'target' not in backup_folders[foldername]:
            backup_folders[foldername]['target'] = '~/'

        to_dir = ensure_dir(backup_folders[foldername]['target'])

        for status, st_dir in folder.items():
            if status == 'target':
                continue
            for dotfile in st_dir:
                from_file, to_file = generate_target_filenames(from_dir, to_dir, dotfile, 'private')
                make_symlink(from_file, to_file, log)
                log.info('{0} is symlinked to {1}'.format(dotfile, to_file))


def make_public_copies(backup_folders, repositories, log):
    "Makes hard copies of files designated public in the config file to the \
    public repository."

    for foldername, folder in backup_folders.items():
        from_dir = check_dir(repositories['private']['dir']) + '/' + foldername + '/'

        target_public = check_slashes(repositories['public']['dir'] + '/' + foldername)

        for status, st_dir in folder.items():
            if status == 'target' or status == 'private':
                continue
            for dotfile in st_dir:
                from_file, to_file = generate_target_filenames(from_dir, target_public, dotfile, 'public')
                ensure_dir(to_file)
                make_copy(from_file, to_file, log)
                log.info('{0} is copied to {1}'.format(dotfile, to_file))


# Loading and reading dotmanager

def read_dotfile(path, def_dotpath, log):
    "Decides if there is a custom dotfile or use default."
    if path:
        log.debug(path)
        return load_dotfile(path, def_dotpath, log)

    dot_path = check_slashes(os.path.expanduser('~') + '/' + def_dotpath)
    log.debug(dot_path)
    return load_dotfile(dot_path, def_dotpath, log)


def load_dotfile(path, def_dotpath, log):
    "Tries to load given config file. If it can't, logs the error: no valid \
    path to dotfile specified, or no file in the default directory (~/.dotfile)"
    try:
        with open(path, 'r') as ymlfile:
            return yaml.load(ymlfile)
    except Exception as e:
        log.error("No dotmanager specified, or ~/{0} not present".format(def_dotpath))
        log.debug(e)


def generate_target_filenames(from_dir, to_dir, dotfile, status):
    """Checks if the filename is a string or a list (as when file has two names,\
    one in backup repository, one in the target directory, for example \
    ranger.conf if backup, and rc.conf when in ~/.config/ranger/rc.conf). \
    If string, it concatenates to the `to` and `from` directories the dotfile's \
    name. If 'private' passed in as status (meaning it symlinks to working \
    dir), makes 'from_file' from_dir + the list's first item, 'to_file' to_dir \
    + the list's second item, if 'public' passed, it'll have the original \
    backup name in the public repository."""
    try:
        assert isinstance(dotfile, str)
        from_file = check_slashes(from_dir + '/' + dotfile)
        to_file = check_slashes(to_dir + '/' + dotfile)
        return from_file, to_file

    except AssertionError:
        if status == 'private':
            if len(dotfile) == 2:
                from_file = check_slashes(from_dir + '/' + dotfile[0])
                to_file = ensure_dir(dotfile[1]) + '/' + os.path.basename(dotfile[1])
                return from_file, to_file

        if status == 'public':
            if len(dotfile) == 2:
                from_file = check_slashes(from_dir + '/' + dotfile[0])
                to_file = check_slashes(to_dir + '/' + dotfile[0])
                return from_file, to_file


def check_slashes(filename):
    "Makes sure there are no double slashes in file path."
    for i in range(len(filename)):
        if i+1 < len(filename):
            if filename[i] == '/' and filename[i+1] == '/':
                filename = filename[:i] + filename[i+1:]
                check_slashes(filename)

    return filename


def make_symlink(from_file, to_file, log):
    "Call symlink shell command."
    command = 'ln -sf {0} {1}'.format(from_file, to_file)
    log.debug('Command called: ' + command)
    call_command(command)


def make_copy(from_file, to_file, log):
    "Call cp shell command."
    command = 'cp {0} {1}'.format(from_file, to_file)
    log.debug('Command called: ' + command)
    call_command(command)


def expand_user(path):
    "Expands the ~ to real user path."
    if path[0] == '~':
        path = os.path.expanduser('~') + path[1:]
    return path


def check_dir(path):
    "Raises error if file doesn't exist."
    path = expand_user(path)
    path = os.path.dirname(path)
    if os.path.exists(path):
        return path
    try:
        raise NameError("No such path exists: {0} Check config and try again.".format(path))
    except NameError as err:
        log.exception('No such file: ', path)


def ensure_dir(path):
    "Checks if dir on path exists, else makes it."
    try:
        value = check_dir(path)
        return value
    except NameError:
        path = expand_user(path)
        path = os.path.dirname(path)
        os.makedirs(path)
        return path

###########
# Logging #
###########

def logr(args):
    if args.verbose is None:
        logging.basicConfig(level=logging.ERROR)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbose >= 1:
        logging.basicConfig(level=logging.DEBUG)

    log = logging.getLogger('dotmanager')

    # dir_of_this_file = os.path.dirname(__file__)
    # dir_above_this_file, _ = os.path.split(dir_of_this_file)
    # root_dir, _ = os.path.split(dir_above_this_file)
    #
    # log_path = root_dir + '/logs/dotmanager.log'
    # print(log_path)
    # fh = logging.FileHandler(log_path)
    #
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    #
    # log.addHandler(fh)
    return log


################################
# Argument and dotfile parsing #
################################

# Argparsing
def def_args():
    parser = argparse.ArgumentParser(description=DESCRIPT)
    # Define the configuration file
    parser.add_argument('-d', '--dotfile',
                        help='Define alternative dotfile for this run.')
    # Setup or backup
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--setup", action="store_true", default=False,
                       help="Sets up the dotfile system.")
    group.add_argument("--backup", action="store_true", default=False,
                       help="Does a backup on public and/or private repos.")

    # Public or private
    group_pp = parser.add_mutually_exclusive_group(required=True)
    group_pp.add_argument("--public", action="store_true", default=False,
                          help="Sets or backs up the public repository, on top of the private.")
    group_pp.add_argument("--private", action="store_true", default=False,
                          help="Sets up only the private repository.")
    # Set verbosity
    parser.add_argument('--verbose', '-v', action='count',
                        help='Increase output verbosity.')
    parser.add_argument('--no_git', action='store_true', default=False,
                        help="leaves out any git call from run.")
    return parser


def parse_cl_args():
    parser = def_args()
    args = parser.parse_args()
    return args


###############
# Usage modes #
###############

def setup(args, config, log):
    """Makes symlinks from private repo to working directories for dotmanager. \
    IF public argument set, makes directory for public repo, if not present \
    clones repo, if URL present in ~/.dotmanager, copies the public files to it \
    and commit/pushes it, as if to test."""

    log.info("Setting up dotmanager.")

    # Symlink
    log.info("Making private symlinks.")
    make_private_symlinks(config["backup-folders"], config['repositories'], log)

    # Copy public files if needed
    if args.public and "public" in config["repositories"] \
            and "dir" in config["repositories"]["public"] \
            and config["repositories"]["public"]["dir"] != "":
        if not args.no_git and "url" in config["repositories"]["private"] \
                and config["repositories"]["private"]["url"] != "":
            log.info("Cloning public repo.")
            clone_public_repo(config)
        log.info("Copying public files.")
        make_public_copies(config["backup-folders"], config['repositories'], log)


def backup(args, config, log):
    """Commits every change in private repo, then commits it. IF public is set
    copies public files from private repo, to public dir, then commits and
    pushes."""

    if not args.no_git and "url" in config["repositories"]["private"] \
            and config["repositories"]["private"]["url"] != "":
        log.info("Committing changes in backup directory.")
        git_commit(config["repositories"]["private"]["dir"],
                   "Backup made by dotmanager.")

    if args.public:
        log.info("Copying public files.")
        if "public" in config["repositories"]:
            make_public_copies(config["backup-folders"], config["repositories"], log)
            if not args.no_git and "url" in config["repositories"]["private"] \
                    and config["repositories"]["private"]["url"] != "":
                log.info("Committing changes in public repository.")
                git_commit(config["repositories"]["public"]["dir"],
                           "Backup made by dotmanager.")


########
# Main #
########

def main():
    args = parse_cl_args()
    log = logr(args)
    log.debug(args.dotfile)
    cnf = read_dotfile(args.dotfile, DEF_DOTFILE, log)

    if not args.setup and not args.backup or not args.private and not args.public:
        print("Invalid arguments. You can get help with dotmanager -h.")
    else:
        if args.setup:
            setup(args, cnf, log)
        if args.backup:
            backup(args, cnf, log)

    log.info("All done.")

if __name__ == '__main__':
    main()
