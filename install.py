#!/usr/bin/env python3

import os
import sys
import shutil

if '--user' in sys.argv:
	bin_path = os.path.expanduser('~/bin')
	lib_path = os.path.expanduser('~/.local/lib/settingsctl')

	for i in [bin_path, lib_path]:
		if not os.path.isdir(i):
			os.mkdir(i)

else:
	# Assume system-wide
	if os.getuid() != 0:  # 0 means root
		print('error: For system-wide installation, this script must be run as the root user: sudo ./install.py')
		print('info: If you want to install just for your user (this will override system-wide one), use the --user option.')
		sys.exit(1)

	bin_path = '/usr/bin'
	lib_path = '/usr/lib/settingsctl'

if os.path.isfile(os.path.join(bin_path, 'settingsctl')):
	os.remove(os.path.join(bin_path, 'settingsctl'))

if os.path.isdir(lib_path):
	os.rmdir(lib_path)

shutil.copy('settingsctl', bin_path)
shutil.copytree('lib', lib_path)


