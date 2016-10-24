# TODO

* Write work-modes from user point of view

* Setup mode
  Standard calling command with public repositories
  `dotfiles --setup --public`
  Calling command with user specified dotfile
  `dotfiles --setup -d /home/user/dir/to/.dotfile --public`

  * Needs working ~/.dotfile or a command line argument specifying one
  * Makes symlinks to working files
  * If there is a public repo
    * Clone it to the destination directory specified in .dotfile
    * Copy from private repo to public one the public files. Commit and push them. Dry run
  * Finish  

* Backup mode
  Calling command backup only private repo
  `dotfile --backup`
  Calling command backup with public repo
  `dotfile --backup --public`
  `dotfile -bp`
  * Commits everything in private repo, and pushes it to origin
  * If public repo is present and specified to back up, copy public files to public repo
  * Commit everything in public repo, and push it to origin

* Standard user workflow
  * Installs dotfiles.py with pip install
  * OR clones from github and runs setup.py
  * Downloads private repo from a git server
  * Copies his/her .dotfile to ~/.dotfile
  * Runs `dotfiles --setup` or `dotfiles --setup --public` or `dotfiles -sp`
  * Uses normally her files, when she makes a change calls backup
    `dotfiles --backup` or `dotfiles --backup --public` or `dotfiles -bp`

* Write arg to clone public repo
* Write script to make public dir
* Write script to clone public repo
* Write script/fuction to copy public files to public repo
  and git add. ci etc
* Finalize the program
* Test it thoroughly
* Write setup.py
* Write wrapper scripts
* Write documentation
