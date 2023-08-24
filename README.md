# Contents
1. [Introduction](#Introduction)
2. [Quick Start with Lab on Demand](#Quick-Start-with-Lab-on-Demand)
3. [Further Execution Examples](#Further-Execution-Examples)
4. [Instructions for Changing the Environment](#Instructions-for-Changing-the-Environment)
5. [Additional References](#Additional-References)
6. [Changelog](#Changelog)


# Introduction
This repository contains Ansible artifacts (inventories, vars, playbooks...) for executing test and demos against ONTAP automatically.
They can be used out of the box in Lab on Demand or tuned to any other environment


# Quick Start with Lab on Demand
For NetApp internal and partner use - ready to go in less than 15 minutes
1. Please use the virtual hands-on lab (log in with your NetApp support account):
   - https://labondemand.netapp.com/node/497
2. Log into the Linux host ("centos1.demo.netapp.com") and clone this repository:
   ```
   git clone https://github.com/AdrianBronder/NetApp-ONTAP-Testplan.git
   ```
3. Initialize the environment by running the lab init script:
   ```
   cd ./NetApp-ONTAP-Testplan
   ./init/init_LD00821.sh
   ```
4. Execute test steps, e.g. general test playbook "ONTAP-00-00.yml"
   ```
   ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-00-00.yml
   ```


# Further Execution Examples
- Execute a single test step (e.g. ONTAP-02-02 - Network):
  ```
  ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-02-02.yml
  ```
- Executing an entire test frame (e.g. ONTAP-02 - Basic Cluster Configuration)
  ```
  ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-02-*.yml
  ```
- Revert configuration changed and objects created during a test frame:
  ```
  ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-revert-21.yml
  ```
- Executing ALL tests with a single command (and track the execution time)
  ```
  time ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-[0-9]*.yml
  ```
- Revert all test steps of the test plan (back to initial state)
  ```
  ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-revert-00_linux.yml
  ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-revert-00_windows.yml
  ansible-playbook -i ./inventories/labondemand ./playbooks/ONTAP-revert-00.yml
  ```


# Instructions for Changing the Environment
The playbooks can be executed in any other non-production environments for demos and testing.
* Ansible host is configured with minimum recommended versions (as of now - August 2023):
  - Python 3.8+
  - Ansible 2.12+
* Inventory folder id created for new environment in ./inventories (as per exmple "labondemand")
  - hosts file and variables have to match specific environment
  - a sinlge file can be used as well, but is not recommended with a large amount of variables and secrets like passwords
* Variable folder is created for new environment in ./vars (as per example "labondemand")
  - it can be a single file, but is not recommended with a large amount of variables and secrets like passwords


# Additional References
- Public documentation of NetApp Modules
  - https://docs.ansible.com/ansible/latest/collections/netapp/ontap/
- NetApp ONTAP Modules on Ansible Galaxy
  - https://galaxy.ansible.com/netapp/ontap
- Public GitHub for NetApp ONTAP Modules
  - https://github.com/ansible-collections/netapp.ontap


# Changelog
## v1.0
Initial Release