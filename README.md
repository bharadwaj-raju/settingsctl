# settingsctl

A cross-desktop (\*nix) tool to handle desktop settings.

**Examples:**

    $ settingsctl list desktop.monitors
	1

	$ settingsctl get desktop.monitors.1.wallpaper
	/path/to/wallpaper

	$ settingsctl get power.screen-lock.enabled
	true

	$ settingsctl set power.screen-lock.timeout 20

(All units in SI, so 5 → 5 seconds)

Intended as a replacement for `xdg-settings` which is a [joke](#why-not-xdg-settings).


## Usage

`settingsctl [set|get] [setting]`

`settingsctl` has three main commands: `get`, `set` and `list`.

A "setting" here is a specific setting of the desktop (see: [list of them](#settings-list)).

A "setting"'s format is `category.subcategory.option`

## Why not xdg-settings

1. It's not been updated since about 2011
2. It supports only *two* settings: default browser and URL scheme handler
3. It says "unknown desktop environment" when you use a non-XDG desktop (Awesome, i3 etc)

This project hopes to eventually *officially* replace the old `xdg-settings`.

