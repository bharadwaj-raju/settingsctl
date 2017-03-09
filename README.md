# settingsctl

Different desktop environments on \*nix usually have different configuration methods for the same setting.
This makes it hard for developers to handle desktop settings in their program.

settingsctl is a cross-desktop (\*nix) tool to handle desktop settings.

This was *also* the aim of `xdg-settings`. [But xdg-settings doesn't really work](#why-not-xdg-settings).

For more information (and the documentation) see [the website](https://bharadwaj-raju.github.io/settingsctl).


## Getting started

Ensure you have [Python 3](https://python.org). You should probably already have it!

1. Download settingsctl [here (zip)](https://github.com/bharadwaj-raju/settingsctl/archive/master.zip)

2. Either:
	1. Install settingsctl system-wide (`sudo sh install.sh`)
	2. Or just run it (`./settingsctl --help`)

### Examples:

	$ settingsctl get appearance.desktop.wallpaper
	/path/to/wallpaper

	$ settingsctl get power.screen-lock.enabled
	true

	$ settingsctl set power.screen-lock.timeout 20


## Features

- Support for nearly every setting you may find in a desktop environment's settings.
- Support for nearly every desktop environment (Yours isn't supported? [File an issue!](https://github.com/bharadwaj-raju/settingsctl/issues/new))
- Support for JSON output format for easy parsing
- Extensive [documentation](https://bharadwaj-raju.github.io/settingsctl/documentation)


## Contributing

(Quality) Contributions are always welcome. Here you will find how to go about contributing to this project.

Firstly, the language: settingsctl is written in Python 3.

The coding conventions are mainly [PEP8](http://pep8.org), but with one notable exception: Tabs are used instead of spaces.

### Contributing a setting

1. Fork the repository.

2. See [Documentation::Creating a Setting](https://bharadwaj-raju.github.io/settingsctl/documentation/creating-a-setting.html).

3. Then [file a pull request](file-pr) for your change.

### Contributing to the settingsctl command itself

1. Fork the repository.

2. Look through the code (file: `settingsctl`).

3. Then [file a pull request](https://github.com/bharadwaj-raju/settingsctl/compare) for your change.


## License

settingsctl is licensed under the GNU General Public License (GPL) version 3 (or, at your option, a later version).

settingsctl is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

For the license text, see the included LICENSE file.


## Why not xdg-settings

1. It's not been updated since about 2011
2. It supports only *two* settings: default browser and URL scheme handler

This project hopes to eventually *officially* (as in approved by XDG as a standard) replace the old `xdg-settings`.
