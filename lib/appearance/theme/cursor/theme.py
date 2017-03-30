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
from textwrap import dedent
import errno

setting = 'appearance.theme.cursor.theme'

def validate(data):

	if len(data) > 1:
		message('only one theme can be set', 'error')
		sys.exit(1)

	if data[0] not in list_all():
		message('theme "{}" does not exist'.format(data[0]), 'error')
		sys.exit(1)

	return data[0]

def info():

	return {
				'type': ['string'],
				'description': 'The mouse cursor theme',
				'data': ['name of the theme'],
			}

def set(data):

	# DE-independent method

	theme_dir = [x[1] for x in list_all(dir=True) if x[0] == data][-1]

	themes_dir = '/usr/share/icons' if os.getuid() == 0 else os.path.expanduser('~/.icons')

	try:
		os.symlink(os.path.join(theme_dir, 'cursors'),
				   os.path.join(themes_dir, 'default/cursors'))

	except OSError as e:
		if e.errno == errno.EEXIST:
			os.remove(os.path.join(themes_dir, 'default/cursors'))
			os.symlink(os.path.join(theme_dir, 'cursors'),
					   os.path.join(themes_dir, 'default/cursors'))

		else:
			raise


	with open(os.path.join(themes_dir, 'default/index.theme')) as f:
		contents = f.read()

	for line in contents[:].splitlines():
		if line.startswith('Inherits='):
			line_new = line.replace(line.split('=', 1)[-1], data)
			contents = contents.replace(line, line_new)

	with open(os.path.join(themes_dir, 'default/index.theme'), 'w') as f:
		f.write(contents)

	# Reload

	# First, rewrite the gtkrc file to not have any pre-existing
	# include entries.
	# Then gtk-theme-name entry is replaced.

	return

	with open(os.path.expanduser('~/.gtkrc-2.0')) as f:
		gtkrc = f.read()

	for line in gtkrc[:].splitlines():
		if line.startswith('gtk-theme-name'):
			gtkrc = gtkrc.replace(line, 'gtk-theme-name = "{}"'.format(data))

		elif line.startswith('include'):
			gtkrc = gtkrc.replace(line, '')

	with open(os.path.expanduser('~/.gtkrc-2.0'), 'w') as f:
		f.write(gtkrc)


def get():

	# DE-independent method

	themes_dir = '/usr/share/icons' if os.getuid() == 0 else os.path.expanduser('~/.icons')

	with open(os.path.join(themes_dir, 'default/index.theme')) as f:
		for line in f:
			if line.startswith('Inherits='):
				return line.split('=', 1)[-1].strip()

	# If code has reached this point, it means no theme was defined

	# Try with global if not defined locally
	if themes_dir != '/usr/share/icons':
		themes_dir = '/usr/share/icons'
		with open(os.path.join(themes_dir, 'default/index.theme')) as f:
			for line in f:
				if line.startswith('Inherits='):
					return line.split('=', 1)[-1].strip()

	# Still nothing?
	message('no cursor theme seems to be defined', level='warning')




def list_all(dir=False):

	xdg_data_dir = os.environ.get('XDG_DATA_HOME', '~/.local/share')
	xdg_data_dir = os.path.expanduser(xdg_data_dir)

	themes_dirs = ['/usr/share/icons',
				  os.path.join(xdg_data_dir, 'icons'),
				  os.path.expanduser('~/.icons')]

	themes = []

	for themes_dir in themes_dirs:
		for theme_dir in os.listdir(themes_dir):
			if 'cursors' in os.listdir(os.path.join(themes_dir, theme_dir)):
				if dir:
					themes.append((theme_dir, os.path.join(themes_dir, theme_dir)))

				else:
					themes.append(theme_dir)

	return themes


