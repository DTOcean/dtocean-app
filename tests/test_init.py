# -*- coding: utf-8 -*-

#    Copyright (C) 2016-2018 Mathew Topper
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

import logging
import warnings

from polite.paths import Directory
from dtocean_app import warn_with_traceback, start_logging
from dtocean_app.utils.config import init_config


def test_warn_with_traceback():
    
    warnings.showwarning = warn_with_traceback
    warnings.warn("Test warning")
    
    assert True

def test_start_logging(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)

    start_logging()
    
    logdir = config_tmpdir.join("..", "logs")
    
    assert len(logdir.listdir()) == 1


def test_start_logging_twice(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)

    start_logging()
    logging.shutdown()
    start_logging()
    
    logdir = config_tmpdir.join("..", "logs")
    
    assert len(logdir.listdir()) == 2


def test_start_logging_debug(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)

    start_logging(debug=True)
    
    logdir = config_tmpdir.join("..", "logs")
    
    assert len(logdir.listdir()) == 1


def test_start_logging_user(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.utils.config.UserDataDirectory',
                 return_value=mock_dir)
    
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(logging=True, files=True)
    
    # This will raise if the logging file is not in the user directory
    mocker.patch('dtocean_app.ObjDirectory',
                 return_value=None)
    
    start_logging()
    
    logdir = config_tmpdir.join("..", "logs")
    
    assert len(logdir.listdir()) == 1
