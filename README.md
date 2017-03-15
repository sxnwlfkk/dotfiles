# dotfiles
A dotfiles syncer and symlinker, written in python, with Git syncing support.

## Master Not Yet Stable Or Finished

## Main features

* Read from config file (~/.dotfiles)
 * Specify another dotfile to use (one use)
* Distinguish between public and private repos
* Make symlinks for usage and for public repo

## Git syncer

* Make a separate git syncer (maybe with inotify reminder)
* Separate syncing action for private and public repos
* Action to set up public repo (pull from github, then symlink with force from private dir

## Contents of config file (~/.dotfiles):

* Private repo url
* Public repo url
* Absolute path to private repository dir
* All sections have two parts a general, and a private
* Section for main config files (.zshrc, .vimrc, oh-my-zsh.sh, etc.)
