# Contents
1. [Introduction](#Introduction)
2. [Quick Start with Lab on Demand](#Quick-Start-with-Lab-on-Demand)
3. [Further Execution Examples](#Further-Execution-Examples)
4. [Instructions for Changing the Environment](#Instructions-for-Changing-the-Environment)
5. [Additional References](#Additional-References)
6. [Changelog](#Changelog)


# Introduction
This repository contains Ansible artifacts (inventories, vars, playbooks...) for executing tests and demos against ONTAP automatically.
They can be used out of the box in Lab on Demand or - by adjusting varaibles - in any other environment.


# Quick Start with Lab on Demand
For NetApp internal and partner use - ready to go in less than 15 minutes
1. Please use one the early adopter virtual hands-on lab (log in with your NetApp support account):
   - https://labondemand.netapp.com/lab/eapontap9131 (ONTAP 9.13.1)
   - https://labondemand.netapp.com/lab/eapontap9141 (ONTAP 9.14.1)
2. Log into the Linux host ("centos1.demo.netapp.com") and clone this repository:
   ```
   yum install -y git
   git clone https://github.com/AdrianBronder/NetApp-ONTAP-Testplan.git
   
   ```
3. Initialize the environment by running the lab init script:
   Caution: The script might end with a reboot of the Linux system. Simply reconnect to execute further steps.
   ```
   cd ./NetApp-ONTAP-Testplan
   # based on ONTAP (lab) version: ./init/init_eapontap<ontapversion>.sh
   # e.g.
   ./init/init_eapontap9141.sh
   
   ```
4. Execute test steps, e.g. general connection test playbook "ONTAP-01-04.yml"
   ```
   # based on ONTAP (lab) version: ./inventories/labondemand_<ontapversion>
   # e.g.
   ansible-playbook -i ./inventories/labondemand_9141 ./playbooks/ONTAP-01/ONTAP-01-04.yml
   
   ```


# Further Execution Examples
(keep in mind: based on ONTAP (lab) version: ./inventories/labondemand_<ontapversion>)
- Execute a single test step (e.g. ONTAP-02-02 - Physical Network):
  ```
  ansible-playbook -i ./inventories/labondemand_9141 ./playbooks/ONTAP-10/ONTAP-10-02.yml
  ```
- Execute an entire test frame (e.g. ONTAP-10 - Basic Cluster Configuration)
  ```
  ansible-playbook -i ./inventories/labondemand_9141 ./playbooks/ONTAP-10/ONTAP-10-*.yml
  ```
- Revert configuration changed and objects created during a test frame:
  ```
  ansible-playbook -i ./inventories/labondemand_9141 ./playbooks/ONTAP-31/ONTAP-revert-31.yml
  ```
- Execute ALL tests with a single command (and track the execution time)
  ```
  time ansible-playbook -i ./inventories/labondemand_9141 ./playbooks/ONTAP-[1-9]*/ONTAP-[0-9]*.yml
  ```
- Revert all test steps of the test plan (back to initial state)
  ```
  ansible-playbook -i ./inventories/labondemand_9141 ./playbooks/ONTAP-00/{ONTAP-revert-00_linux,ONTAP-revert-00_windows,ONTAP-revert-00}.yml
  ```


# Dealing with Credentials
Although only LoD and test specific credentials are used in the existing inventory and variable files, all of them are encrypted with the default Lab on Demand admin/root password. For ease of use, it is stored in a password file and referenced in the ansible configuration file (<project_root>/ansible.cfg). If you want to view or encrypt new files according to your environment, here some examples:
- View content of an encrypted file:
  ```
  # ansible-vault view vault.yml
  Vault password:
  # Ansible Variables
  
  # Custom Variables
  vault_ontap_admin_user:           "admin"
  vault_ontap_admin_password:       <hidden>
  ...
  ```
- Encrypt file in place:
  ```
  # ansible-vault encrypt vault.yml
  New Vault password:
  Confirm New Vault password:
  Encryption successful
  ```
Ansibe Vault documentation:
https://docs.ansible.com/ansible/2.8/user_guide/vault.html


# Instructions for Changing the Environment
The playbooks can be executed in any other non-production environments for demos and testing.
* Ansible host is configured with minimum recommended versions (as of now - August 2023):
  - Python 3.8+
  - Ansible 2.12+
* Variables are defined at various levels. There are generally two categories of variables for this test:
  * **Environment**, or: Desired state of a system or a group of systems
    * Inventory folder id created for new environment in ./inventories (as per exmple "labondemand")
    * hosts file and variables have to match specific environment
    * a sinlge file can be used as well, but is not recommended with a large amount of variables and secrets like passwords
  * **Runtime**, or: Configuration, that is created or changed as part of the test plan
    * Variable folder is created for new environment in ./vars (as per example "labondemand")
    * it can be a single file, but is not recommended with a large amount of variables and secrets like passwords


# Additional References
- Public documentation of NetApp Modules
  - https://docs.ansible.com/ansible/latest/collections/netapp/ontap/
- NetApp ONTAP Modules on Ansible Galaxy
  - https://galaxy.ansible.com/netapp/ontap
- Public GitHub for NetApp ONTAP Modules
  - https://github.com/ansible-collections/netapp.ontap


# Changelog
## v1.2
- Adding ONTAP-xx - ???
- Adding support for ONTAP 9.14.1 lab
- General Clean-up (comments, format...)

## v1.1
- Adding ONTAP-42 - Quality of Service
- Adding ONTAP-51 - Local Versioning (Snapshots)
- Adding ONTAP-52 - Backup (SnapMirror)
- Adding "prepare" playbooks to run all pre-requesits for a particular test frame
- Moving RO policy creation for NFS to “ONTAP-20 – Basic SVM Setup”

## v1.0
- Initial Release