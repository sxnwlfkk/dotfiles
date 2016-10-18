#! /usr/bin/env python

import os
import subprocess
import shlex
import yaml


# Loading and reading dotfiles

def read_dotfile(path, def_dotpath, log):
    "Decides if there is a custom dotfile or use default."
    if path:
        log.debug(path)
        return load_dotfile(path, def_dotpath, log)

    dot_path = check_slashes(os.path.expanduser('~') + '/' + def_dotpath)
    log.debug(dot_path)
    return load_dotfile(dot_path, def_dotpath, log)


def load_dotfile(path, def_dotpath, log):
    "Loads given dotfile, with `with`."
    try:
        with open(path, 'r') as ymlfile:
            return yaml.load(ymlfile)
    except Exception as e:
        log.error("No dotfiles specified, or ~/{0} not present".format(def_dotpath))
        log.debug(e)

# Calling commands


def call_command(command):
    """Executes a shell command through the subprocess module. Returns
    a tuple (stdout, stderr)."""
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=False,)
    return process.communicate()


# Symlinking
#
def setup_links(backup_folders, repositories, private, log):
    "Invokes the make_private_symlinks function and if there are public files \
    in the config file, invokes the make_public_copies function."
    log.info("Making private symlinks")
    make_private_symlinks(backup_folders, repositories, log)
    log.info('Private value: ' + private)
    if private != 'true':
        log.info("Making public hard copies")
        make_public_copies(backup_folders, repositories, log)


def make_private_symlinks(backup_folders, repositories, log):
    "Reads the config and makes symlinks of all entries. Uses functions to \
    ensure folder availability."

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
                make_symlink(from_file, to_file, log)
                log.info('{0} is symlinked to {1}'.format(dotfile, to_file))

# TODO Seems like I don't use this anymore. Remove?
def strip_unneeded(filename):
    if filename[0] == '~':
        filename = filename[1:]
    if filename[0] == '/':
        return filename[1:]


def generate_target_filenames(from_dir, to_dir, dotfile, status):
    "Checks if the filename is a string or a list (as when file has two names,\
    one in backup repository, one in the target directory, for example \
    ranger.conf if backup, and rc.conf when in ~/.config/ranger/rc.conf). \
    If string, it concatenates to the to and from directories the dotfile's \
    name. If 'private' passed in as status (meaning it symlinks to working \
    dir), makes 'from_file' from_dir + the list's firt item, 'to_file' to_dir \
    + the list's second item, if 'public' passed, it'll have the original \
    backup name in the public repository."
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
