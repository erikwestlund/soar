# Install packages required
sudo yum -y install libsecret libsodium openssl-devel bzip2-devel libffi-devel epel openssl11-devel dbus-devel sqlite-devel

# Setup MsSql Tools
sudo su
curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/msprod.repo
exit

sudo yum -y remove mssql-tools unixODBC-utf16-devel
export ACCEPT_EULA='y'
sudo yum -y install mssql-tools unixODBC-devel

echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.zshrc
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

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
source ~/.bashrc

sudo ln -fs /usr/local/bin/python3.10 /usr/bin/python3
sudo ln -fs /usr/local/bin/pip3.10 /usr/bin/pip3
/usr/local/bin/python3.10 -m pip install --upgrade pip

# Install dependencies needed by Soar
pip3 install keyring click pyyaml black rpy2