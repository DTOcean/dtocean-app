# GUI

## Installation

### pyqt

There is a bug in the anaconda pyrcc4.bat file (look in the Scripts directory of your environment) and you have to change the contents of it to:

```
@echo off

"%~dp0\..\Library\bin\pyrcc4" %*
```

### polite

```
cd \path\to\polite
winmake.bat install
```

### Anaconda

```
conda install pandas-qt pyqt=4.11.4
```

### dtocean-gui

```
cd \path\to\dtocean-gui
winmake.bat bootstrap
```

## Running

```
dtocean-gui
```

## Icons

Crystal Clear (LPGL)
GNOME (GPL)
ScreenRuler Tango (GPL)
