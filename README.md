# Snap-Rotate v3.1

Author: Erick Rodríguez 

Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com

License: GPLv3

Snap-Rotate is an application that creates a new FS (Shared File System) repository in ElasticSearch every month to store snapshots of certain indexes.

# Applications
## Snap-Rotate
Application that is responsible for rotating or creating new repositories every month and there to store snapshots of certain indexes.

![Snap-Rotate](https://github.com/erickrr-bd/Snap-Rotate/blob/master/screens/screen1.jpg)

Characteristics:
- The connection with ElasticSearch can be done through HTTPS and HTTP authentication (It must be configured in ElasticSearch).
- The first day of the month is when you create the repository for this month.
- Create snapshots only of those indices that have rotated or that are no longer being written to.
- It has a specific user for the execution of the service.
- It works as a service or daemon of the operating system.
- Sending alerts about the process to a Telegram channel.
- It allows deleting or not the indexes backed up in the created snapshot(s).
- It allows compressing or not the directory corresponding to the repository created.
- Generation of application logs.

## Snap-Rotate-Tool
Snap-Rotate-Tool is a graphical tool that helps the user to perform tasks around Snap-Rotate.

![Snap-Rotate-Tool](https://github.com/erickrr-bd/Snap-Rotate/blob/master/screens/screen2.jpg)

Characteristics:
- Allows you to create or modify the Snap-Rotate configuration file.
- Encrypts sensitive data such as passwords so that they are not stored in plain text.
- Allows you to start, restart, stop and get the status of the Snap-Rotate service.
- Generation of application logs.

# Requirements
- CentOS 8 (So far it has only been tested in this version)
- ElasticSearch 7.x 
- Python 3.6
- Python Libraries
  - elasticsearch-dsl
  - requests
  - pythondialog
  - pycryptodome
  - pyyaml

# Installation
To install or update Snap-Rotate you must run the script "installer_snap_rotate.sh" for this you can use any of the following commands:

`./installer_snap_rotate.sh` or `sh installer_snap_rotate.sh`

The installer performs the following actions on the computer:

- Copy and creation of directories and files necessary for the operation of Snap-Rotate.
- Creation of user and specific group for the operation of Snap-Rotate.
- It changes the owner of the files and directories necessary for the operation of Snap-Rotate, assigning them to the user created for this purpose.
- Creation of passphrase for the encryption and decryption of sensitive information, which is generated randomly, so it is unique for each installed Snap-Rotate installation.
- Creation of Snap-Rotate service.

# Running

- Run as service:

`systemctl start snap-rotate.service`

- To execute manually, first you must go to the path /etc/Snap-Rotate-Suite/Snap-Rotate and execute using the following commands:

`python3 Snap_Rotate.py` or `./Snap_Rotate.py`


- To execute Snap-Rotate-Tool, first you must go to the path /etc/Snap-Rotate-Suite/Snap-Rotate-Tool and execute using the following commands:

`python3 Snap_Rotate_Tool.py` or `./Snap_Rotate_Tool.py`

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
