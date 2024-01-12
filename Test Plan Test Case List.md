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
| 51-01 | Local Versioning (Snapshots)	    | Custom Policy                         |
| 51-02 | Local Versioning (Snapshots)	    | Prepare Filesystem                    |
| 51-03 | Local Versioning (Snapshots)	    | Create Snapshot                       |
| 51-04 | Local Versioning (Snapshots)	    | Delete Files                          |
| 51-05 | Local Versioning (Snapshots)	    | Restore Snapshot                      |
| 52-01 | Backup (SnapMirror)               | SVM Peering                           |
| 52-02 | Backup (SnapMirror)               | Custom Policies                       |
| 52-03 | Backup (SnapMirror)               | Prepare Filesystem (Source)           |
| 52-04 | Backup (SnapMirror)               | Protect Volume                        |
| 52-05 | Backup (SnapMirror)               | Access Backup (read-only)             |
| 52-06 | Backup (SnapMirror)               | Create Additional Files               |
| 52-07 | Backup (SnapMirror)               | Create Incremental Backup             |
| 52-08 | Backup (SnapMirror)               | Delete Files                          |
| 52-09 | Backup (SnapMirror)               | Restore Backup                        |
| 52-11 | Backup (SnapMirror)               | Bulk Protect Volumes                  |
| ---   | ---                               | ---                                   |
| Prepare-15         | Prepare test frame 15 - Cluster Peering                    | |
| Prepare-20         | Prepare test frame 20 - Storage Virtual Machines (SVMs)    | |
| Prepare-31         | Prepare test frame 31 - NFS                                | |
| Prepare-32         | Prepare test frame 32 - CIFS                               | |
| Prepare-35         | Prepare test frame 35 - iSCSI                              | |
| Prepare-37         | Prepare test frame 37 - NVMe/TCP                           | |
| Prepare-41         | Prepare test frame 41 - NFS FlexClone                      | |
| Prepare-51         | Prepare test frame 51 - Local Versioning (Snapshots)       | |
| Prepare-52         | Prepare test frame 52 - Backup (SnapMirror)                | |
| ---   | ---                               | ---                                   |
| Revert-00_linux   | Revert all systems to initial state - Linux                 | |
| Revert-00_windows | Revert all systems to initial state - Windows               | |
| Revert-00         | Revert all systems to initial state - ONTAP                 | |
| Revert-20         | Revert test frame 20 - Storage Virtual Machines (SVMs)      | |
| Revert-31         | Revert test frame 31 - NFS                                  | |
| Revert-32         | Revert test frame 32 - CIFS                                 | |
| Revert-35         | Revert test frame 35 - iSCSI                                | |
| Revert-37         | Revert test frame 37 - NVMe/TCP                             | |
| Revert-41         | Revert test frame 41 - NFS FlexClone                        | |
| Revert-51         | Revert test frame 51 - Local Versioning (Snapshots)         | |
| Revert-52         | Revert test frame 52 - Backup (SnapMirror)                  | |