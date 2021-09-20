# Snap-Rotate v3.0

Author: Erick Rodríguez 

Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com

License: GPLv3

Telk-Alert is a tool that through ElasticSearch (Query String) searches carried out every certain time, sends alerts to a Telegram channel or one or more email addresses in a timely manner, which translates into a constant and efficient monitoring of events stored in ElasticSearch.

# Applications
## Snap-Rotate
Application that allows data searches in ElasticSearch using defined rules, and when events are found, it allows sending alerts to the user with details about the event found.

Characteristics:
- The connection with ElasticSearch can be done through HTTPS and HTTP authentication (It must be configured in ElasticSearch).
- It has been tested to work with the indices generated by Auditbeat, Winlogbeat and Filebeat.
- The search in ElasticSearch is done through Query String.
- The sending of alerts can be sent to a Telegram channel or to one or more email addresses or both.
- The searches are carried out every certain configurable time. Which translates into 24/7 monitoring.
- N alert rules can be configured, each with a specific purpose.
- Generation of application logs both in a file and in an index in ElasticSearch.
- For security reasons, a user is created for the Telk-Alert service to work with.
- Sending alerts restricted by a certain number of events by hostname (For example, for failed user logins).
- Sending alerts restricted by a certain number of fields, that is, it does not send all the information about the event, but only sends the fields that were configured in the alert rule.
- In case of finding more than one event, the alert can be configured to send only one message and the total number of events or one message for each event found.
- Parse data that will be sent in the alert to give you a better view.

## Snap-Rotate-Tool
Telk-Alert graphical tool that allows the user to define the configuration and alert rules that will be used for the operation of the application. These data are saved in files with the extension yaml.

Characteristics:
- Allows you to create and modify the Telk-Alert connection settings.
- Allows you to create, modify and delete alert rules.
- Encrypts sensitive data such as passwords so that they are not stored in plain text.
- Allows you to start, restart, stop and get the status of the Telk-Alert service.
- Allows you to create and modify the Telk-Alert-Agent configuration.
- Allows you to start, restart, stop and get the status of the Telk-Alert-Agent service.

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
- It changes the owner of the files and directories necessary for the operation of Snap-Rotate, assigning them to the user created for this purpose.
- Creation of passphrase for the encryption and decryption of sensitive information, which is generated randomly, so it is unique for each installed Snap-Rotate installation.
- Creation of Snap-Rotate service.

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/