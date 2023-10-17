# NetApp ONTAP Automation Examples



## Automation Grouping & Timing

1. Cluster Configuration
2. Data Storage Virtual Machine(SVM) Configuration
3. NAS Provisioning - Standard NFS Exports & SMB Shares

```shell
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-1*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-2*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-3*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-revert-00*
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