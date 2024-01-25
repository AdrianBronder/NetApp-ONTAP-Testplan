#!/usr/bin/env bash

################################################################################
#
# Title:        init_eapontap9131.sh
# Author:       Adrian Bronder
# Initial Date: 2023-08-16
# Description:  Prepare linux host "centos1" in LoD lab 497
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
PYTHON3VERS="3.9.18"
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
yum -y update

echo ""
echo ""
echo "--> Installing additional packages"
yum install -y wget gcc libffi-devel epel-release zlib-devel python3-devel jq libxml2 git krb5-devel krb5-workstation sshpass ncurses-devel nvme-cli --skip-broken
yum erase -y openssl

echo ""
echo ""
echo "--> Install OpenSSL"
mkdir $DOWNLOADPATH
wget -P $DOWNLOADPATH https://www.openssl.org/source/openssl-$OPENSSLVERS.tar.gz
tar xfo $DOWNLOADPATH/openssl-$OPENSSLVERS.tar.gz -C $DOWNLOADPATH
cd $DOWNLOADPATH/openssl-$OPENSSLVERS
echo "Configuring OpenSSL..."
./config --prefix=$OPENSSLPATH --openssldir=$OPENSSLPATH > /dev/null
make > /dev/null
echo "Installing OpenSSL..."
make install > /dev/null
echo "$OPENSSLPATH/lib" > /etc/ld.so.conf.d/openssl.conf
ldconfig
rm $DOWNLOADPATH/openssl-$OPENSSLVERS.tar.gz
echo "export PATH=$PATH:$OPENSSLPATH/bin" >> ~/.bashrc
source ~/.bashrc
cd $SCRIPTPATH

echo ""
echo ""
echo "--> Install Python3"
mkdir $DOWNLOADPATH
wget -P $DOWNLOADPATH https://www.python.org/ftp/python/$PYTHON3VERS/Python-$PYTHON3VERS.tgz
tar xfo $DOWNLOADPATH/Python-$PYTHON3VERS.tgz -C $DOWNLOADPATH
cd $DOWNLOADPATH/Python-$PYTHON3VERS
echo "Configuring Python3..."
./configure --enable-optimizations --with-openssl="$OPENSSLPATH" > /dev/null
echo "Installing Python3..."
make altinstall > /dev/null
ln -s /usr/local/bin/python3.9 /usr/bin/python3.9
rm $DOWNLOADPATH/Python-$PYTHON3VERS.tgz
echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
source ~/.bashrc
cd $SCRIPTPATH

echo ""
echo ""
echo "--> Setting alternative Python to 3.9 as default"
update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
update-alternatives --set python3 /usr/local/bin/python3.9

echo ""
echo ""
echo "--> Upgrading pip"
python3 -m pip install --upgrade pip

echo ""
echo ""
echo "--> Installing additional Python libs"
python3 -m pip install --upgrade requests six netapp_lib selinux
python3 -m pip install --upgrade "pywinrm[kerberos]>=0.3.0"

echo ""
echo ""
echo "--> Installing Asnible"
python3 -m pip install ansible-core==$ANSIBLEVERS

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
echo "--> Creating default multi-path config on linux host"
mpathconf --enable

echo ""
echo ""
echo "--> Creating Users and groups in AD (dc1)"
ansible-playbook -i $SCRIPTPATH/../inventories/labondemand_9131 $SCRIPTPATH/init_helper/init_ad.yml --vault-password-file $SCRIPTPATH/init_helper/vaultfile.txt

echo ""
echo ""
echo "--> Prepare storage clusters in LoD (cluster1 & cluster2)"
ansible-playbook -i $SCRIPTPATH/../inventories/labondemand_9131 $SCRIPTPATH/../playbooks/ONTAP-00/ONTAP-revert-00.yml --vault-password-file $SCRIPTPATH/init_helper/vaultfile.txt

echo ""
echo ""
echo "--> Install new Linux kernel, change kernel default, add NVMe_TCP module to load after reboot and reboot"
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
yum -y install https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm
yum -y --enablerepo=elrepo-kernel install kernel-lt
sed -i 's/GRUB_DEFAULT=saved/GRUB_DEFAULT=0/g' /etc/default/grub
grub2-mkconfig -o /boot/grub2/grub.cfg
echo "nvme_tcp" > /etc/modules-load.d/nvme_tcp.conf
reboot