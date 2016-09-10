#! /usr/bin/env python

from src.dotfiles.dot_mechanism import (
    strip_unneeded,
    check_slashes,
    generate_target_filenames,
)

import pytest

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
