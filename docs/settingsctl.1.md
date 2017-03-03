settingsctl(1) -- cross-desktop settings tool
=============================================

## SYNOPSIS

`settingsctl` <set> setting value
`settingsctl` <get> setting
`settingsctl` <list>
`settingsctl` <tree> [<setting>, <--maxdepth>]

## DESCRIPTION

settingsctl is intended to be a tool to set desktop settings on most \*nix
desktops.

It supports a wide variety of settings one would commonly find in a desktop's
settings manager, configuration file or similar.

It stays out of system-wide settings.

## SYNTAX

The syntax is `settingsctl` <command> [<arguments>, ...]

See [SYNOPSIS][].

## ENVIRONMENT

* `SETTINGSCTL_LIB`
  The path to the settings definition files is usually `/usr/lib/settingsctl`,
  or `lib/` in settingsctl's working directory. This can be overridden with the
  environment variable `SETTINGSCTL_LIB`, which should specify a path to a
  directory.

* `XDG_CURRENT_DESKTOP`
  Identifies the desktop environment/window manager/etc to settingsctl.
  This is usually automatically set by your desktop environment/window manager/etc

## RETURN VALUES

* `0`
  No error.

* `1`
  A settingsctl was not specified/invalid.

* `2`
  Error in executing the operation. Details on the error are printed to stdout
  or stderr.






