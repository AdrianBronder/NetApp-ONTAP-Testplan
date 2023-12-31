#!/usr/bin/env bash

################################################################################
#
# Title:        init_LD00821.sh
# Author:       Adrian Bronder
# Initial Date: 2023-08-16
# Description:  Prepare linux host "centos1" in LoD lab LD00821
#               --> "Early Adopter Lab for ONTAP 9.13.1"
#
# URLs:         https://labondemand.netapp.com/node/497
#               https://docs.netapp.com/us-en/ontap/index.html
#               https://galaxy.ansible.com/netapp/ontap
#
################################################################################

echo ""
echo ""
echo "--> Setting variables & paths"
source ~/.bashrc
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

echo ""
echo ""
echo "--> Updating Centos system"
sudo yum -y update

echo ""
echo ""
echo "--> Remove Python3"
sudo yum remove -y python3
sudo rm -f /usr/bin/python3
sudo rm -f /usr/bin/pip3
sudo rm -rf /usr/local/lib
rm -rf ~/.local/*

echo ""
echo ""
echo "--> Installing additional packages"
sudo yum install -y wget gcc libffi-devel epel-release zlib-devel jq libxml2 git krb5-devel sshpass ncurses-devel nvme-cli --skip-broken
sudo yum erase -y openssl

echo ""
echo ""
echo "--> Install OpenSSL"
sudo mkdir $DOWNLOADPATH
sudo wget -P $DOWNLOADPATH https://www.openssl.org/source/openssl-$OPENSSLVERS.tar.gz
sudo tar xfo $DOWNLOADPATH/openssl-$OPENSSLVERS.tar.gz -C $DOWNLOADPATH
cd $DOWNLOADPATH/openssl-$OPENSSLVERS
echo "Configuring OpenSSL..."
sudo ./config --prefix=$OPENSSLPATH --openssldir=$OPENSSLPATH > /dev/null
sudo make > /dev/null
echo "Installing OpenSSL..."
sudo make install > /dev/null
sudo echo "$OPENSSLPATH/lib" > /etc/ld.so.conf.d/openssl.conf
sudo ldconfig
rm $DOWNLOADPATH/openssl-$OPENSSLVERS.tar.gz
echo "export PATH=$PATH:$OPENSSLPATH/bin" >> ~/.bashrc
source ~/.bashrc
cd $SCRIPTPATH

echo ""
echo ""
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
rm $DOWNLOADPATH/Python-$PYTHON3VERS.tgz
echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
source ~/.bashrc
cd $SCRIPTPATH

echo ""
echo ""
echo "--> Upgrading pip"
sudo pip3 install --upgrade pip

echo ""
echo ""
echo "--> Installing additional Python libs"
sudo pip3 install --upgrade requests six netapp_lib selinux
sudo pip3 install --upgrade "pywinrm[kerberos]>=0.3.0"

echo ""
echo ""
echo "--> Installing Asnible"
pip3 install ansible-core==$ANSIBLEVERS

echo ""
echo ""
echo "--> Installing additional ansible collections"
ansible-galaxy collection install -r $SCRIPTPATH/requirements.yml --ignore-certs

echo ""
echo ""
echo "--> Adding centos1 to known hosts and setting up SSH keys"
mkdir ~/.ssh
ssh-keyscan -t ecdsa centos1 centos1.demo.netapp.com 192.168.0.61 >> ~/.ssh/known_hosts
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

echo ""
echo ""
echo "--> Creating default multi-path config on centos"
sudo touch /etc/multipath.conf

echo ""
echo ""
echo "--> Creating Users and groups in AD (dc1)"
ansible-playbook -i $SCRIPTPATH/../inventories/labondemand $SCRIPTPATH/init_helper/init_ad.yml --vault-password-file $SCRIPTPATH/init_helper/vaultfile.txt

echo ""
echo ""
echo "--> Prepare storage clusters in LoD (cluster1 & cluster2)"
ansible-playbook -i $SCRIPTPATH/../inventories/labondemand $SCRIPTPATH/../playbooks/ONTAP-00/ONTAP-revert-00.yml --vault-password-file $SCRIPTPATH/init_helper/vaultfile.txt

echo ""
echo ""
echo "--> Install new Linux kernel, change kernel default, add NVMe_TCP module to load after reboot and reboot"
sudo rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
sudo yum -y install https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm
sudo yum -y --enablerepo=elrepo-kernel install kernel-lt
sudo sed -i 's/GRUB_DEFAULT=saved/GRUB_DEFAULT=0/g' /etc/default/grub
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo echo "nvme_tcp" > /etc/modules-load.d/nvme_tcp.conf
sudo reboot