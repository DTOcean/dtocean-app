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

Note the database requires a PostgresSQL server to be installed on the local
machine and full instructions are provided within the download.

With the current (1.0.0) version of the installer some user have reported
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
distribution. A prerequist of this is installation of Anaconda Python for Python
version 2.7. Additionally, if the full system has not been installed previously
using the process described in the [Windows Installer](#windows-installer)
section, the supplementary data pacakage must be installed. The current version
of the data pacakage can be downloaded from
[SETIS](https://setis.ec.europa.eu/dt-ocean/download/file/fid/88).

Once the above prerequists are installed, it is recommended to install and
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


#### Run the application

```
activate _dtocean
dtocean-app
```

It is assumed that the _dtocean environment has not been previously activated.
If dtocean-app is not started try running in debug mode:

```
dtocean-app --debug
```

### Manual Install

Although not supported, it is possible to install the DTOcean packages outside
of the Anaconda development environment.

#### Dependencies

The full list of dependencies 
(copied from the output of the Anaconda install) is:

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
a Windows Command Prompt in as follows:

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
