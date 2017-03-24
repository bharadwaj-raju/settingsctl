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

setting = 'display.resolution'

ls_monitors = Process('xrandr -q | grep connected | grep -v disconnected', shell=True).stdout

# Typical output:
# VGA1 connected primary 1440x900+0+0 (normal left inverted right x axis y axis) 410mm x 260mm

def validate(data):

	if data[0] not in [x.split(' ')[0] for x in ls_monitors.splitlines()]:
		message('no such monitor connected', 'error')
		sys.exit(0)

	return {
				'monitor': data[0],
				'resolution': data[1]
			}


def info():

	return {
				'type': ['string', 'string'],
				'description': 'The display resolution(s)',
				'data': ['name of the monitor', 'resolution in heightxwidth format'],
			}

def set(data):

	Process(['xrandr', '--output', data['monitor'], '--mode', data['resolution']])


def get():

	monitor_resolutions = {}

	for i in ls_monitors.splitlines():
		mon, res = i.split(' ')[0], i.split(' ')[3].split('+', 1)[0]
		monitor_resolutions[mon] = res

	if os.environ.get('SETTINGSCTL_USE_JSON', False):
		return monitor_resolutions

	else:
		retval = ''

		for mon in monitor_resolutions:
			retval += '{} {}'.format(mon, monitor_resolutions[mon])

		return retval

