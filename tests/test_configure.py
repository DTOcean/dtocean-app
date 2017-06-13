
from polite.paths import Directory
from dtocean_app import init_config, start_logging


def test_init_config(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config()
        
    assert len(config_tmpdir.listdir()) == 2

    
def test_start_logging():

    start_logging(True)
    
    assert True
