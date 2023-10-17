#!/usr/bin/env bash

################################################################################
#
# Title:        automation_demo.sh
# Author:       Ken Hillier
# Initial Date: 2023-10-17
# Description:  Batch run cluster and SVM configuration, with some client tasks
#
# URLs:         https://labondemand.netapp.com/node/497
#               https://github.com/AdrianBronder/NetApp-ONTAP-Testplan
#               https://docs.netapp.com/us-en/ontap/index.html
#               https://galaxy.ansible.com/netapp/ontap
#
################################################################################

echo ""
echo ""
echo "--> Running Ansible Playbooks to demo ONTAP automated configuration:"
echo "--> 1. Cluster Configuration"
echo "--> 2. Data Storage Virtual Machine(SVM) Configuration"
echo "--> 3. NFS Provisioning - Flexclone NFS Exports"
echo "--> 4. Revert / Remove all configuration & Reset environment" 

echo ""
echo ""
echo "--> Cluster Configuration"
cd ~/NetApp-ONTAP-Testplan
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-1*

echo ""
echo ""
echo "--> Data Storage Virtual Machine(SVM) Configuration"
cd ~/NetApp-ONTAP-Testplan
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-2*

echo ""
echo ""
echo "--> NAS Provisioning - Standard NFS Exports & SMB Shares"
cd ~/NetApp-ONTAP-Testplan
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-4*

echo ""
echo ""
echo "--> Revert / Remove all configuration & Reset environment"
cd ~/NetApp-ONTAP-Testplan
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-revert-41.yml

# echo ""
# echo ""
# echo "--> Revert / Remove all configuration & Reset environment"
# cd ~/NetApp-ONTAP-Testplan
# time ansible-playbook -i inventories/labondemand playbooks/ONTAP-revert-00*

echo ""
echo ""
echo "--> Finished!"