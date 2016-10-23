#! /usr/bin/env python

from os.path import exists as path_exists
from shutil import rmtree

import pytest
from src.dotfiles.dot_mechanism import (check_slashes, expand_user,
                                        generate_target_filenames,
                                        strip_unneeded)
from src.dotfiles.git_funcitons import git_clone

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
