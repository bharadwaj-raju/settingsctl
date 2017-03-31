# This file is a part of settingsctl.

# settingsctl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# settingsctl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with settingsctl.  If not, see <http://www.gnu.org/licenses/gpl.txt>.

# A copy of the license is included in the LICENSE file, which should have
# been distributed along with this program.
# If not, see http://www.gnu.org/licenses/gpl.txt


# Copyright © Bharadwaj Raju and other contributors (list of contributors: https://github.com/bharadwaj-raju/settingsctl/graphs/contributors)

import os
import sys
from textwrap import dedent

setting = 'power.screen-lock.enabled'

desktop_env = Process([os.environ.get('SETTINGSCTL_BIN'), 'get', 'desktop-environment']).stdout

if os.environ.get('XDG_CONFIG_HOME', None) is not None:
	xdg_config_home = os.environ.get('XDG_CONFIG_HOME')

else:
	xdg_config_home = os.path.expanduser('~/.config')

def validate(data):

	if len(data) > 1:
		message('only one boolean (true/false) value can be set', 'error')
		sys.exit(1)

	if data[0].lower() not in ['true', 'false']:
		message('value must be a boolean ("true" or "false")', 'error')
		sys.exit(1)

	return data[0].lower()

def info():

	return {
				'type': ['boolean'],
				'description': 'Whether screen lock is enabled or not',
				'data': ['is screen lock enabled?'],
			}

def set(data):

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'budgie']:
		Process(['gsettings', 'set', 'org.gnome.desktop.screensaver',
				 'lock-enabled', data])

	elif desktop_env == 'kde':
		with open(os.path.join(xdg_config_home, 'kscreenlockerrc')) as f:
			contents = f.read()

		for line in contents[:]:
			if line.startswith('Autolock='):
				contents.replace(line, 'Autolock=' + data)

		with open(os.path.join(xdg_config_home, 'kscreenlockerrc'), 'w') as f:
			f.write(contents)

	# TODO: Needs input for other desktops


def get():

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'budgie']:
		return Process(['gsettings', 'get', 'org.gnome.desktop.screensaver',
				 'lock-enabled']).stdout

	elif desktop_env == 'kde':
		with open(os.path.join(xdg_config_home, 'kscreenlockerrc')) as f:
			for line in f:
				if line.startswith('Autolock='):
					return line.split('=', 1)[-1].strip()

	# TODO: Needs input for other desktops

