# Functions related to git

from dot_mechanism import call_command
from os import getcwd, chdir


def git_clone(source_url, dest_dir):
    "Calls git clone on source url and puts it in the destination directory. \
    Url and path should be checked before calling this function. Path should \
    be absolute. Returns the stdout and stderr."
    stdout, stderr = call_command('git clone {0} {1}'.format(source_url, dest_dir))
    return stdout, stderr


def git_commit(dest_dir, message=''):
    "Changes current dir to destination dir, calls `git add .` then `git ci` \
    or `git ci -m 'message'`, then changes back to the original dir."
    curr_dir = getcwd()
    chdir(dest_dir)
    out, _ = call_command('git add .')
    if message == '':
        out, _ = call_command("git ci -m 'Backup from command line'")
    else:
        out, _ = call_command("git ci -m {0}".format(message))
