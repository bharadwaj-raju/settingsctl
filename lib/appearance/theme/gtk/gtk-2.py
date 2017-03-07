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

setting = 'appearance.theme.gtk.gtk-2'

def format_set(data):

	if len(data) > 1:
		message('only one theme can be set', 'error')
		sys.exit(1)

	return data[0]

def info():

	return {
				'type': ['string'],
				'description': 'the theme name'
			}

def set(data):

	# First, rewrite the gtkrc file to not have any pre-existing
	# include entries.
	# Then gtk-theme-name entry is replaced.

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

	# Scan gtkrc for gtk-theme-name and include configuration entries
	# Return the most appropriate

	with open(os.path.expanduser('~/.gtkrc-2.0')) as f:
		theme_conf_lines = []
		include_lines = []
		line_no = 0
		for line in f:
			line_no += 1
			if line.startswith('gtk-theme-name'):
				theme_conf_lines.append((line, line_no))

			elif line.startswith('include'):
				include_lines.append((line, line_no))

		if not include_lines:
			include_lines = [('', 0)]

		if not theme_conf_lines:
			theme_conf_lines = [('', 0)]

		theme_name = theme_conf_lines[-1]
		include = include_lines[-1]

		if len(theme_conf_lines) > 1 or len(include_lines) > 1:
			message('different themes are set together in ~/.gtkrc', 'warning')

		theme = {}

		theme['gtk-theme-name'] = theme_name[0].split('=', 1)[-1].replace('"', '').strip()

		theme_file = include[0].split(' ', 1)[-1].replace('"', '')

		if theme_file.startswith('/usr/share/themes') or \
				theme_file.startswith('~/.themes') or \
				theme_file.startswith(os.path.expanduser('~/.themes')):
			theme['include'] = theme_file.replace('/usr/share/themes', '').replace('~/.themes', '').replace(os.path.expanduser('~/.themes'), '')
			theme['include'] = theme['include'].split('/')[0] or theme['include'].split('/')[1]

		if not theme.get('include', None):
			return theme['gtk-theme-name']

		if theme.get('include', None) == theme.get('gtk-theme-name', 0):
			return theme['gtk-theme-name']

		else:
			message('different themes are set together in ~/.gtkrc, reporting the one set by include directive', 'warning')
			return theme['include']


		# gtk-theme-name is what will be likely reported by settings managers
		# but the include entry is what is usually followed by applications
		# thus a warning is issued to stdout

		return theme


