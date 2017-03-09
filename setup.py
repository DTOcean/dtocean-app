# -*- coding: utf-8 -*-

import os
import sys
import glob

from setuptools import Command, find_packages, setup
from setuptools.command.test import test as TestCommand
      
class Bootstrap(Command):
    
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        
        # Convert all UI files to py files
        ui_search_path = os.path.join("designer", "*.ui")
        dst_dir = os.path.join("dtocean_app", "designer")
        
        for ui_path in glob.glob(ui_search_path):
            
            _, file_name = os.path.split(ui_path)
            file_root, _ = os.path.splitext(file_name)  
            dst_path = os.path.join(dst_dir, file_root + ".py")
            
            sys_command = "pyuic4 -o {} {}".format(dst_path, ui_path)
            
            # Convert the files
            print "create ui file: {}".format(dst_path)
            os.system(sys_command)
            
        # Convert all QRC files to py files
        ui_search_path = os.path.join("designer", "*.qrc")
        dst_dir = os.path.join("dtocean_app", "designer")
        
        for ui_path in glob.glob(ui_search_path):
            
            _, file_name = os.path.split(ui_path)
            file_root, _ = os.path.splitext(file_name)  
            dst_path = os.path.join(dst_dir, file_root + "_rc.py")
            
            sys_command = "pyrcc4 -o {} {}".format(dst_path, ui_path)
            
            # Convert the files
            print "create resource file: {}".format(dst_path)
            os.system(sys_command)

        return

        
class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)
        

class CleanTest(Command):

    description = 'clean test files'
    user_options = []
     
    def initialize_options(self):
        pass
     
    def finalize_options(self):
        pass
     
    def run(self):
        clean = Cleaner("test files",
                        ['.pyc', '.pkl'])
        clean()
 
        
class Cleaner(object):
     
    def __init__(self, description='some files',
                       clean_list=None,
                       exclude_list=None
                       ):
        
        if clean_list is None: clean_list = []
        if exclude_list is None: exclude_list = ['.eggs',
                                                 '.git',
                                                 '.idea',
                                                 '.hg',
                                                 '__pycache__',
                                                 'test_data']
        
        self.description = description
        self.clean_list = clean_list
        self.exclude_list = exclude_list
     
    def is_exclude(self, path):
        for item in self.exclude_list:
            if path.find(item) != -1:
                return True
        return False
     
    def is_clean(self, path):
        return path.endswith(tuple(self.clean_list))
     
    def pickup_clean(self):
        for root, dirs, files in os.walk(os.getcwd()):
            if self.is_exclude(root):
                continue
            for fname in files:
                if not self.is_clean(fname):
                    continue
                yield os.path.join(root, fname)
                
    def __call__(self):
        print "start clean {}".format(self.description)
        for clean_path in self.pickup_clean():
            print "remove {}: {}".format(os.path.splitext(clean_path)[1],
                                         clean_path)
            os.remove(clean_path)
        print "end cleanup"


setup(name='dtocean-app',
      version='1.0.2',
      description='Main application for the DTOcean tools',
      author='Mathew Topper, Rui Duarte',
      author_email=('damm_horse@yahoo.co.uk, '
                    'Rui.Duarte@france-energies-marines.org'),
      license="GPLv3",
      packages=find_packages(),
      install_requires=[
           'dtocean-core>=1.0',
           'matplotlib',
           'numpy',
           'pandas',
           'dtocean-qt>=0.9.1',
           'pil',
           'polite>=0.9',
          # 'sip',
          # 'PyQt4',
      ],
      entry_points={
          'console_scripts':
              [
               'dtocean-app = dtocean_app:gui_interface',
               ]},
      package_data={'': ['*.png', 'test_images/*.png'],
                    'dtocean_app': ['config/*.ini',
                                    'config/*.yaml',
                                    'resources/*.yaml',
                                    'resources/*.png']
                    },
      zip_safe=False, # Important for reading data files
      # scripts=['post-install.py'],
      cmdclass = {'bootstrap': Bootstrap,
                  'test': PyTest,
                  'cleantest': CleanTest
                  },
      )
      
