#! /bin/bash

clear
echo -e "\e[96m@2022 Tekium. All rights reserved.\e[0m"
echo -e '\e[96mInstaller for Snap-Rotate v3.1\e[0m'
echo -e '\e[96mAuthor: Erick Rodríguez\e[0m'
echo -e '\e[96mEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\e[0m'
echo -e '\e[96mLicense: GPLv3\e[0m'
echo ''
echo -e '\e[1;33m--------------------------------------------------------------------------------\e[0m'
echo ''
echo 'Do you want to install or update Snap-Rotate on the computer (I/U)?'
read opc
if [ $opc = "I" ] || [ $opc = "i" ]; then
	echo ''
	echo -e '\e[96mStarting the Snap-Rotate installation...\e[0m'
	echo ''
	echo 'Do you want to install the packages and libraries necessary for the operation of Snap-Rotate (Y/N)?'
	read opc_lib
	if [ $opc_lib = "Y" ] || [ $opc_lib = "y" ]; then
		echo ''
		echo -e '\e[96mStarting the installation of the required packages and libraries...\e[0m'
		yum install python3-pip -y
		dnf install dialog -y
		dnf install gcc -y
		dnf install python3-devel -y
		dnf install libcurl-devel -y
		dnf install openssl-devel -y
		pip3 install pythondialog 
		pip3 install pycryptodome
		pip3 install pyyaml 
		pip3 install pycurl 
		pip3 install elasticsearch-dsl 
		pip3 install requests 
		echo ''
		echo -e '\e[96mRequired installed libraries...\e[0m'
		sleep 3
		echo ''
	fi
	echo ''
	echo -e '\e[96mCreating user and group for Snap-Rotate...\e[0m'
	groupadd snap_rotate
	useradd -M -s /bin/nologin -g snap_rotate -d /etc/Snap-Rotate-Suite snap_rotate
	echo ''
	echo -e '\e[96mUser and group created...\e[0m'
	sleep 3
	echo ''
	echo -e '\e[96mCreating the necessary services for Snap-Rotate...\e[0m'
	dir=$(sudo pwd)
	cd $dir
	cp snap-rotate.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable snap-rotate.service
	echo ''
	echo -e '\e[96mCreated services...\e[0m'
	sleep 3
	echo ''
	echo -e '\e[96mCopying and creating the required directories for Snap-Rotate...\e[0m'
	echo ''
	cp -r Snap-Rotate-Suite /etc/
	mkdir /etc/Snap-Rotate-Suite/Snap-Rotate/conf
	mkdir /var/log/Snap-Rotate
	echo -e '\e[96mDirectories copied and created...\e[0m'
	sleep 3
	echo ''
	echo -e '\e[96mCreating passphrase...\e[0m'
	passphrase=$(cat /dev/random | tr -dc '[:alpha:]' | head -c 30; echo)
	cat << EOF > /etc/Snap-Rotate-Suite/Snap-Rotate/conf/key 
$passphrase
EOF
	echo ''
	echo -e '\e[96mPassphrase created...\e[0m'
	sleep 3
	echo ''
	chown snap_rotate:snap_rotate -R /etc/Snap-Rotate-Suite
	chown snap_rotate:snap_rotate -R /var/log/Snap-Rotate
	echo -e '\e[96mSnap-Rotate installed on the computer...\e[0m'
	sleep 3	
	echo ''
	echo -e '\e[96mStarting Snap-Rotate-Tool...\e[0m'
	sleep 5
	cd /etc/Snap-Rotate-Suite/Snap-Rotate-Tool
	python3 Snap_Rotate_Tool.py
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	echo ''
	echo -e '\e[96mStarting the Snap-Rotate update...\e[0m'
	echo ''
	systemctl stop snap-rotate.service
	dir=$(sudo pwd)
	cp -r Snap-Rotate-Suite /etc/
	chown snap_rotate:snap_rotate -R /etc/Snap-Rotate-Suite
	cp snap-rotate.service /etc/systemd/system/
	systemctl daemon-reload
	rm -rf /etc/Snap-Rotate-Suite/Snap-Rotate/conf/snap_rotate_conf.yaml
	sleep 3
	echo -e '\e[96mSnap-Rotate updated...\e[0m'
	echo ''
	echo -e '\e[96mStarting Snap-Rotate-Tool...\e[0m'
	sleep 5
	cd /etc/Snap-Rotate-Suite/Snap-Rotate-Tool
	python3 Snap_Rotate_Tool.py
else
	clear
	exit
fi