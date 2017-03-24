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

setting = 'appearance.theme.gtk.gtk-3'

config_home = os.path.expanduser(os.environ.get('XDG_CONFIG_HOME', '~/.config'))
settings_file = os.path.join(config_home, 'gtk-3.0/settings.ini')

desktop = Process([os.getenv('SETTINGSCTL_BIN'), 'get', 'desktop-environment']).stdout

def validate(data):

	if len(data) > 1:
		message('only one theme can be set', 'error')
		sys.exit(1)

	return data[0]

def info():

	return {
				'type': ['string'],
				'description': 'The current theme for GTK+ 3 applications',
				'data': ['the name of the theme'],
			}

def set(data):

	# Replace gtk-theme-name entry in gtk settings.ini.

	if desktop in ['gnome', 'unity', 'cinnamon', 'budgie']:
		key = 'org.gnome.desktop.interface'

	elif desktop == 'pantheon':
		key = 'org.pantheon.desktop.interface'

	try:
		Process(['gsettings', 'set', key, 'gtk-theme', data])

	except UnboundLocalError:
		# Not GNOME-based desktop
		# Thus, values key and data won't be set (see if condition above)
		pass


	with open(settings_file) as f:
		gtk_settings = f.read()

	for line in gtk_settings[:].splitlines():
		if line.startswith('gtk-theme-name'):
			gtk_settings = gtk_settings.replace(line, 'gtk-theme-name={}'.format(data))

	with open(settings_file, 'w') as f:
		f.write(gtk_settings)


def get():

	# Scan gtk settings.ini for gtk-theme-name configuration entries

	if desktop in ['gnome', 'unity', 'cinnamon', 'budgie']:
		key = 'org.gnome.desktop.interface'

	elif desktop == 'pantheon':
		key = 'org.pantheon.desktop.interface'

	try:
		de_theme = Process(['gsettings', 'get', key, 'gtk-theme']).stdout

	except UnboundLocalError:
		# Not GNOME-based desktop
		pass


	with open(settings_file) as f:
		for line in f:
			if line.startswith('gtk-theme-name'):
				theme = line.split('=', 1)[-1].replace('"', '').strip()

	try:
		return theme if de_theme == theme else de_theme

	except UnboundLocalError:
		# Not GNOME-based desktop
		# Thus, values key and data won't be set (see if-elif and try-except above)
		return theme



