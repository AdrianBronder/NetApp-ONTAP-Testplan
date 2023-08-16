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
sudo mkdir /tmp/download-openssl
sudo wget -P /tmp/download-openssl https://www.openssl.org/source/openssl-1.1.1u.tar.gz
sudo tar xfo /tmp/download-openssl/openssl-1.1.1u.tar.gz -C /opt/
cd /opt/openssl-1.1.1u
sudo ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl
sudo make
sudo make install
sudo echo "/usr/local/openssl/lib" > /etc/ld.so.conf.d/openssl.conf
sudo ldconfig
export PATH=$PATH:/usr/local/openssl/bin
cd $(dirname $0)

echo "--> Install Python3"
sudo mkdir /tmp/download-python
sudo wget -P /tmp/download-python https://www.python.org/ftp/python/3.9.17/Python-3.9.17.tgz
sudo tar xfo /tmp/download-python/Python-3.9.17.tgz -C /opt/
cd /opt/Python-3.9.17
sudo ./configure --enable-optimizations --with-openssl="/usr/local/openssl"
sudo make altinstall
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3.9
sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip3.9
export PATH=$PATH:~/.local/bin
cd $(dirname $0)

echo "--> Upgrading pip"
sudo pip3 install --upgrade pip

echo "--> Installing additional Python libs"
sudo pip3 install --upgrade requests six netapp_lib selinux
sudo pip3 install --upgrade "pywinrm[kerberos]>=0.3.0"

echo "--> Installing Asnible"
pip3 install 'ansible-core==2.15.2'

echo "--> Installing additional ansible collections"
ansible-galaxy collection install -r $(dirname $0)/requirements.yml --ignore-certs

echo "--> Creating Users and groups in AD (dc1)"
ansible-playbook -i $(dirname $0)/init_helper/init_inventory $(dirname $0)/init_helper/init_ad.yml

echo "--> Prepare primary storage system (cluster1)"
ansible-playbook -i $(dirname $0)/init_helper/init_inventory $(dirname $0)/init_helper/init_ontap.yml
