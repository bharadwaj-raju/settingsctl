# settingsctl

A cross-desktop (\*nix) tool to handle desktop settings.

See [the website](https://bharadwaj-raju.github.io/settingsctl/).

**Examples:**

	$ settingsctl get appearance.desktop.wallpaper
	/path/to/wallpaper

	$ settingsctl get power.screen-lock.enabled
	true

	$ settingsctl set power.screen-lock.timeout 20


Intended as a replacement for `xdg-settings` which is a [joke](#why-not-xdg-settings).


## Usage

`settingsctl [command] [setting] [--json]`

A "setting" here is a specific setting of the desktop.

`--json` causes the output to be in JSON format.

A "setting"'s format is `category.subcategory.option`

## Why not xdg-settings

1. It's not been updated since about 2011
2. It supports only *two* settings: default browser and URL scheme handler
3. It says "unknown desktop environment" when you use a non-XDG desktop (Awesome, i3 etc)

This project hopes to eventually *officially* replace the old `xdg-settings`.

