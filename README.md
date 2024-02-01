# 🦅 Soar: A CLI Helper for the Johns Hopkins University Crunchr Platform

This package is a CLI helper for the Johns Hopkins University Crunchr platform. It is designed to automate tasks that would otherwise be tedious, such as:

* Mounting network volumes.
* Preparing containers with the necessary software and dependencies, such as Java runtimes, database drivers, and R/Python packages.
* Managing credentials in a secure vault that can be easily accessed from R/Python.
* Storing known-working database drivers and other dependencies.
* Generating config files for analysis notebooks, including database connection strings.
* Enhancing the shell environment to be more productive.
* Configuring RStudio settings on new container instances.

## Installation

Install the tool by running this command from an RStudio terminal in a Crunchr container:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/erikwestlund/soar/master/install.sh)" && source ~/.bashrc
```

## Usage

All commands must be run from a Terminal window in RStudio.

Upon a successful installation, type `soar configure` to configure your container. You will be asked to enter a keyring password, which will be used to encrypt your credentials. You will also be asked to enter your JHED username and password.

After configuration, you can use the `soar` command to access the various options available.

To view sub-options for the list commends, type `soar <sub-option>`. For example, type `soar install` to see the various different installation options.

You can type `crunchr` instead of `soar` to access the same commands.

## Features

### Mounting Network Volumes

The `soar mount` commands allow you to mount network volumes. This is useful for accessing your JHU network drives from your container, as well as other SAFE volumes.

* `soar mount home` mounts your home directory to `/homes/idies/workspace/home`.
* `soar mount project` mounts a SAFE project directory to `/homes/idies/workspace/project`, where `project` is the name of the project.

### Installing Software

The `soar install` commands allow you to install software and dependencies.

* `soar install r-data-science` installs useful R packages, such as the Tidyverse suite and numerous database connection utilities.
* `soar install r-ohdsi` installs useful OHDSI-related packages, such as rJava.

### Enhancing Your Container

The `soar enhance` commands allow you to enhance your container environment.

* `soar enhance shell` install the Zsh shell, tells RStudio to use it, and installs Oh My Zsh for a better shell experience. This command also installs the alias helpers described below.
* `soar enhance rstudio-keybindings` configures RStudio keybindings to be more like popular text editors, such as VSCode and Sublime Text. For example, `Ctrl+D` will allow for selecting multiple instances of a word with multiple cursors.
* `soar enhance aliases` installs useful aliases for the shell, such as git convenience commands like `ac` for `git commit -am` and `s` for `git status`.

### Managing Credentials

The `soar credential` commands allow you to manage your credentials. It does so by creating a secure keyring that is encrypted with a password you provide.

You can store your JHED password in the keyring, as well as any other credentials you need to access databases and other services, such as Github Personal Access Tokens.

To access your credentials from R, use the `keyring` package.

Should you forget or mis-type your keyring password, you can reset it by typing `soar keyring-reset`.

### Generating Config and Other Templates

The `soar make` commands allow you to generate config files and other templates.

This command will also copy necessary drivers and other dependencies to the appropriate locations.

Upon running `soar make`, you will be asked to enter the necessary information to generate the config file.

The program will return directions on how to incorporate the generated config files into your analysis notebooks and scripts.


## Package Information

This package is currently under development.

Soar is written in Python.

Author: [Erik Westlund](https://publichealth.jhu.edu/faculty/4677/erik-westlund)
