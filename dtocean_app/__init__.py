
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

from PyQt4 import QtGui, QtCore

from polite.paths import ObjDirectory, UserDataDirectory, DirectoryMap
from polite.configuration import Logger

from .utils.qtlog import QtHandler

module_path = os.path.realpath(__file__)

def start_logging(debug=False):

    # Configure logging
    objdir = ObjDirectory(__name__, "config")
    datadir = UserDataDirectory("dtocean_app", "DTOcean", "config")
    dirmap = DirectoryMap(datadir, objdir)
    
    # Disable the logging QtHandler if the debug flag is set
    QtHandler.debug = debug

    log = Logger(dirmap)
    log("dtocean_app", info_message="Welcome to DTOcean.")
    
    return

def main(debug=False):

    """Run the DTOcean tool"""
    
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
    
    epiStr = ('''Mathew Topper, Tecnalia (c) 2016.''')
              
    desStr = "Run the DTOcean GUI."

    parser = argparse.ArgumentParser(description=desStr,
                                     epilog=epiStr)

    parser.add_argument("--debug",
                        help=("disable stream redirection"),
                        action='store_true')
                                     
    args = parser.parse_args()
    debug = args.debug
        
    main(debug)

    return

