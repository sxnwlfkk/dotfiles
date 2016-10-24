#! /usr/bin/env python

from os import chdir, getcwd
from os.path import exists as path_exists
from shutil import rmtree

import pytest
from src.dotfiles.dot_mechanism import (call_command, check_slashes,
                                        expand_user, generate_target_filenames,
                                        strip_unneeded)
from src.dotfiles.git_funcitons import git_clone, git_commit

TEST_DIR = expand_user('~/mysrc/dotfiles/src/tests')


def test_strip_unneeded_1():
    print('In test_strip_unneeded')
    assert strip_unneeded('~/Valami') == \
            'Valami'



def test_strip_unneeded_2():
    print('In test_strip_unneeded')
    assert strip_unneeded('/Valami') == \
            'Valami'


def test_check_slashes():
    print('In test_check_slashes')
    assert check_slashes('/user//dir/') == \
            '/user/dir/'


def test_generate_target_filenames():
    print('In test_generate_target_filenames')
    assert generate_target_filenames('/', '/', 'valami', 'public') == \
            ('/valami', '/valami')


def test_git_clone_fn():
    print('Testing git clone auxiliary function.')
    _, stderr = git_clone('https://github.com/sxnwlfkk/configs.git', TEST_DIR+'/test_git_clone')
    assert path_exists(TEST_DIR+'/test_git_clone/home') == True
    if len(stderr) == 0:
        print("No problems here.")
    else:
        print("Stderr is: " + stderr)
    rmtree(TEST_DIR+'/test_git_clone')

def test_git_commit_fn():
    "Very expensive test, lots of communication with github servers, and user \
    interaction needed."
    print('Testing git commit auxiliary function.')

    local_test_dir_1 = TEST_DIR+'/test_git_commit'
    local_test_dir_2 = local_test_dir_1 + '2'

    # Cloning with the previously tested git_clone()
    stdout, stderr = git_clone('https://github.com/sxnwlfkk/configs.git', local_test_dir_1)

    # Setting up the folder and the to be committed new file
    curr_dir = getcwd()
    chdir(local_test_dir_1)
    stdout, stderr = call_command('touch test1.txt')
    chdir(curr_dir)

    # Testing the commit function
    git_commit(local_test_dir_1, 'test commit')
    git_clone('https://github.com/sxnwlfkk/configs.git', local_test_dir_2)

    assert path_exists(local_test_dir_2+'/test1.txt')

    # Removing test file from repository
    chdir(local_test_dir_1)
    call_command('rm test1.txt')
    chdir(curr_dir)
    git_commit(local_test_dir_1, 'test commit')

    # Removing test folders
    rmtree(local_test_dir_1)
    rmtree(local_test_dir_2)
