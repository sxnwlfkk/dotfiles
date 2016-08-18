

import argparse
import logging
import os
import subprocess
import shlex
import yaml


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

########
# Main #
########

def main():

    args = parse_cl_args()
    log = logr(args)
    log.debug(args.dotfile)
    cnf = read_dotfile(args.dotfile)
    args = parse_dot_args(args, cnf['settings'])
    # If there is a public repo, pull it to the public dir
    # if args.private == False:
    #     github_sync()
    make_symlinks(cnf['backup-folders'], cnf['repositories'], args, log)
    # If there is a public repo, sync it with the symlinks in it


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
    parser.add_argument('--private', '-p', choices=['true', 'false'], default='true',
                        help="If True, then doesn't make public folders and symlinks. Defaults to True.")
    parser.add_argument('--verbose', '-v', action='count',
                        help='Increase output verbosity.')
    return parser


def parse_cl_args():
    parser = def_args()
    args = parser.parse_args()
    return args


def parse_dot_args(old_args, settings):
    if settings == None:
        return old_args
    else:
        parser = def_args()
        read_args = build_args_str(settings).split()
        new_args = parser.parse_args(args=read_args, namespace=old_args)
        return new_args


def build_args_str(settings_dict):
    arg_str = ''
    for key, value in settings_dict.items():
        arg_str += '--' + key + ' ' +  str(value) + ' '

    return arg_str


# Loading and reading dotfiles
#
def read_dotfile(path):
    "Decides if there is a custom dotfile or use default."
    if path:
        return load_dotfile(path)

    dot_path = check_slashes(os.path.expanduser('~') + '/' + DEF_DOTFILE)
    return load_dotfile(dot_path)


def load_dotfile(path):
    "Loads given dotfile, with `with`."
    try:
        with open(path, 'r') as ymlfile:
            return yaml.load(ymlfile)
    except:
        log.error("No dotfiles specified, or ~/{0} not present".format(DEF_DOTFILE))


# Symlinking
#
def make_symlinks(backup_folders, repositories, args, log):
    log.info("Making private symlinks")
    make_private_symlinks(backup_folders, repositories, log)
    log.info('Private value: ' + args.private)
    if args.private != 'true':
        log.info("Making public symlinks")
        make_public_symlinks(backup_folders, repositories, log)


def make_private_symlinks(backup_folders, repositories, log):

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


def make_public_symlinks(backup_folders, repositories, log):

    for foldername, folder in backup_folders.items():
        from_dir = check_dir(repositories['private']['dir']) + '/' + foldername + '/'

        target_public = check_slashes(repositories['public']['dir'] + '/' + foldername)

        for status, st_dir in folder.items():
            if status == 'target' or status == 'private':
                continue
            for dotfile in st_dir:
                from_file, to_file = generate_target_filenames(from_dir, target_public, dotfile, 'public')
                ensure_dir(to_file)
                make_symlink(from_file, to_file)
                log.info('{0} is symlinked to {1}'.format(dotfile, to_file))


def strip_unneeded(filename):
    if filename[0] == '~':
        filename = filename[1:]
    if filename[0] == '/':
        return filename[1:]


def generate_target_filenames(from_dir, to_dir, dotfile, status):
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
    for i in range(len(filename)):
        if i+1 < len(filename):
            if filename[i] == '/' and filename[i+1] == '/':
                filename = filename[:i] + filename[i+1:]
                check_slashes(filename)

    return filename


def make_symlink(from_file, to_file, log):
    command = 'ln -sf {0} {1}'.format(from_file, to_file)
    log.debug('Command called: ' + command)
    call_command(command)

def expand_user(path):
    if path[0] == '~':
        path = os.path.expanduser('~') + path[1:]
    return path


def check_dir(path):
    path = expand_user(path)
    path = os.path.dirname(path)
    if os.path.exists(path):
        return path
    try:
        raise NameError("No such path exists: {0} Check config and try again.".format(path))
    except NameError as err:
        log.exception('No such file: ', path)


def ensure_dir(path):
    try:
        value = check_dir(path)
        return value
    except NameError:
        path = expand_user(path)
        path = os.path.dirname(path)
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























