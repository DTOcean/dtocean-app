# DTOcean Graphical Application

## Introduction

This repository contains the main graphical application of the DTOcean software
suite. The code contained in this package relates only to the Qt4 GUI
representation of the system. All underlying logic can be found in the
dtocean-core package and the related dtocean-* modules and themes. The only
unique dependency for this package is dtocean-qt which contains helper functions
for PyQt.

This package can be used as a basis for development of the DTOcean system by
following the installation and development instructions given below. Submissions
to the official DTOcean repositories should follow the instructions given
in the following blog post:

[INSERT BLOG POST LINK HERE]

## Installation

The DTOcean suite can be installed using three methods as follows:

1. Windows Installer: The latest major.minor release can be downloaded from
   [SETIS][1].
2. Anaconda Package: The latest major.minor.micro release is packaged for the
   [Anaconda Python][2] distribution.
3. Manual installation using setuptools.

Each of these installation methods will be described in the sections below.

### Windows Installer

A Microsoft Windows installer is available for installation from the [SETIS][1]
website. Generally, this installer will provide the latest major.minor version
of the DTOcean tool. The installer will contain any supplementary data that
is not stored within the source control repositories but does not automatically
install the examples database or the manuals. These must be downloaded and
installed separately:

* [Database](https://setis.ec.europa.eu/dt-ocean/download/file/fid/85)
* [Manuals](https://setis.ec.europa.eu/dt-ocean/download/file/fid/82)

Note the database requires a PostgreSQL server to be installed on the local
machine and full instructions are provided within the download.

With the current (1.0.0) version of the installer some users have reported
problems related to the installation directory not being found. A temporary
workaround for this issue is described in the following blog post:

[DTOcean Installation Solution](http://www.dataonlygreater.com/latest/professional/2017/02/15/dtocean-installation-solution/)

Other known issues with the current installer version can be found on the
[Any Asked Questions](https://dtocean.github.io/#aqa) page or the 
[dtocean-issues](https://github.com/DTOcean/dtocean-issues) repository. If
you can't find your issue in the closed or open issues then the developers would
strongly encourage you to create a new issue.

### Anaconda Package

The DTOcean application can be installed easily using the [Anaconda Python][2]
distribution. A prerequisite is installation of the Anaconda distribution for Python
version 2.7. Additionally, if the full system has not been installed previously
using the process described in the [Windows Installer](#windows-installer)
section, the supplementary data package must be installed. The current version
of the data package can be downloaded from
[SETIS](https://setis.ec.europa.eu/dt-ocean/download/file/fid/88).

If desired, the example database must also be downloaded and installed
separately:

* [Database](https://setis.ec.europa.eu/dt-ocean/download/file/fid/85)

Note the database requires a PostgreSQL server to be installed on the local
machine and full instructions are provided within the download.

Installation of the DTOcean manuals is not currently supported through this
method but will be included in the near future.

Once the above prerequisites are installed, it is recommended to install and
run DTOcean from an "environment". The process, using a Windows Command Prompt
window, is as follows.

#### Add Anaconda Cloud Channels (First Time Only)

```
conda config --append channels conda_forge
conda config --append channels dataonlygreater
```

These channels provide the DTOcean packages and their dependencies.

#### Create an Environment (First Time Only)

```
conda create -n _dtocean
```

Follow the prompts and press enter as required. The underscore in the
environment name prevents start menu links being created for this environment.

#### Install DTOcean (First Time Only)

```
activate _dtocean
conda install dtocean-app
```

Follow the prompts and press enter as required. It is assumed that the
_dtocean environment has not been previously activated.

#### Run the application (Anaconda)

```
activate _dtocean
dtocean-app
```

It is assumed that the _dtocean environment has not been previously activated.
If dtocean-app is not started try running in debug mode:

```
dtocean-app --debug
```

### Installing from Source

Although not supported, it is possible to install the DTOcean packages without
use of the Anaconda development environment directly from the source code.

#### Dependencies

The full list of dependencies  (copied from the output of the Anaconda install)
is:

* aneris
* attrdict
* basemap
* cma
* configobj
* cycler
* decorator
* descartes
* dtocean-core
* dtocean-economics
* dtocean-electrical
* dtocean-environment
* dtocean-hydrodynamics
* dtocean-installation
* dtocean-logistics
* dtocean-maintenance
* dtocean-moorings
* dtocean-qt
* dtocean-reliability
* easygui
* et_xmlfile
* geoalchemy2
* geopy
* geos
* h5py
* hdf5
* jdcal
* jpeg
* libpng
* libpq
* libpython
* libtiff
* matplotlib
* mingw
* mkl
* netcdf4
* networkx
* numpy
* openpyxl
* openssl
* pandas
* pil
* polite
* psycopg2
* pyopengl
* pyparsing
* pypower
* pyproj
* pyqt
* python-dateutil
* python
* pytest
* pytz
* pywin32
* pyyaml
* qt
* scikit-learn
* scipy
* setuptools
* shapely
* sip
* six
* sqlalchemy
* tk
* utm
* vc
* xarray
* xlrd
* xlwt
* zlib

#### Installation

Once all the dependencies are installed this package can be installed from
a Windows Command Prompt as follows:

```
cd \path\to\dtocean-app
python setup.py bootstrap
python setup.py install
```

The bootstrap command converts the QtDesigner files found in the "designer"
directory into PyQt source code and places them within the package.

#### Testing

The package comes with a small pytest test suite. Following installation of
pytest, the test suite can be run using:

```
cd \path\to\dtocean-app
py.test tests
```

#### Shortcuts

A batch script is provided within the source code to shortcut the installation
and testing process. It can be run as follows:

```
cd \path\to\dtocean-app
winmake.bat bootstrap
```

The script can also be used to run the tests without installation:

```
cd \path\to\dtocean-app
winmake.bat test
```

Or to skip the bootstrap stage:

```
cd \path\to\dtocean-app
winmake.bat install
```

The above commands are also useful when developing the package.

#### PyQt Bug

If the bootstrap command fails, it could be due to a bug in the pyrcc4.bat file.

For the Anaconda python distribution, this file can be found in the "Scripts"
directory of your environment. You have to change the contents of it to:

```
@echo off

"%~dp0\..\Library\bin\pyrcc4" %*
```

## Development

It is recommended to conduct development of dtocean-app or another dtocean-*
package using the Anaconda installation technique described in the
[Anaconda Package](#anaconda-package) section. This will pull all of the
prerequisite dependencies so that the developer need only replace the package
they wish to develop with a local version. The main application can then
be run using the instructions in the
[Run the application (Anaconda)](#run-the-application-\(anaconda\)) section
using the updated code.

### Package Uninstall

The process to remove a dtocean package installed using Anaconda is as follows:

```
activate _dtocean
conda remove --force dtocean-*
```

Here dtocean-* refers to whichever dtocean package is (or packages are) being
developed and the "force" flag allows the package to be removed without also
removing the upstream dependencies. This is important if a package that is
a direct or indirect dependency of dtocean-app is being changed as Anaconda will
want to remove it if the flag is not provided.

If developing without Anaconda, the "pip" package manager can be used to
remove a package as follows:

```
pip uninstall dtocean-*
```

### Development Version Install

A development version of a package can be installed as a "live" version.  This
approach will allow the immediate impact of any code change to be examined
within the overall DTOcean application. To install the live package we use the 
"pip" package manager.

Firstly, activate your environment, if not active already:

```
activate _dtocean
```

If "pip" is not already installed, install it using conda:

```
conda install pip
```

Then, to install the development version of the package do:

```
pip install -e \path\to\dtocean-*
```

### QtDesigner Files Bootstrapping

For some packages, including dtocean-app, another installation stage is required
which is called a "bootstrap" stage. The bootstrap stage is only required where
some external (non-python) files are translated into source code, prior to
installation. In the case of dtocean-app "ui" files from QtDesigner are
translated into PyQt code for drawing widgets.

To carry out the bootstrapping stage type:

```
cd \path\to\dtocean-app
python setup.py bootstrap
```

This bootstrapping stage is only required on first installation or if the files
in the "designer" folder have changed or if new files have been added or
deleted. The converted files are placed into the dtocean_app\designer folder
from where they can be imported for use in other parts of the code.

Note, only the __init__.py file should ever be under version control in the
dtocean_app\designer folder.

Please be aware of the potential [PyQt Bug](#pyQt-bug) for which a solution is
described above.

### Manual Testing

Testing is an important part of development and a mix of manual and automated
testing is used within DTOcean. The most basic test for dtocean-app or changes
to its dependencies is to attempt to start the application with the development
package installed. 

First, ensure that the Anaconda environment is active:

```
activate _dtocean
```

The application is then started in the usual manner:

```
dtocean-app
```

If the application fails to start but not output is produced, try running in
debug mode:

```
dtocean-app --debug
```

### Automated Testing

A small automated test suite is provided with dtocean-app. This test suite is
written using the [pytest](http://doc.pytest.org/en/latest/) framework and the
tests for dtocean-app are found in the "tests" directory.

To run the tests, remember to start the environment if not already active:

```
activate _dtocean
```

Also, ensure that pytest is installed:

```
conda install pytest
```

The test suite can then be activated in two ways. Firstly, it can be invoked
directly from the py.test command as follows:

```
cd \path\to\dtocean-app
py.test tests
```

Alternatively the "winmake.bat" shortcut script can be used to invoke the
tests:

```
cd \path\to\dtocean-app
winmake.bat test
```

Developers are encouraged to ensure all tests pass before submitting code to
the official repositories. They are also encouraged to
develop new automated tests for code that is changed or added. Code that is
failing tests should not be submitted for inclusion in the official
repositories.

### Contributing

The process and ethos for contributing to the official DTOcean repositories is
detailed in the following blog post:

[INSERT BLOG POST HERE]

## Licences

### Software

DTOcean is open source software. Please see the LICENCE.txt file for the full
text of the software licence.

### Icons

The icons used with the graphical interface are source directly or derived from
the following open source icon sets:

* Crystal Clear (LPGL)
* GNOME (GPL)
* ScreenRuler Tango (GPL)

[1]: https://setis.ec.europa.eu/dt-ocean/
[2]: https://www.continuum.io/anaconda-overview
