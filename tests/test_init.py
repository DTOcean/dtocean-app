# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:16:37 2017

@author: mtopper
"""

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
