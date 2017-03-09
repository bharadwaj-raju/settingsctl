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

setting = 'desktop-environment'
read_only = True

def info():

	return {
			'type': ['string'],
			'description': 'The running desktop environment or window manager',
			'data': ['the name of the desktop environment'],
			}

def get():

	desktop_session = os.environ.get('XDG_CURRENT_DESKTOP', os.environ.get('DESKTOP_SESSION'))

	if desktop_session is not None:
		desktop_session = desktop_session.lower()

		# Fix for X-Cinnamon etc
		if desktop_session.startswith('x-'):
			desktop_session = desktop_session.replace('x-', '', 1)

		if desktop_session in ['gnome', 'unity', 'cinnamon', 'mate',
								'xfce', 'lxde', 'fluxbox',
								'blackbox', 'openbox', 'icewm', 'jwm',
								'afterstep', 'trinity', 'kde', 'pantheon',
								'i3', 'lxqt', 'awesome', 'enlightenment',
								'budgie', 'awesome', 'ratpoison']:

			return desktop_session

		#-- Special cases --#

		# Canonical sets environment var to Lubuntu rather than
		# LXDE if using LXDE.
		# There is no guarantee that they will not do the same
		# with the other desktop environments.

		elif 'xfce' in desktop_session:
			return 'xfce'

		elif desktop_session.startswith('ubuntu'):
			return 'unity'

		elif desktop_session.startswith('xubuntu'):
			return 'xfce'

		elif desktop_session.startswith('lubuntu'):
			return 'lxde'

		elif desktop_session.startswith('kubuntu'):
			return 'kde'

		elif desktop_session.startswith('razor'):
			return 'razor-qt'

		elif desktop_session.startswith('wmaker'):
			return 'windowmaker'

	if os.environ.get('KDE_FULL_SESSION') == 'true':
		return 'kde'

	elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
		if not 'deprecated' in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
			return 'gnome2'

	return 'unknown'


def list_all():

	return ['gnome', 'unity', 'cinnamon', 'mate',
			'xfce', 'lxde', 'fluxbox', 'windowmaker',
			'blackbox', 'openbox', 'icewm', 'jwm',
			'afterstep', 'trinity', 'kde', 'pantheon',
			'i3', 'lxqt', 'awesome', 'enlightenment',
			'budgie', 'awesome', 'ratpoison', 'razor-qt', 'gnome2']




