# Introduction
This repository contains playbooks and vars used for automating execution of PoC tests.
- Main artificats (aside of this README) are located in the subfolder "playbooks".
- Additional ressoruces used for internal development lab environment setup can be reviewed in "init".

# Pre-requisits & Assumptions
Following assumptions have been made for executing playbooks successfully:
- "playbooks/vars/vars_labondemand.yml" and "playbooks/inventory/hosts_poclab" are reviewed and adjusted/completed to lab specific values.
- Ansible host is set up wiht latest collection of "netapp.ontap" from Ansible Galaxy (currently: 22.7.0).
- Ansible host is configured with minimum versions provided by customer:
  - Python 3.7.5 (recommended: 3.8+)
  - Ansible 2.10.3 (recommended: 2.12+)
- Playbooks contain plays for Linux hosts to mount/unmount NFS exports. Proper SSH key and known hosts setup on Ansible host is required to connect to test Linux machines. It is also possible providing SSH password by using "--ask-pass" parameter when executing playbooks.
- If executing mount/umount operations on Linux hosts is not desired, Linux Plays have to be removed from the playbooks.
- DNS records exist for the cluster as well as for every SVM and test host within the test environment.

# Playbooks General
- A dedicated playbook exists for every automated test case documented in customer PoC test plan, e.g. "BSS-02-01.yml"
- Test plan instructions are executed as tasks
- Almost every playbook contains built-in verification by displaying storage array configuration prior to executing test plan instructions (pre_tasks) and after executing test plan instructinos (post_tasks)
- There is a revert playbook for every test frame documented in the PoC test plan, e.g. revert_BSS-02. These playbooks can be executed to get the system to the known state prior to executing the test steps.

# Execution Examples
- Executing a test step (BSS-00-01 - initial preparation & configuration):
  ```
  ansible-playbook -i ./playbooks/inventory/hosts_poclab ./playbooks/BSS-00-01.yml
  ```
- Executing a test step containing instructions for Linux (BSS-03-06 - create and mount a volume):
  ```
  ansible-playbook -i ./playbooks/inventory/hosts_poclab ./playbooks/BSS-03-06.yml --ask-pass
  ```
- Executing a revert playbook to get all tests in section 3 (BSS-03-*) reverted:
  ```
  ansible-playbook -i ./playbooks/inventory/hosts_poclab ./playbooks/BSS-*.yml --ask-pass
  ```
- Executing all tests steps of the test plan in a single command
  ```
  ansible-playbook -i ./playbooks/inventory/hosts_poclab ./playbooks/BSS-*.yml --ask-pass
  ```
- Revert all test steps of the test plan in a single command
  ```
  ansible-playbook -i ./playbooks/inventory/hosts_poclab ./playbooks/revert_BSS-10.yml ./playbooks/revert_BSS-08.yml ./playbooks/revert_BSS-07.yml ./playbooks/revert_BSS-06.yml ./playbooks/revert_BSS-03.yml ./playbooks/revert_BSS-02.yml ./playbooks/revert_BSS-00.yml --ask-pass
  ```

# Additional Info
- Initial cluster setup (Day0/1) is a wide area with a lot of possible customization. This repository covers only a small portion showcasing some automation capabilities. Further tasks can be added easily, when knowing more detailed requirements and customer's desired standard install procedure.
- Automated attaching of storage devices (volumes/shares/exports) to hosts is out of scope for this PoC.
  - However, Linux tasks have been implemented for speeding up testing.
  - Same could be applied with shares and Windows hosts (community.windows). Additional development and testing of these tasks could not be completed in time.

# References
- Public documentation of NetApp Modules
  - https://docs.ansible.com/ansible/latest/collections/netapp/ontap/
- NetApp ONTAP Modules on Ansible Galaxy
  - https://galaxy.ansible.com/netapp/ontap
- Public GitHub for NetApp ONTAP Modules
  - https://github.com/ansible-collections/netapp.ontap

# For NetApp Internal use: Quick Start with Lab on Demand
1. Please use the virtual hands-on lab (log in with your NetApp support account):
   - https://labondemand.netapp.com/node/497
2. Log into the Ansible Linux host ("centos1.demo.netapp.com") and clone this repository:
   ```
   git clone https://github.com/CXO-Automation/Roche_PDT_Test_NetApp.git
   ```
3. Initialize the environment by running the lab init script:
   ```
   ./Roche_PDT_Test_NetApp/init/init_LD00821.sh
   ```
4. Go to the playbook folder and start executing test steps, e.g. general test playbook "NTAP-00-00.yml"
   ```
   cd ./Roche_PDT_Test_NetApp
   ansible-playbook -i ./playbooks/inventory/hosts_devlab ./playbooks/NTAP-00-00.yml -e "@playbooks/vars/vars_devlab.yml"
   ```

# Changelog
## v1.0
Initial Release