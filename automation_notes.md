# Demonstration Notes

Lab Configuration

Prompt

[Coderwall - Add git branch name to bash prompt](https://coderwall.com/p/fasnya/add-git-branch-name-to-bash-prompt)

```shell
# GIT Branch Prompt
parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="[\u@\h \[\033[32m\]\w\[\033[33m\]]\$(parse_git_branch)\[\033[00m\] # "  # <-- user is root
```

Other Prompt Ideas:

[Display git branch in bash prompt](https://gist.github.com/justintv/168835)

Example of an image `![A test image](image.png)`

![Prompt Image:](https://user-images.githubusercontent.com/3128048/111437981-5fb53300-870c-11eb-94ea-83f83587546f.png)

```shell
# prompt
FMT_BOLD="\e[1m"
FMT_RESET="\e[0m"
FMT_UNBOLD="\e[21m"
FG_BLACK="\e[30m"
FG_BLUE="\e[34m"
FG_CYAN="\e[36m"
FG_GREEN="\e[32m"
FG_MAGENTA="\e[35m"
FG_RED="\e[31m"
FG_WHITE="\e[97m"
BG_BLUE="\e[44m"
BG_GREEN="\e[42m"
BG_MAGENTA="\e[45m"

export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWCOLORHINTS=1

export PS1=\
"\n\[${BG_GREEN}\] \[${FG_RED}\] \[${FG_BLACK}\]\u \[${FG_GREEN}${BG_BLUE}\] "\
"\[${FG_BLACK}\]\w \[${FMT_RESET}${FG_BLUE}\]"\
'$(__git_ps1 "\[${BG_MAGENTA}\] \[${FG_WHITE}\] %s \[${FMT_RESET}${FG_MAGENTA}\]")'\
"\n \[${FG_GREEN}\]╰ \[${FG_CYAN}\]\$ \[${FMT_RESET}\]"
```

```shell
[root@centos1 NetApp-ONTAP-Testplan]# time ./init/init_LD00821.sh ^C
[root@centos1 NetApp-ONTAP-Testplan]# 
[root@centos1 NetApp-ONTAP-Testplan]# 
[root@centos1 NetApp-ONTAP-Testplan]# vi ~/.bashrc
[root@centos1 NetApp-ONTAP-Testplan]# source !$
source ~/.bashrc
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ vi ~/.bashrc
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ vi ~/.bashrc
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ 
```
Updating **Python** & adding **Ansible**

```shell
[root@centos1 NetApp-ONTAP-Testplan]# time ./init/init_LD00821.sh 

...

PLAY RECAP *****************************************************************************************************************************************************************************************************************************************************************************************************************
cluster1                   : ok=19   changed=7    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0   
cluster2                   : ok=15   changed=3    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0   


real    13m21.519s
user    9m32.267s
sys     2m25.006s
```

Cluster Configuration  

```shell
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ time ansible-playbook -i inventories/labondemand playbooks/ONTAP-1*

PLAY [ONTAP-10-01 - Licenses] *******************************************************************************************************************************************************************************************************************************************************

...

PLAY RECAP **************************************************************************************************************************************************************************************************************************************************************************
cluster1                   : ok=32   changed=25   unreachable=0    failed=0    skipped=6    rescued=2    ignored=1   
cluster2                   : ok=31   changed=24   unreachable=0    failed=0    skipped=7    rescued=2    ignored=1   


real    2m55.844s
user    0m51.838s
sys     0m7.626s
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $
```

Data Storage Virtual Machine (SVM) Configuration

```shell
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ time ansible-playbook -i inventories/labondemand playbooks/ONTAP-2*

PLAY [ONTAP-20-01 - Storage Virtual Machines (SVMs)] ********************************************************************************************************************************************************************************************************************************

...
PLAY RECAP **************************************************************************************************************************************************************************************************************************************************************************
cluster1                   : ok=12   changed=12   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


real    0m50.075s
user    0m14.680s
sys     0m2.112s
```

```shell
root@centos1 ~/NetApp-ONTAP-Testplan (flexclonenfs) $ time ansible-playbook -i inventories/labondemand playbooks/ONTAP-revert-00*

PLAY [ONTAP-revert-00 - Return to Day0 - Linux] *************************************************************************************************************************************************************************************************************************************

...
PLAY RECAP **************************************************************************************************************************************************************************************************************************************************************************
centos1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
cluster1                   : ok=22   changed=12   unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
cluster2                   : ok=22   changed=12   unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
jumphost                   : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


real    2m10.330s
user    0m36.596s
sys     0m6.409s
```
Demo Command Summary
```shell
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-1*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-2*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-4*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-revert-00*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-1*
time ansible-playbook -i inventories/labondemand playbooks/ONTAP-2*
```

## Issues

Check idempotency for FlexClone cleanup

```shell
TASK [Delete all volumes from clusters] *********************************************************************************************************************************************************************************************************************************************
skipping: [cluster2]
failed: [cluster1] (item={'uuid': '4ba4c213-66cc-11ee-81f7-00505685c51b', 'name': 'ontap_41_nfs_vol01', 'is_svm_root': False, 'svm': {'name': 'ntap-svm01-nas', 'uuid': '03003e2f-66cc-11ee-81f7-00505685c51b', '_links': {'self': {'href': '/api/svm/svms/03003e2f-66cc-11ee-81f7-00505685c51b'}}}, '_links': {'self': {'href': '/api/storage/volumes/4ba4c213-66cc-11ee-81f7-00505685c51b'}}}) => {"ansible_loop_var": "item", "changed": false, "item": {"_links": {"self": {"href": "/api/storage/volumes/4ba4c213-66cc-11ee-81f7-00505685c51b"}}, "is_svm_root": false, "name": "ontap_41_nfs_vol01", "svm": {"_links": {"self": {"href": "/api/svm/svms/03003e2f-66cc-11ee-81f7-00505685c51b"}}, "name": "ntap-svm01-nas", "uuid": "03003e2f-66cc-11ee-81f7-00505685c51b"}, "uuid": "4ba4c213-66cc-11ee-81f7-00505685c51b"}, "msg": "Error in rest_delete_volume: calling: storage/volumes/4ba4c213-66cc-11ee-81f7-00505685c51b: got {'message': '[Job 155] Job failed: Failed to delete volume \"ontap_41_nfs_vol01\" in Vserver \"ntap-svm01-nas\" because it has one or more clones.\\n\\nUse the \"volume clone show -parent-vserver ntap-svm01-nas -parent-volume ontap_41_nfs_vol01\" command to list clones, and either delete or split the clones and retry the operation.\\n\\nUse \"volume clone split start -vserver <vserver name> -flexclone <clone name>\" to split clones.\\nUse \"volume delete -vserver <vserver name> -volume <clone name>\" to delete clones.', 'code': '460770'}."}
changed: [cluster1] => (item={'uuid': '5075d55c-66cc-11ee-81f7-00505685c51b', 'name': 'clone', 'is_svm_root': False, 'svm': {'name': 'ntap-svm01-nas', 'uuid': '03003e2f-66cc-11ee-81f7-00505685c51b', '_links': {'self': {'href': '/api/svm/svms/03003e2f-66cc-11ee-81f7-00505685c51b'}}}, '_links': {'self': {'href': '/api/storage/volumes/5075d55c-66cc-11ee-81f7-00505685c51b'}}})
changed: [cluster1] => (item={'uuid': '516b2298-66cc-11ee-81f7-00505685c51b', 'name': 'db_backup', 'is_svm_root': False, 'svm': {'name': 'ntap-svm01-nas', 'uuid': '03003e2f-66cc-11ee-81f7-00505685c51b', '_links': {'self': {'href': '/api/svm/svms/03003e2f-66cc-11ee-81f7-00505685c51b'}}}, '_links': {'self': {'href': '/api/storage/volumes/516b2298-66cc-11ee-81f7-00505685c51b'}}})
```

Updates to make  
* Change name from db_backup to something software_dev or repo  
* Check if there is a way to scale to mulitple clients and mount points  
* Run complete demo - then walk it back  
* Investigate / fix revert issue  
