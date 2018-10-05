
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

import sys
import argparse

from polite.configuration import ReadINI
from polite.paths import (DirectoryMap,
                          ObjDirectory,
                          SiteDataDirectory,
                          UserDataDirectory)


def get_install_paths():
    
    """Pick the necessary paths to configure the external files for the 
    manuals."""
    
    install_config_name = "install.ini"
    
    user_data = UserDataDirectory("dtocean_doc", "DTOcean", "config")
    user_ini_reader = ReadINI(user_data, install_config_name)
    
    # Get the root path from the site data path.
    site_data = SiteDataDirectory("DTOcean Manuals", "DTOcean")
    site_ini_reader = ReadINI(site_data, install_config_name)
    
    if user_ini_reader.config_exists():
        config = user_ini_reader.get_config()
    elif site_ini_reader.config_exists():
        config = site_ini_reader.get_config()
    else:
        return None
                 
    path_dict = {"man_user_path": config["man"]["user_path"],
                 "man_technical_path": config["man"]["technical_path"]}

    return path_dict


def init_config(logging=False, files=False, install=False, overwrite=False):
    
    """Copy config files to user data directory"""
    
    if not any([logging, files, install]): return
    
    objdir = ObjDirectory(__name__, "..", "config")
    datadir = UserDataDirectory("dtocean_app", "DTOcean", "config")
    dirmap = DirectoryMap(datadir, objdir)
    
    if logging: dirmap.copy_file("logging.yaml", overwrite=overwrite)
    if files: dirmap.copy_file("files.ini", overwrite=overwrite)
    if install: dirmap.copy_file("install.ini", overwrite=overwrite)
    
    return datadir.get_path()


def init_config_parser(args):
    
    '''Command line parser for init_config.
    
    Example:
    
        To get help::
        
            $ dtocean-app-config -h
            
    '''
    
    epiStr = ('Mathew Topper (c) 2017.')
              
    desStr = ("Copy user modifiable configuration files to "
              "<UserName>\AppData\Roaming\DTOcean\dtocean-app\config")

    parser = argparse.ArgumentParser(description=desStr,
                                     epilog=epiStr)
    
    parser.add_argument("--logging",
                        help=("copy logging configuration"),
                        action="store_true")
    
    parser.add_argument("--files",
                        help=("copy log file location configuration"),
                        action="store_true")
    
    parser.add_argument("--install",
                        help=("copy manuals installation path configuration"),
                        action="store_true")
    
    parser.add_argument("--overwrite",
                        help=("overwrite existing configuration files"),
                        action="store_true")
                        
    args = parser.parse_args(args)

    logging = args.logging
    files = args.files
    install = args.install
    overwrite = args.overwrite
    
    return logging, files, install, overwrite


def init_config_interface():
    
    '''Command line interface for init_config.'''
    
    logging, files, install, overwrite = init_config_parser(sys.argv[1:])
    dir_path = init_config(logging=logging,
                           files=files,
                           install=install,
                           overwrite=overwrite)
    
    if dir_path is not None:
        print "Copying configuration files to {}".format(dir_path)

    return
