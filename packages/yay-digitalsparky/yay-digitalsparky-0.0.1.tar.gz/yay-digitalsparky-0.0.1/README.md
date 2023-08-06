# python-yay

Simple Python interface to Arch Linux 'yay' package management interface

### Examples

* Refresh master package list: `yay.refresh()`
* Install a package: `yay.install("php")`
* Remove a package: `yay.remove("php", purge=True)`
* Upgrade all packages: `yay.upgrade()`
* List all installed packages: `yay.get_installed()` (returns dict of id, version, upgradable status)
* List all available packages: `yay.get_available()` (returns dict of id, version, repo name)
* Get info for a package: `yay.get_info("php")` (returns dict, info labels as keys)
* Get uninstalled dependencies of a package: `yay.needs_for("php")` (returns list of package names)
* Get installed packages that depend on this one: `yay.depends_for("php")` (returns list of package names)
* Check if a package is installed: `yay.is_installed("php")` (returns bool)

All functions that allow a package name as parameter (except `get_info`) will accept either a single package name or a list of multiple names.
