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

setting = 'display.monitors'
read_only = True

def info():

	return {
				'type': ['list'],
				'description': 'The monitor()s connected to this computer',
				'data': ['names of the monitors'],
			}

def get():

	ls_monitors = Process('xrandr -q | grep connected | grep -v disconnected', shell=True).stdout

	# Typical output:
	# VGA1 connected primary 1440x900+0+0 (normal left inverted right x axis y axis) 410mm x 260mm

	ls_monitors = [x.split()[0] for x in ls_monitors.splitlines()]

	return ls_monitors

