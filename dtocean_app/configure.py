# -*- coding: utf-8 -*-

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

"""
"""

# Helpers for configuration files
from polite.paths import SiteDataDirectory, UserDataDirectory
from polite.configuration import ReadINI


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

