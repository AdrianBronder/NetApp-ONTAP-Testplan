# NetApp ONTAP Automation Examples

This *branch* adds NFS Flexclone fprovisioning automation. The script will run through all NFS Flexclone tasks *ONTAP-41*

This automation:
1. Creates a volume
2. Mounts on client & writes some data
3. Snapshots and clones the volume, mounting & writing more data
4. The final step creates 9 more clones for illustration purposes
5. The *ONTAP-revert-41.yml* removes all the client and ONTAP config created by the *ONTAP-41* tasks

## Automation Grouping & Timing

1. Cluster Configuration
2. Data Storage Virtual Machine(SVM) Configuration
3. NFS Flexclone Provisioning - Flexclone NFS Exports

```shell
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-1*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-2*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-41-*
# Run manualy / seperately to see the config on the client
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-revert-41.yml
```

File size defaults to 500MB
`time ansible-playbook -i inventory/labondemand playbooks/ONTAP-41-04.yml -e "filesize=1GB"`
`time ansible-playbook -i inventory/labondemand playbooks/ONTAP-41-07.yml -e "filesize=1GB"`

```shell
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ time ansible-playbook -i inventories/labondemand playbooks/ONTAP-41-06.yml 

TASK [Create test file on NFS export] **********************************************************************************************************************************************************************************************************************************************
changed: [centos1]

real    0m5.139s
user    0m1.635s
sys     0m0.257s

root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ time ansible-playbook -i inventories/labondemand playbooks/ONTAP-41-06.yml -e "filesize=1TB"

TASK [Create test file on NFS export] **********************************************************************************************************************************************************************************************************************************************
^C [ERROR]: User interrupted execution

real    73m9.386s
user    4m32.497s
sys     0m39.492s
```

## Observations

### Timing Examples

Cluster  CFG  

real    2m2.652s
user    0m46.661s
sys     0m7.922s

SVM CFG  

real    0m41.924s
user    0m15.781s
sys     0m2.943s

NAS CFG & Client Mount  

real    2m57.534s
user    0m53.982s
sys     0m12.166s

Revert ALL  

real    2m29.567s
user    0m44.212s
sys     0m8.709s

## Timing for Initial Lab Configuration

This installs and/or updates:
* Ansible
* Python

**Initial Lab Configuration**

`~/init/init_LD00821.sh`

```shell
real    11m20.105s
user    5m47.239s
sys     1m25.138s
```

## Timing for running batches of test cases

Ensure ONTAP clusters are reachable and responding.

**Initial Connectivity Test and Version**

```shell
real    0m2.156s
user    0m2.021s
sys     0m0.389s
```

These next several task batches configure the cluster and the SVM.  
That gets the envionrment ready to present resources to clients.  

**Cluster Configuration**

*Basic*
```shell
real    1m33.155s
user    0m20.262s
sys     0m3.238s
```

*Advanced*
```shell
real    0m31.240s
user    0m17.447s
sys     0m3.167s
```

*Administrative Authentication*
```shell
real    0m44.061s
user    0m15.535s
sys     0m2.384s
```

**SVM (Vserver) Configuration**
```shell
real    0m47.796s
user    0m16.529s
sys     0m2.952s
```

**NFS Storage & Export Configuration**
```shell
real    0m52.979s
user    0m17.514s
sys     0m5.329s
```

**SMB Storage & Share Configuration**
```shell
real    2m6.211s
user    0m37.379s
sys     0m6.984s
```

**Reverts**  
31
```shell
real    0m35.957s
user    0m8.358s
sys     0m2.436s
```

32
```shell
real    1m11.672s
user    0m14.255s
sys     0m2.189s
```

revert-00*
```shell
real    2m1.052s
user    0m38.970s
sys     0m7.839s
```