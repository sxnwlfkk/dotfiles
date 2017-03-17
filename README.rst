n++ dotfiles
============

npp\_dotfiles makes it easy to use and manage your configuration files
while keeping them in one secure directory (like Dropbox or other
hosts). You can configure it to symlink your files to their destination
directory with support to different names in backup and working dirs.
More, you can manage the config files, that you want to share with
others separate from your private ones. Uses git to automatically push
and pull repositories on backup.

**Current stable version is 0.2.0**

Install
-------

You can install it with pip:

``pip install npp-dotmanager``

Or download the source and use:

::

    $ git clone https://github.com/sxnwlfkk/dotmanager
    $ cd dotmanager
    $ python3 setup.py install

Run
---

You can run the program with the ``dotmanager`` command. You can explore
the arguments with ``dotmanager -h`` help function.

If you don't have root permission, you can use the
``dotmanager_noroot.py`` script after cloning the repository. In the
root dir of the project call:

``python3 scripts/dotmanager_noroot.py -h``

Configuration
-------------

Dotmanager needs a configuration file to run, and checks first in
``~/.dotfile``. You can specify a config file from another directory
with calling:

``dotmanager -d ~/path/to/alternative/dotfile``

Configuration file
~~~~~~~~~~~~~~~~~~

The configuration file needs to be formatted in YAML, in the following
fashion:

::

    repositories:
        private:
            dir: /home/user/path/to/backup/directory
            url: https://example@bitbucket.org/configs.git
        public:
            dir: /home/user/path/to/public/respitory
            url: https://github.com/example/configs.git

    backup-folders:
        scripts:
            target: ~/bin/
            public:
                - first_script
                - second_script
            private:
                - third_script
        home:
            target: ~/
            public:
                - .vimrc
                - .tmux.conf
                - [.newsbeuterrc, ~/.newsbeuter/config/.newsbeuterrc]
            private:
                - .zshrc
                - .dotfile
                - .netrc
                - [ranger.conf, ~/.config/ranger/rc.conf]

*This example config file is available in the source repositories.*

The ``repositories`` and ``backup-folders`` are mandatory levels.
Repositories needs to have at least a private level, where the ``dir``
needs to be set to the backup folder, and the ``url`` is only needed, if
you want to use the Git functionality.

The keys in the ``backup-folders`` are the name of the directories
inside your backup folder **(at the moment you need at least one, and
it's also a good idea to structure your backup files)**. The ``target``
key determines the working directory, where most of the dotfiles will be
symlinked.

Public and Private modes
~~~~~~~~~~~~~~~~~~~~~~~~

The files under the ``public`` key will be treated the same as the
private ones, -- symlinked to the target directory -- with the exception
that they will be copied additionally to the public directory, if you
specified one.

Storing files with alternative name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to store your config files with different name than it needs
to be in the target directory for whatever reason, you can do that. For
example, you want to store ``ranger``'s config file (``rc.conf``) as
``ranger.conf`` in your backup directory. For this to work, you need to
specify the alternative name first, then the path to the target file:

``- [ranger.conf, ~/.config/ranger/rc.conf]``

Alternate target path
~~~~~~~~~~~~~~~~~~~~~

If your file needs to be in other directory than the rest of your files
in your backup dir, you can specify the alternate path with the above
method.

Setup
-----

Setup is one of the main modes of work if ``dotmanager``. You can call
it with public or private. Setup symlinks in both cases both public and
private files to their destination. However public tries to clone the
public ``git`` repository, if provided. Else, it makes the directory (if
it doesnt exists), and copies the public files to their position.
Optimally you'll need to use this once an install.

Private
~~~~~~~

``dotmanager --setup --private``

Public
~~~~~~

``dotmanager --setup --public``

Backup
------

Backup is the function to call, if you want to migrate your backups to
their git servers. If called with the ``--private`` flag, it just
commits the changes in your backup directory, and pushes it to current
branch. Called with the ``--public`` flag, it commits and pushes the
private directory, then copies the current state of the public files to
the public dir. After that the public repository is also committed and
pushed to the current dir.

Private
~~~~~~~

``dotmanager --backup --private``

Public
~~~~~~

``dotmanager --backup --public``

The ``--no_git`` flag
---------------------

The ``--no_git`` flag inhibits every git functionality of the program,
if you want to use other hosting or version control.

License
-------

::

    Copyright (C) 2017, Saxon Wolfkok <saxonwolfkok@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
