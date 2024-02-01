#!/usr/bin/env bash
read -p "This will update this container's default system shell to Zsh. Do you wish to proceed? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

sudo yum -y install zsh
chsh -s /bin/zsh root
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
/bin/cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
source ~/.zshrc
