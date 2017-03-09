# settingsctl

Different desktop environments on \*nix usually have different configuration methods for the same setting.
This makes it hard for developers to handle desktop settings in their program.

settingsctl is a cross-desktop (\*nix) tool to handle desktop settings.

This was *also* the aim of `xdg-settings`. [But xdg-settings doesn't really work](#why-not-xdg-settings).

For more information (and the documentation) see [the website](web).


## Getting started

Ensure you have [Python 3](python). You should probably already have it!

1. Download settingsctl [here (zip)](zip-dl)

2. Either:
	a. Install settingsctl system-wide (`sudo sh install.sh`)
	b. Or just run it (`./settingsctl --help`)

### Examples:

	$ settingsctl get appearance.desktop.wallpaper
	/path/to/wallpaper

	$ settingsctl get power.screen-lock.enabled
	true

	$ settingsctl set power.screen-lock.timeout 20


## Features

- Support for nearly every setting you may find in a desktop environment's settings.
- Support for nearly every desktop environment (Yours isn't? [File an issue!](new-issue))
- Support for JSON output format for easy parsing
- Extensive [documentation](docs)


## Contributing

(Quality) Contributions are always welcome. Here you will find how to go about contributing to this project.

Firstly, the language: settingsctl is written in Python 3.

The coding conventions are mainly [PEP8](pep8), but with one notable exception: Tabs are used instead of spaces.

### Contributing a setting

1. Fork the repository.

2. See [Documentation::Creating a Setting](docs-create-setting).

3. Then [file a pull request](file-pr) for your change.

### Contributing to the settingsctl command itself

1. Fork the repository.

2. Look through the code (file: `settingsctl`).

3. Then [file a pull request](new-pr) for your change.


## License

settingsctl is licensed under the GNU General Public License (GPL) version 3 (or, at your option, a later version).

settingsctl is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

For the license text, see the included LICENSE file.


## Why not xdg-settings

1. It's not been updated since about 2011
2. It supports only *two* settings: default browser and URL scheme handler

This project hopes to eventually *officially* (as in approved by XDG as a standard) replace the old `xdg-settings`.

[web]: https://bharadwaj-raju.github.io/settingsctl/
[docs]: https://bharadwaj-raju.github.io/settingsctl/documentation/
[pep8]: https://pep8.org
[new-issue]: https://github.com/bharadwaj-raju/settingsctl/issues/new
[new-pr]: https://github.com/bharadwaj-raju/settingsctl/compare
[python]: https://python.org
[zip-dl]: https://github.com/bharadwaj-raju/settingsctl/archive/master.zip
[docs-settingsctl]: https://bharadwaj-raju.github.io/settingsctl/documentation/developing-settingsctl.html
[docs-create-setting]: https://bharadwaj-raju.github.io/settingsctl/documentation/creating-a-setting.html


