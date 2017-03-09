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
import subprocess as sp

setting = 'appearance.desktop.wallpaper'

def format_set(data):

	if not os.path.isfile(data[0]):
		print('{name}: cannot access "{file}": no such file.'.format(name=setting, file=data[0]))
		sys.exit(0)

	return data

def info():

	return {
				'type': ['string'],
				'description': 'The current desktop background/wallpaper',
				'data': ['file path to the wallpaper'],
			}

def set(data):

	pass  # TODO
