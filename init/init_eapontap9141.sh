#!/usr/bin/env bash

################################################################################
#
# Title:        init_eapontap9141.sh
# Author:       NetApp Inc. (badrian)
# Initial Date: 2024-01-23
# Description:  Prepare linux host "rhel1" in LoD lab 724
#               --> "Early Adopter Lab for ONTAP 9.14.1"
#
# URLs:         https://labondemand.netapp.com/node/724
#               https://docs.netapp.com/us-en/ontap/index.html
#               https://galaxy.ansible.com/netapp/ontap
#
################################################################################

echo ""
echo ""
echo "--> Setting variables & paths"
source ~/.bashrc
#OPENSSLVERS="1.1.1u" #"1.1.1u"
#PYTHON3VERS="3.9.18"
ANSIBLEVERS="2.15.2"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECTPATH=${SCRIPTPATH%/*}
#DOWNLOADPATH="/tmp/downloads"
#OPENSSLPATH="/usr/local/openssl"
#echo "OpenSSL version to be installed: $OPENSSLVERS"
#echo "Python3 version to be installed: $PYTHON3VERS"
echo "Ansible version to be installed: $ANSIBLEVERS"
echo "Path to this script:             $SCRIPTPATH"
echo "Path to this project:            $PROJECTPATH"
#echo "Download path:        $DOWNLOADPATH"
#echo "OpenSSL path:         $OPENSSLPATH" 

echo ""
echo ""
echo "--> Updating RHEL system"
dnf -y update

echo ""
echo ""
echo "--> Installing additional packages"
dnf install -y perl openssl-devel bzip2-devel zlib-devel sqlite-devel python3.11-kerberos krb5-workstation krb5-devel python3.11-pip python3.11-devel nfs-utils java-21-openjdk --skip-broken

echo ""
echo ""
echo "--> Setting alternative Python to 3.11 as default"
alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
update-alternatives --set python3 /usr/bin/python3.11

echo ""
echo ""
echo "--> Setting alternative JAVA to 21 as default"
alternatives --install /usr/bin/java java /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.412.b08-2.el8.x86_64/jre/bin/java 1
alternatives --install /usr/bin/java java /usr/lib/jvm/java-21-openjdk-21.0.3.0.9-1.el8.x86_64/bin/java 2
update-alternatives --set java /usr/lib/jvm/java-21-openjdk-21.0.3.0.9-1.el8.x86_64/bin/java

echo ""
echo ""
echo "--> Upgrading pip"
python3 -m pip install --upgrade pip

echo ""
echo ""
echo "--> Installing additional Python packages"
python3 -m pip install --upgrade requests six netapp_lib selinux flask Flask-LDAP3-Login jmespath pyyaml netapp_ontap
python3 -m pip install --upgrade "pywinrm[kerberos]>=0.3.0"

echo ""
echo ""
echo "--> Installing Asnible"
python3 -m pip install ansible-core==$ANSIBLEVERS ansible-rulebook ansible_runner

echo ""
echo ""
echo "--> Installing additional ansible collections"
ansible-galaxy collection install -r $SCRIPTPATH/requirements.yml --ignore-certs

echo ""
echo ""
echo "--> Adding rhel1 to known hosts and setting up SSH keys"
mkdir ~/.ssh
ssh-keyscan -t ecdsa rhel1 rhel1.demo.netapp.com 192.168.0.61 >> ~/.ssh/known_hosts
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

echo ""
echo ""
echo "--> Enable multipath on linux host"
modprobe -v dm-multipath
mpathconf --enable --user_friendly_names n
systemctl restart multipathd.service

echo ""
echo ""
echo "--> Enable NVMe/TCP on linux host"
modprobe nvme_tcp

echo ""
echo ""
echo "--> Copying default ansible config"
cp $PROJECTPATH/ansible.cfg ~/ansible.cfg

echo ""
echo ""
echo "--> Run web-server for advanced demos as system service"
cat << EOF >> /etc/systemd/system/netapp-self-service.service
[Unit]
Description=Demo Self-Service Portal
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$PROJECTPATH/playbooks/ONTAP-81/web_service/
ExecStart=python3 $PROJECTPATH/playbooks/ONTAP-81/web_service/http_server.py

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable netapp-self-service
systemctl start netapp-self-service

echo ""
echo ""
echo "--> Creating Users and groups in AD (dc1)"
ansible-playbook -i $SCRIPTPATH/../inventories/labondemand_9141 $SCRIPTPATH/init_helper/init_ad.yml

echo ""
echo ""
echo "--> Prepare storage clusters in LoD (cluster1 & cluster2)"
ansible-playbook -i $SCRIPTPATH/../inventories/labondemand_9141 $SCRIPTPATH/../playbooks/ONTAP-00/ONTAP-revert-00.yml
