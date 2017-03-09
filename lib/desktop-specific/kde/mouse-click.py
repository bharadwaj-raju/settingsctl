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


# Copyright © Bharadwaj Raju <bharadwaj.raju777@gmail.com>

import os
import sys

setting = 'desktop-specific.kde.mouse-click'

config_home = os.path.expanduser(os.environ.get('XDG_CONFIG_HOME', '~/.config'))
settings_file = os.path.join(config_home, 'kdeglobals')

def format_set(data):

	if data[0].lower() not in ['single', 'double']:
		message('value must be one of "single" or "double"', 'error')
		sys.exit(1)

	return data[0].lower()

def info():

	return {
				'type': ['string'],
				'description': 'Whether to use single or double click to open files and folders in KDE',
				'data': ['must be one of "single" or "double"'],
			}

def set(data):

	# Replace SingleClick={true|false} entry in kdeglobals.

	with open(settings_file) as f:
		settings = f.read()

	for line in settings[:].splitlines():
		if line.startswith('SingleClick'):
			settings = settings.replace(line, 'SingleClick={}'.format('true' if data == 'single' else 'false'))

	with open(settings_file, 'w') as f:
		f.write(settings)


def get():

	# Scan kdeglobals for SingleClick configuration entries

	with open(settings_file) as f:
		for line in f:
			if line.startswith('SingleClick'):
				theme = line.split('=', 1)[-1].replace('"', '').strip()

	return 'single' if theme in ['true', '1'] else 'double'



