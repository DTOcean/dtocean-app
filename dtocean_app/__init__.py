
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


def init_config():
    
    """Copy config files to user data directory"""
    
    objdir = ObjDirectory(__name__, "config")
    datadir = UserDataDirectory("dtocean_app", "DTOcean", "config")
    dirmap = DirectoryMap(datadir, objdir)
    
    dirmap.copy_file("logging.yaml")
    dirmap.copy_file("files.ini")
    
    return


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
    
    datadir = UserDataDirectory("dtocean_app", "DTOcean", "config")
    
    files_ini = ReadINI(datadir, "files.ini")
    files_config = files_ini.get_config()
    
    appdir_path = datadir.get_path("..")
    log_folder = files_config["logs"]["path"]
    log_path = os.path.join(appdir_path, log_folder)
    logdir = Directory(log_path)
    
    # Disable the logging QtHandler if the debug flag is set
    QtHandler.debug = debug
    
    log = Logger(datadir)
    log_config_dict = log.read()
    
    # Update the file logger if present
    if "file" in log_config_dict["handlers"]:
        log_filename = log_config_dict["handlers"]["file"]["filename"]
        log_path = logdir.get_path(log_filename)
        log_config_dict["handlers"]["file"]["filename"] = log_path
        logdir.makedir()
    
    log.configure_logger(log_config_dict)
    log.add_named_logger("dtocean_app",
                         info_message="Welcome to DTOcean")
    
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

