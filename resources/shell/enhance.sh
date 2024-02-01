#!/usr/bin/env bash
read -p "This will update this container's default system shell to Zsh. Do you wish to proceed? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

sudo chsh -s /bin/zsh root
sudo chsh -s /bin/zsh idies
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh > /dev/null 2>&1
cat ~/.oh-my-zsh/templates/zshrc.zsh-template >> ~/.zshrc
