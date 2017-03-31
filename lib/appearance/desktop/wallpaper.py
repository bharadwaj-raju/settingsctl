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
import traceback
from textwrap import dedent

setting = 'appearance.desktop.wallpaper'

if os.environ.get('XDG_CONFIG_HOME'):
	config_dir = os.path.expanduser(os.environ.get('XDG_CONFIG_HOME'))

else:
	config_dir = os.path.expanduser('~/.config')

desktop_env = Process([os.environ.get('SETTINGSCTL_BIN'), 'get', 'desktop-environment']).stdout

def validate(data):

	if len(data) > 1:
		message('only one wallpaper can be set', 'error')
		sys.exit(1)

	if not os.path.isfile(data[0]):
		message('no such file "{}"'.format(data[0]), 'error')
		sys.exit(1)

	return data[0]

def info():

	return {
				'type': ['string'],
				'description': 'The current desktop background/wallpaper',
				'data': ['file path to the wallpaper'],
			}

def get():

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'mate']:
		SCHEMA = 'org.gnome.desktop.background'
		KEY = 'picture-uri'

		if desktop_env == 'mate':
			SCHEMA = 'org.mate.background'
			KEY = 'picture-filename'

		proc = Process(['gsettings', 'get', SCHEMA, KEY])

		if proc.return_code != 0:
			proc = Process(['mateconftool-2', '-t', 'string', '--get',
							'/desktop/mate/background/picture-filename'])

		return proc.stdout

	elif desktop_env == 'gnome2':
		return Process(['gconftool-2', '-t', 'string', '--get',
						'/desktop/gnome/background/picture_filename']).replace('file://', '')

	elif desktop_env == 'kde':
		conf_file = os.path.join(config_dir, 'plasma-org.kde.plasma.desktop-appletsrc')

		line_count = 0
		line_found = 0

		with open(conf_file) as f:
			contents = f.read().splitlines()

		for line in contents:
			line_count += 1

			if '[Wallpaper]' in line and line.startswith('['):
				line_found = int(line_count)
				break

		if line_found != 0:
			contents = contents[line_found:]

			for line in contents:
				if line.startswith('Image'):
					return line.split('=', 1)[-1].strip().replace('file://', '').replace('"', '').replace("'", '')

	elif desktop_env == 'xfce':
		# XFCE4's image property is not image-path but last-image (What?)

		list_of_properties = Process(['xfconf-query', '-R', '-l', '-c',
									  'xfce-desktop', '-p', '/backdrop']).stdout

		for i in list_of_properties.splitlines():
			if i.endswith('last-image') and 'workspace' in i:
				# The property given is a background property
				return Process(
					['xfconf-query', '-c', 'xfce-desktop', '-p', i]).stdout

	elif desktop_env == 'razor-qt':
		desktop_conf = configparser.ConfigParser()
		# Development version

		desktop_conf_file = os.path.join(config_dir, 'razor', 'desktop.conf')

		if os.path.isfile(desktop_conf_file):
			config_option = r'screens\1\desktops\1\wallpaper'

		else:
			desktop_conf_file = os.path.join(
				os.path.expanduser('~'), '.razor/desktop.conf')
			config_option = r'desktops\1\wallpaper'

		desktop_conf.read(os.path.join(desktop_conf_file))

		try:
			if desktop_conf.has_option('razor', config_option):
				return desktop_conf.get('razor', config_option)
		except:
			pass

	elif desktop_env in ['fluxbox', 'jwm', 'openbox', 'afterstep', 'i3']:
		# feh stores last feh command in '~/.fehbg'
		# parse it
		with open(os.path.expanduser('~/.fehbg')) as f:
			fehbg = f.read()

		fehbg = fehbg.split('\n')

		for line in fehbg:
			if '#!' in line:
				fehbg.remove(line)

		fehbg = fehbg[0]

		for i in fehbg.split(' '):
			if not i.startswith("-"):
				if not i.startswith('feh'):
					if not i in ['', ' ', '  ', '\n']:
						return(i.replace("'", ''))

	elif desktop_env == 'icewm':
		with open(os.path.expanduser('~/.icewm/preferences')) as f:
			for line in f:
				if line.startswith('DesktopBackgroundImage'):
					return os.path.expanduser(line.strip().split(
						'=', 1)[1].strip().replace('"', '').replace("'", ''))

	elif desktop_env == 'awesome':
		conf_file = os.path.join(config_dir, 'awesome', 'rc.lua')

		with open(conf_file) as f:
			for line in f:
				if line.startswith('theme_path'):
					awesome_theme = line.strip().split('=', 1)
					awesome_theme = awesome_theme[
						len(awesome_theme) - 1].strip().replace('"', '').replace("'", '')

		with open(os.path.expanduser(awesome_theme)) as f:
			for line in f:
				if line.startswith('theme.wallpaper'):
					awesome_wallpaper = line.strip().split('=', 1)
					awesome_wallpaper = awesome_wallpaper[
						len(awesome_wallpaper) - 1].strip().replace('"', '').replace("'", '')

					return os.path.expanduser(awesome_wallpaper)

	# TODO: way to get wallpaper for desktops which are commented-out below

	# elif desktop_env == 'blackbox':
	# 	args = ['bsetbg', '-full', image]
	# 	sp.Popen(args)
	#
	# elif desktop_env == 'lxde':
	# 	args = 'pcmanfm --set-wallpaper %s --wallpaper-mode=scaled' % image
	# 	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'lxqt':
	# 	args = 'pcmanfm-qt --set-wallpaper %s --wallpaper-mode=scaled' % image
	# 	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'windowmaker':
	# 	args = 'wmsetbg -s -u %s' % image
	# 	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'enlightenment':
	#	args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
	#	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'awesome':
	# 	with sp.Popen("awesome-client", stdin=sp.PIPE) as awesome_client:
	# 		command = 'local gears = require("gears"); for s = 1, screen.count()
	#       do gears.wallpaper.maximized("%s", s, true); end;' % image
	# 		awesome_client.communicate(input=bytes(command, 'UTF-8'))

def set(image):

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'mate']:
		uri = 'file://%s' % image

		SCHEMA = 'org.gnome.desktop.background'
		KEY = 'picture-uri'

		if desktop_env == 'mate':
			uri = image

			SCHEMA = 'org.mate.background'
			KEY = 'picture-filename'

		proc = Process(['gsettings', 'set', SCHEMA, KEY, image])

		if proc.return_code != 0:
			Process(['mateconftool-2', '-t', 'string', '--set',
					 '/desktop/mate/background/picture-filename',
					 image])

	elif desktop_env == 'gnome2':
		Process(
			['gconftool-2', '-t', 'string', '--set', '/desktop/gnome/background/picture_filename', image]
		)

	elif desktop_env == 'kde':
		# This probably only works in Plasma 5+

		kde_script = dedent(
		'''\
		var Desktops = desktops();
		for (i=0;i<Desktops.length;i++) {
			d = Desktops[i];
			d.wallpaperPlugin = "org.kde.image";
			d.currentConfigGroup = Array("Wallpaper",
										"org.kde.image",
										"General");
			d.writeConfig("Image", "file://%s");
		}
		''') % image

		Process(
				['dbus-send', '--session', '--dest=org.kde.plasmashell',
				 '--type=method_call', '/PlasmaShell',
				 'org.kde.PlasmaShell.evaluateScript',
				 'string:{}'.format(kde_script)]
		)

	elif desktop_env in ['kde3', 'trinity']:
		args = ['dcop', 'kdesktop', 'KBackgroundIface', 'setWallpaper', '0', image, '6']
		sp.Popen(args)

	elif desktop_env == 'xfce4':
		# XFCE4's image property is not image-path but last-image (What?)

		list_of_properties = Process(['xfconf-query', '-R', '-l', '-c', 'xfce4-desktop', '-p', '/backdrop']
			).stdout

		for i in list_of_properties.splitlines():
			if i.endswith('last-image'):
				# The property given is a background property
				Process(['xfconf-query', '-c', 'xfce4-desktop', '-p', i, '-s', image])

				Process(['xfdesktop', '--reload'])

	elif desktop_env == 'razor-qt':
		desktop_conf = configparser.ConfigParser()
		# Development version

		desktop_conf_file = os.path.join(
			config_dir, 'razor', 'desktop.conf')

		if os.path.isfile(desktop_conf_file):
			config_option = r'screens\1\desktops\1\wallpaper'

		else:
			desktop_conf_file = os.path.join(
				os.path.expanduser('~'), '.razor/desktop.conf')
			config_option = r'desktops\1\wallpaper'

		desktop_conf.read(os.path.join(desktop_conf_file))
		try:
			if desktop_conf.has_option('razor', config_option):
				desktop_conf.set('razor', config_option, image)
				with codecs.open(desktop_conf_file, 'w', encoding='utf-8', errors='replace') as f:
					desktop_conf.write(f)
		except:
			pass

	elif desktop_env in ['fluxbox', 'jwm', 'openbox', 'afterstep', 'i3']:
		try:
			args = ['feh', '--bg-scale', image]
			Process(args)
		except:
			pass
			# TODO: support for feh alternatives (nitrogen etc)

	elif desktop_env == 'icewm':
		args = ['icewmbg', image]
		Process(args)

	elif desktop_env == 'blackbox':
		args = ['bsetbg', '-full', image]
		Process(args)

	elif desktop_env == 'lxde':
		args = ['pcmanfm', '--set-wallpaper', image, '--wallpaper-mode=scaled']
		Process(args)

	elif desktop_env == 'lxqt':
		args = ['pcmanfm-qt', '--set-wallpaper', image, '--wallpaper-mode=scaled']
		Process(args)

	elif desktop_env == 'windowmaker':
		args = ['wmsetbg', '-s', '-u', image]
		Process(args)

	elif desktop_env == 'enlightenment':
		args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
		Process(['enlightenment_remote', '-desktop-bg-add', '0', '0', '0', '0',
				 image])

	elif desktop_env == 'awesome':
		with sp.Popen("awesome-client", stdin=sp.PIPE) as awesome_client:
			command = ('local gears = require("gears"); for s = 1,'
						' screen.count() do gears.wallpaper.maximized'
						'("%s", s, true); end;') % image
			awesome_client.communicate(input=command.encode('utf-8'))

