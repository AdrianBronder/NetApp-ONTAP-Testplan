#!/usr/bin/env bash

################################################################################
#
# Title:        init_LD00821.sh
# Author:       Adrian Bronder
# Initial Date: 2023-07-25
# Description:  Prepare linux host "centos1" in LoD lab LD00821
#               --> "Early Adopter Lab for ONTAP 9.13.1"
#
# URLs:         https://labondemand.netapp.com/node/497
#               https://docs.netapp.com/us-en/ontap/index.html
#               https://galaxy.ansible.com/netapp/ontap
#
################################################################################

echo "--> Setting variables & paths"
OPENSSLVERS="1.1.1u"
PYTHON3VERS="3.9.17"
ANSIBLEVERS="2.15.2"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DOWNLOADPATH="/tmp/downloads"
OPENSSLPATH="/usr/local/openssl"
echo "OpenSSL version to be installed: $OPENSSLVERS"
echo "Python3 version to be installed: $PYTHON3VERS"
echo "Ansible version to be installed: $ANSIBLEVERS"
echo "Path to this script:  $SCRIPTPATH"
echo "Download path:        $DOWNLOADPATH"
echo "OpenSSL path:         $OPENSSLPATH" 

echo "--> Updating Cetnos system"
sudo yum -y update

echo "--> Remove Python3"
sudo yum remove -y python3
sudo rm -f /usr/bin/python3
sudo rm -f /usr/bin/pip3
sudo rm -rf /usr/local/lib
rm -rf ~/.local/*

echo "--> Installing additional packages"
sudo yum install -y wget gcc libffi-devel epel-release zlib-devel jq libxml2 git krb5-devel sshpass --skip-broken
sudo yum erase -y openssl

echo "--> Install OpenSSL"
sudo mkdir $DOWNLOADPATH
sudo wget -P $DOWNLOADPATH https://www.openssl.org/source/openssl-$OPENSSLVERS.tar.gz
sudo tar xfo $DOWNLOADPATH/openssl-$OPENSSLVERS.tar.gz -C $DOWNLOADPATH
cd $DOWNLOADPATH/openssl-$OPENSSLVERS
echo "Configuring OpenSSL..."
sudo ./config --prefix=$OPENSSLPATH --openssldir=$OPENSSLPATH > /dev/null
sudo make
echo "Installing OpenSSL..."
sudo make install > /dev/null
sudo echo "$OPENSSLPATH/lib" > /etc/ld.so.conf.d/openssl.conf
sudo ldconfig
export PATH=$PATH:$OPENSSLPATH/bin
cd $SCRIPTPATH

echo "--> Install Python3"
sudo mkdir $DOWNLOADPATH
sudo wget -P $DOWNLOADPATH https://www.python.org/ftp/python/$PYTHON3VERS/Python-$PYTHON3VERS.tgz
sudo tar xfo $DOWNLOADPATH/Python-$PYTHON3VERS.tgz -C $DOWNLOADPATH
cd $DOWNLOADPATH/Python-$PYTHON3VERS
echo "Configuring Python3..."
sudo ./configure --enable-optimizations --with-openssl="$OPENSSLPATH" > /dev/null
echo "Installing Python3..."
sudo make altinstall > /dev/null
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3.9
sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip3.9
export PATH=$PATH:~/.local/bin
cd $SCRIPTPATH


echo "--> Upgrading pip"
sudo pip3 install --upgrade pip

echo "--> Installing additional Python libs"
sudo pip3 install --upgrade requests six netapp_lib selinux
sudo pip3 install --upgrade "pywinrm[kerberos]>=0.3.0"

echo "--> Installing Asnible"
pip3 install ansible-core==$ANSIBLEVERS

echo "--> Installing additional ansible collections"
ansible-galaxy collection install -r $SCRIPTPATH/requirements.yml --ignore-certs

echo "--> Creating Users and groups in AD (dc1)"
ansible-playbook -i $SCRIPTPATH/init_helper/init_inventory $SCRIPTPATH/init_helper/init_ad.yml

echo "--> Prepare primary storage system (cluster1)"
ansible-playbook -i $SCRIPTPATH/init_helper/init_inventory $SCRIPTPATH/init_helper/init_ontap.yml
