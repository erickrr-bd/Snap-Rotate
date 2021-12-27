# Snap-Rotate v3.1

Author: Erick Rodríguez 

Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com

License: GPLv3

Snap-Rotate is an application that creates a new FS (Shared File System) repository in ElasticSearch every month to store snapshots of certain indexes.

# Applications
## Snap-Rotate
Application that is responsible for rotating or creating new repositories every month and there to store snapshots of certain indexes.

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
To install or update Snap-Rotate, you must run the installer_snap_rotate.sh executable with administrator rights. The installer will perform the following actions:
- Copy and creation of directories and files necessary for the operation of Snap-Rotate.
- Creation of passphrase for the encryption and decryption of sensitive information, which is generated randomly, so it is unique for each installed Snap-Rotate installation.
- Creation of Snap-Rotate service.

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
