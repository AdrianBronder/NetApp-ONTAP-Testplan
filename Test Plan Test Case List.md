# NetApp ONTAP Test Plan - Test Case List

| Task	| Category                          | Decription                            |
| ---   | ---                               | ---                                   |
| 01-04 | Cluster Basic Connection Checks	| Ansible                               |
| 10-01 | Basic Cluster Configuration	    | Licenses                              |
| 10-02 | Basic Cluster Configuration	    | Physical Network                      |
| 10-03 | Basic Cluster Configuration	    | Network Services                      |
| 10-04 | Basic Cluster Configuration	    | Aggregates                            |
| 10-05 | Basic Cluster Configuration	    | AutoSupport                           |
| 11-01 | Advanced Cluster Configuration	| Cluster/Node Parameters               |
| 11-02 | Advanced Cluster Configuration	| Administrative Domain Authentication  |
| 11-03 | Advanced Cluster Configuration	| Key Manager                           |
| 12-01 | Cluster User Management	        | Read-only Local User                  |
| 12-02 | Cluster User Management	        | Administrative Local User             |
| 12-03 | Cluster User Management	        | Local User Access                     |
| 12-04 | Cluster User Management	        | Read-only Domain Group                |
| 12-05 | Cluster User Management	        | Administrative Domain Group           |
| 12-06 | Cluster User Management	        | Domain User Access                    |
| 12-10 | Cluster User Management	        | Admin Multifactor Authentication      |
| 20-01 | Basic Data SVM Setup	            | Storage Virtual Machines (SVMs)       |
| 20-02 | Basic Data SVM Setup	            | SVM network interfaces (LIFs)         |
| 20-03 | Basic Data SVM Setup	            | SVM Network Services                  |
| 20-04 | Basic Data SVM Setup	            | SVM Protocol Setup                    |
| 31-01 | NFS	                            | Export Policies & Rules               |
| 31-02 | NFS	                            | Volumes & Qtrees                      |
| 31-03 | NFS	                            | Mount & Write (Volumes)               |
| 31-04 | NFS	                            | FlexGroup & Qtrees                    |
| 31-05 | NFS	                            | Mount & Write (FlexGroups)            |
| 32-01 | CIFS	                            | Volumes & Qtrees                      |
| 32-02 | CIFS	                            | Shares & ACLs (Volume)                |
| 32-03 | CIFS	                            | Mount & Write (Volume)                |
| 32-04 | CIFS	                            | FlexGroup & qtrees                    |
| 32-05 | CIFS	                            | Shares & ACLs (FlexGroup)             |
| 32-06 | CIFS	                            | Mount & Write (FlexGroup)             |
| 35-01 | iSCSI	                            | iGroups                               |
| 35-02 | iSCSI	                            | Volumes                               |
| 35-03 | iSCSI	                            | LUNs & Mappings                       |
| 35-04 | iSCSI	                            | Mount & Write (Linux)                 |
| 35-05 | iSCSI	                            | Mount & Write (Windows)               |
| 37-01 | NVMe/TCP	                        | Volumes                               |
| 37-02 | NVMe/TCP	                        | Namespaces                            |
| 37-03 | NVMe/TCP	                        | Subsystem                             |
| 37-04 | NVMe/TCP	                        | Mount & Write (Linux)                 |
| 41-01 | Cloning (NFS)	                    | Export Policies & Rules               |
| 41-02 | Cloning (NFS)	                    | Origin Volume                         |
| 41-03 | Cloning (NFS)	                    | Mount & Write (Origin Volume)         |
| 41-04 | Cloning (NFS)	                    | Client Write (Origin Volume)          |
| 41-05 | Cloning (NFS)	                    | Clone Volume                          |
| 41-06 | Cloning (NFS)	                    | Mount & Write (Clone)                 |
| 41-07 | Cloning (NFS)	                    | Client Write (Clone)                  |
| 41-08 | Cloning (NFS)	                    | Clone & Write (Loop)                  |
|  ---  |                                   |                                       |
| Revert-00_linux   | Revert all systems to initial state - Linux                 | |
| Revert-00_windows | Revert all systems to initial state - Windows               | |
| Revert-00         | Revert all systems to initial state - ONTAP                 | |
| Revert-31         | Revert all steps performed in test frame 31 - NFS           | |
| Revert-32         | Revert all steps performed in test frame 32 - CIFS          | |
| Revert-35         | Revert all steps performed in test frame 35 - iSCSI         | |
| Revert-37         | Revert all steps performed in test frame 37 - NVMe/TCP      | |
| Revert-41         | Revert all steps performed in test frame 41 - NFS FlexClone | |