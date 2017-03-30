#!/bin/bash

# Shellcheck verified!

set -e

cd /tmp

echo "Downloading..."

wget https://github.com/bharadwaj-raju/settingsctl/archive/master.tar.gz 2>/dev/null

tar -xvf master.tar.gz > /dev/null

cd settingsctl-master

echo "Install locally or system-wide? (enter 'l' for local and 's' for system-wide). ^C (Control-C) to abort."

read -r choice

case $choice in
	l)
		./install.py --user
		;;

	s)
		if [[ $(id -u) -eq 0 ]]; then
			./install.py

		else
			sudo ./install.py

		fi

		;;

	*)
		echo "Please enter 'l' for local installation or 's' for system-wide installation!"
		echo "Defaulting to local installation!"
		./install.py --user
		;;

esac


