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
import subprocess as sp
from textwrap import dedent
import errno

setting = 'appearance.theme.cursor.size'

def validate(data):

	if len(data) > 1:
		message('only one size can be set', 'error')
		sys.exit(1)

	try:
		int(data[0])

	except:
		message('value must be an integer', 'error')
		sys.exit(1)

	return int(data[0])

def info():

	return {
				'type': ['string'],
				'description': 'The mouse cursor theme',
				'data': ['name of the theme'],
			}

def set(data):

	return
	# TODO: desktop (and display-server) independent way of cursor size


def get():

	return

	# TODO: desktop (and display-server) independent way of cursor size
