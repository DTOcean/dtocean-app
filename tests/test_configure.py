
from polite.paths import Directory
from dtocean_app import (init_config,
                         init_config_parser,
                         init_config_interface,
                         start_logging)
from dtocean_app.configure import get_install_paths


def test_init_config(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config()
        
    assert len(config_tmpdir.listdir()) == 2
              
    init_config()
    
    assert len(config_tmpdir.listdir()) == 4
              

def test_init_config_overwrite(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config()
        
    assert len(config_tmpdir.listdir()) == 2
              
    init_config(overwrite=True)
    
    assert len(config_tmpdir.listdir()) == 2
              
              
def test_init_config_install(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(install=True)
        
    assert len(config_tmpdir.listdir()) == 3

    
def test_init_config_parser():
    
    install, overwrite = init_config_parser([])
    
    assert not overwrite
    assert not install


def test_init_config_parser_overwrite():
    
    install, overwrite = init_config_parser(["--overwrite"])
    
    assert overwrite
    assert not install
    
    
def test_init_config_parser_install():
    
    install, overwrite = init_config_parser(["--install"])
    
    assert not overwrite
    assert install
    
    
def test_init_config_interface(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
    mocker.patch('dtocean_app.init_config_parser',
                 return_value=(False, False))
                 
    init_config_interface()
        
    assert len(config_tmpdir.listdir()) == 2

    
def test_start_logging(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)

    start_logging()
    
    assert True
    
    
def test_start_logging_debug(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)

    start_logging(debug=True)
    
    assert True


def test_start_logging_user(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config()
    
    mocker.patch('dtocean_app.ObjDirectory',
                 return_value=None)
    
    start_logging()
    
    assert True
    

def test_get_install_paths(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(install=True)
    
    mocker.patch('dtocean_app.configure.UserDataDirectory',
                 return_value=mock_dir)
                 
    test_dict = get_install_paths()
    
    assert "man_user_path" in test_dict
