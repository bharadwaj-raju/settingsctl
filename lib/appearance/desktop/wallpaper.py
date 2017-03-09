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
import traceback
from textwrap import dedent

setting = 'appearance.desktop.wallpaper'

if os.environ.get('XDG_CONFIG_HOME'):
	config_dir = os.path.expanduser(os.environ.get('XDG_CONFIG_HOME'))

else:
	config_dir = os.path.expanduser('~/.config')

desktop_env = sp.check_output([os.environ.get('SETTINGSCTL_BIN'), 'get', 'desktop-environment']).decode('utf-8').strip()

def format_set(data):

	if not os.path.isfile(data[0]):
		print('{name}: cannot access "{file}": no such file.'.format(name=setting, file=data[0]))
		sys.exit(1)

	return data

def info():

	return {
				'type': ['string'],
				'description': 'The current desktop background/wallpaper',
				'data': ['file path to the wallpaper'],
			}

def set(data):

	pass  # TODO


def get():

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'mate']:
		SCHEMA = 'org.gnome.desktop.background'
		KEY = 'picture-uri'

		if desktop_env == 'mate':
			SCHEMA = 'org.mate.background'
			KEY = 'picture-filename'

		try:
			from gi.repository import Gio

			gsettings = Gio.Settings.new(SCHEMA)
			return gsettings.get_string(KEY).replace('file://', '')

		except ImportError:
			try:
				return sp.check_output(
					['gsettings', 'get', SCHEMA, KEY]).replace('file://', '')
			except:  # MATE < 1.6
				return sp.check_output(
						['mateconftool-2', '-t', 'string', '--get',
						 '/desktop/mate/background/picture_filename']
						).replace('file://', '')

	elif desktop_env == 'gnome2':
		args = ['gconftool-2', '-t', 'string', '--get',
				'/desktop/gnome/background/picture_filename']
		return sp.check_output(args).replace('file://', '')

	elif desktop_env == 'kde':
		conf_file = os.path.join(config_dir, 'plasma-org.kde.plasma.desktop-appletsrc')
		with open(conf_file) as f:
			contents = f.read()

		contents = contents.splitlines()

		contents = contents[
			contents.index(
			'[Containments][8][Wallpaper][org.kde.image][General]') + 1
			].split('=', 1)

		return contents[len(contents) - 1].strip().replace('file://', '')

	elif desktop_env == 'xfce':
		# XFCE4's image property is not image-path but last-image (What?)

		list_of_properties = sp.check_output(
			['xfconf-query', '-R', '-l', '-c', 'xfce-desktop', '-p',
			 '/backdrop']).decode('utf-8').strip()

		for i in list_of_properties.split('\n'):
			if i.endswith('last-image') and 'workspace' in i:
				# The property given is a background property
				return sp.check_output(
					['xfconf-query', '-c', 'xfce-desktop', '-p', i]).decode('utf-8').strip()

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

	# TODO: way to get wallpaper for desktops which are commented-out below
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

		try:
			from gi.repository import Gio

			gsettings = Gio.Settings.new(SCHEMA)
			gsettings.set_string(KEY, uri)
		except ImportError:
			try:
				gsettings_proc = sp.Popen(
					['gsettings', 'set', SCHEMA, KEY, uri])
			except:  # MATE < 1.6
				sp.Popen(['mateconftool-2', '-t', 'string', '--set', '/desktop/mate/background/picture_filename', '%s' % image],
						 stdout=sp.PIPE)
			finally:
				gsettings_proc.communicate()

				if gsettings_proc.returncode != 0:
					sp.Popen(['mateconftool-2', '-t', 'string', '--set', '/desktop/mate/background/picture_filename', '%s' % image])

	elif desktop_env == 'gnome2':
		sp.Popen(
			['gconftool-2', '-t', 'string', '--set', '/desktop/gnome/background/picture_filename', image]
		)

	elif desktop_env == 'kde':
		# This probably only works in Plasma 5+

		kde_script = dedent(
		'''\
		var Desktops = desktops();
		for (i=0;i<Desktops.length;i++) {{
			d = Desktops[i];
			d.wallpaperPlugin = "org.kde.image";
			d.currentConfigGroup = Array("Wallpaper",
										"org.kde.image",
										"General");
			d.writeConfig("Image", "file://{}")
		}}
		''').format(image)

		sp.Popen(
				['dbus-send', '--session', '--dest=org.kde.plasmashell', '--type=method_call', '/PlasmaShell', 'org.kde.PlasmaShell.evaluateScript',
				 'string:{}'.format(kde_script)]
		)

	elif desktop_env in ['kde3', 'trinity']:
		args = ['dcop', 'kdesktop', 'KBackgroundIface', 'setWallpaper', '0', image, '6']
		sp.Popen(args)

	elif desktop_env == 'xfce4':
		# XFCE4's image property is not image-path but last-image (What?)

		list_of_properties = sp.check_output(['xfconf-query', '-R', '-l', '-c', 'xfce4-desktop', '-p', '/backdrop']
			).decode('utf-8').strip()

		for i in list_of_properties.split('\n'):
			if i.endswith('last-image'):
				# The property given is a background property
				sp.Popen(['xfconf-query', '-c', 'xfce4-desktop', '-p', i, '-s', image])

				sp.Popen(['xfdesktop', '--reload'])

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
			sp.Popen(args)
		except:
			pass # TODO: feh alts support

	elif desktop_env == 'icewm':
		args = ['icewmbg', image]
		sp.Popen(args)

	elif desktop_env == 'blackbox':
		args = ['bsetbg', '-full', image]
		sp.Popen(args)

	elif desktop_env == 'lxde':
		args = ['pcmanfm', '--set-wallpaper', image, '--wallpaper-mode=scaled']
		sp.Popen(args)

	elif desktop_env == 'lxqt':
		args = ['pcmanfm-qt', '--set-wallpaper', image, '--wallpaper-mode=scaled']
		sp.Popen(args)

	elif desktop_env == 'windowmaker':
		args = ['wmsetbg', '-s', '-u', image]
		sp.Popen(args)

	elif desktop_env == 'enlightenment':
		args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
		sp.Popen(args, shell=True)

	elif desktop_env == 'awesome':
		with sp.Popen("awesome-client", stdin=sp.PIPE) as awesome_client:
			command = ('local gears = require("gears"); for s = 1,'
						' screen.count() do gears.wallpaper.maximized'
						'("%s", s, true); end;') % image
			awesome_client.communicate(input=command.encode('utf-8'))

