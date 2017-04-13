# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Add high DPI scaling widgets which activate when Windows virtual DPI exceeds
  100. Improves look and feel on high DPI displays.
- Split high low and shared QtDesigner files into separate directories.
- Added dynamic generation of tools menu from plugins created in the tools
  module.
- Added constraints plot tool.
- Allow filtering of database when only sites or only devices are defined.
- Add test for opening main window. Requires pytest-qt and pytest-mock.
- Add tests for scenario activation upto and including pipeline activation
  without a database connected.
- Add change log.

### Changed

- Changed dtocean-qt dependency to 0.9.1.
- Updated README.
- Removed "schema" from database configuration dialog.

### Fixed

- Fix bug in InputTriStateTable widget that stopped input of Observed Receptors
  variable in environmental assessment theme.
- Fix issue with displaying PointList data (such as the user defined array
  layout) when z-coordinates are not set.


## [1.0.0] - 2017-02-23

### Added

- Initial import of dtocean-gui from SETIS.

### Changed

- Changed package name to dtocean-app.
- Changed pandas-qt dependency to dtocean-qt.

