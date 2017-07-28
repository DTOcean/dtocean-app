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
- Add tests for scenario activation up to and including pipeline activation
  without a database connected.
- Add DateTimeDict structure and set up output widget.
- Add input and output widgets for SimpleDictColumn.
- Added ScientificDoubleSpinBox widget to allow scientific notation for floats.
- Created static version of Ui_FloatSelect (called Ui_ScientificSelect) which
  uses ScientificDoubleSpinBox.
- Added configuration file for setting the location of logs using the files.ini
  configuration file (found in User\AppData\Roaming\DTOcean\dtocean_app\config
  folder).
- Added configuration file generator called dtocean-app-config which copies
  the default configuration to the
  User\AppData\Roaming\DTOcean\dtocean_app\config folder.
- Added save file robustness compatibility with dtocean-core.
- Add widgets for CartesianListColumn structure.
- Added Alt key shortcuts to menus.
- Added Export and Import actions to the Data menu to create and load datastate
  files. These save the data in the active datastate and can be reused in any
  project.
- Allow text to be selected in variable details widget.

### Changed

- Changed dtocean-qt dependency to 0.9.1.
- Updated README.
- Removed "schema" from database configuration dialog.
- Hide input variables labelled as overwritten and output variables labelled
  as unavailable or overwritten.
- Move ListWidget ui file to shared directory and add specific unit label.
- FloatSelect widget now subclasses Ui_ScientificSelect.
- Using default configuration files in source code unless a user configuration
  is found.
- Changed timed rotating file logger for a standard rotating file logger that
  is rolled over at the beginning of each session.

### Fixed

- Fix bug in InputTriStateTable widget that stopped input of Observed Receptors
  variable in environmental assessment theme.
- Fix issue with displaying PointList data (such as the user defined array
  layout) when z-coordinates are not set.
- Fixed issue with missing data in IndexTable and SimpleDict widgets.
- Correctly, order columns of DatetimeDict output widget.


### Removed

- Removed floatselect.ui as the widget is now built inside the package.


## [1.0.0] - 2017-02-23

### Added

- Initial import of dtocean-gui from SETIS.

### Changed

- Changed package name to dtocean-app.
- Changed pandas-qt dependency to dtocean-qt.

