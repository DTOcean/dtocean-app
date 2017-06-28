
#    Copyright (C) 2016 Mathew Topper, Rui Duarte
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
import warnings
import traceback

from PyQt4 import QtGui, QtCore

from polite.configuration import ReadINI
from polite.paths import (Directory,
                          ObjDirectory,
                          UserDataDirectory,
                          DirectoryMap)
from polite.configuration import Logger

from .utils.qtlog import QtHandler

module_path = os.path.realpath(__file__)


def warn_with_traceback(message,
                        category,
                        filename,
                        lineno,
                        file=None,
                        line=None):

    log = file if hasattr(file,'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message,
                                     category,
                                     filename,
                                     lineno,
                                     line))
    
    return


def start_logging(debug=False):
    
    # Pick up the configuration from the user directory if it exists
    userdir = UserDataDirectory("dtocean_app", "DTOcean", "config")
            
    if userdir.isfile("files.ini") and userdir.isfile("logging.yaml"):
        configdir = userdir
    else:
        configdir = ObjDirectory("dtocean_app", "config")
    
    files_ini = ReadINI(configdir, "files.ini")
    files_config = files_ini.get_config()
    
    appdir_path = userdir.get_path("..")
    log_folder = files_config["logs"]["path"]
    log_path = os.path.join(appdir_path, log_folder)
    logdir = Directory(log_path)
    
    # Disable the logging QtHandler if the debug flag is set
    QtHandler.debug = debug
    
    log = Logger(configdir)
    log_config_dict = log.read()
    
    # Update the file logger if present
    if "file" in log_config_dict["handlers"]:
        log_filename = log_config_dict["handlers"]["file"]["filename"]
        log_path = logdir.get_path(log_filename)
        log_config_dict["handlers"]["file"]["filename"] = log_path
        logdir.makedir()
    
    log.configure_logger(log_config_dict)
    logger = log.add_named_logger("dtocean_app",
                                  info_message="Welcome to DTOcean")
    
    # Rotate any rotating file handlers
    for handler in logger.handlers:
        if handler.__class__.__name__ == 'RotatingFileHandler':
            handler.doRollover()
    
    return


def init_config(install=False, overwrite=False):
    
    """Copy config files to user data directory"""
    
    objdir = ObjDirectory(__name__, "config")
    datadir = UserDataDirectory("dtocean_app", "DTOcean", "config")
    dirmap = DirectoryMap(datadir, objdir)
    
    dirmap.copy_file("logging.yaml", overwrite=overwrite)
    dirmap.copy_file("files.ini", overwrite=overwrite)
    
    # Copy the manuals installation configuration
    if install:
        dirmap.copy_file("install.ini", overwrite=overwrite)
    
    return


def init_config_parser(args):
    
    '''Command line parser for init_config.
    
    Example:
    
        To get help::
        
            $ dtocean-app-config -h
            
    '''
    
    epiStr = ('Mathew Topper (c) 2017.')
              
    desStr = ("Copy user modifiable configuration files to "
              "User\AppData\Roaming\DTOcean\dtocean-app\config")

    parser = argparse.ArgumentParser(description=desStr,
                                     epilog=epiStr)

    parser.add_argument("--install",
                        help=("add path configuration for manuals"),
                        action="store_true")

    parser.add_argument("--overwrite",
                        help=("overwrite any existing configuration files"),
                        action="store_true")
                        
    args = parser.parse_args(args)

    install = args.install
    overwrite = args.overwrite
    
    return install, overwrite


def init_config_interface():
    
    '''Command line interface for init_config.'''
    
    install, overwrite = init_config_parser(sys.argv[1:])
    dir_path = init_config(install=install, overwrite=overwrite)
    print "Copying configuration files to {}".format(dir_path)

    return


def main(debug=False, trace_warnings=False):

    """Run the DTOcean tool"""
    
    # Add traces to warnings
    if trace_warnings: warnings.showwarning = warn_with_traceback
    
    # Bring up the logger
    start_logging(debug)

    # Build the main app
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
    splash_path = os.path.join(module_path, '..', 'splash_loading.png')
    splash_pix = QtGui.QPixmap(splash_path)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    from .main import DTOceanWindow, Shell

    shell = Shell()

    main_window = DTOceanWindow(shell, debug)
    main_window.show()
    splash.finish(main_window)

    sys.exit(app.exec_())
    
    return


def gui_interface():

    '''Command line interface for dtocean-app.
    
    Example:
    
        For help::
        
            $ dtocean-app --help
            
    '''
    
    epiStr = ('''Mathew Topper, Tecnalia (c) 2017.''')
              
    desStr = "Run the DTOcean graphical application."

    parser = argparse.ArgumentParser(description=desStr,
                                     epilog=epiStr)

    parser.add_argument("--debug",
                        help=("disable stream redirection"),
                        action='store_true')
    
    parser.add_argument("--trace-warnings",
                        help=("add stack trace to warnings"),
                        action='store_true')
                                     
    args = parser.parse_args()
    debug = args.debug
    trace_warnings = args.trace_warnings
        
    main(debug=debug, trace_warnings=trace_warnings)

    return

