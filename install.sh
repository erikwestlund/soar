#!/usr/bin/env bash

# Get user's JHED
read -p "This will update your container. Do you wish to proceed? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
read -p "Enter your JHED: " JHED_USERNAME

# Install packages required
sudo yum -y install \
            libsecret libsodium-devel openssl-devel bzip2-devel libffi-devel epel zsh nano \
            openssl11-devel dbus-devel sqlite-devel krb5-server krb5-libs krb5-workstation

# Setup MsSql Tools
curl https://packages.microsoft.com/config/rhel/8/prod.repo -o /tmp/msprod.repo
cat /tmp/msprod.repo | sudo tee -a /etc/yum.repos.d/msprod.repo > /dev/null
rm /tmp/msprod.repo

sudo yum -y remove mssql-tools unixODBC-utf16-devel
export ACCEPT_EULA='y'
sudo yum -y install mssql-tools unixODBC-devel

echo export PATH="/opt/mssql-tools/bin:$PATH" >> ~/.bash_profile
echo export PATH="/opt/mssql-tools/bin:$PATH" >> ~/.zshrc
echo export PATH="/opt/mssql-tools/bin:$PATH" >> ~/.bashrc

# Install Python 3.10
mkdir -p /home/idies/workspace/python310
cd /home/idies/workspace/python310
wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz
tar -xzf Python-3.10.2.tgz
cd Python-3.10.2
sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' configure
sudo ./configure --enable-optimizations
sudo make altinstall
python3.10 -V

# Put Python3/Pip into the path and symlink
echo export PATH="/usr/local/bin/python3.10:$PATH" >> ~/.bash_profile
echo export PATH="/usr/local/bin/python3.10:$PATH" >> ~/.zshrc
echo export PATH="/usr/local/bin/python3.10:$PATH" >> ~/.bashrc
echo export PATH="/usr/local/bin/pip3.10:$PATH" >> ~/.bash_profile
echo export PATH="/usr/local/bin/pip3.10:$PATH" >> ~/.zshrc
echo export PATH="/usr/local/bin/pip3.10:$PATH" >> ~/.bashrc

sudo ln -fs /usr/local/bin/python3.10 /usr/bin/python3
sudo ln -fs /usr/local/bin/pip3.10 /usr/bin/pip3
/usr/local/bin/python3.10 -m pip install --upgrade pip

# Install dependencies needed by Soar
pip3 install keyring click pyyaml black rpy2 sh jinja2
R -e "install.packages('keyring')"

# Install Soar
STORAGE_DIR="/home/idies/workspace/Storage/$JHED_USERNAME/persistent"
mkdir -p $STORAGE_DIR
rm -rf "$STORAGE_DIR/soar"
git clone https://github.com/erikwestlund/soar.git "$STORAGE_DIR/soar"

# Add aliases that work regardless of user configuration
echo "alias soar=\"python3 $STORAGE_DIR/soar/soar.py\"" >> ~/.bash_profile
echo "alias soar=\"python3 $STORAGE_DIR/soar/soar.py\"" >> ~/.zshrc
echo "alias soar=\"python3 $STORAGE_DIR/soar/soar.py\"" >> ~/.bashrc
echo "alias crunchr=\"python3 $STORAGE_DIR/soar/soar.py\"" >> ~/.bash_profile
echo "alias crunchr=\"python3 $STORAGE_DIR/soar/soar.py\"" >> ~/.zshrc
echo "alias crunchr=\"python3 $STORAGE_DIR/soar/soar.py\"" >> ~/.bashrc

# Update soar command
echo "alias updatesoar=\"cd $STORAGE_DIR/soar && git reset --hard HEAD && git pull && soar configure\"" >> ~/.bash_profile
echo "alias updatesoar=\"cd $STORAGE_DIR/soar && git reset --hard HEAD && git pull && soar configure\"" >> ~/.zshrc
echo "alias updatesoar=\"cd $STORAGE_DIR/soar && git reset --hard HEAD && git pull && soar configure\"" >> ~/.bashrc

# Add .soarrc
cp $STORAGE_DIR/soar/resources/shell/.soarrc ~/.soarrc

# Store the jhed username in a temporary file to load it on first run
echo $JHED_USERNAME > $STORAGE_DIR/soar/.jhed_username

echo "Installation complete."
echo "Type \"crunchr configure\" to use Soar."
