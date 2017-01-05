
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


def which(program):
    
    """From: http://stackoverflow.com/questions/377017/
    test-if-executable-exists-in-python/377028
    """
    
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    
    if fpath:
        
        if is_exe(program): return program

    else:
        
        for path in os.environ["PATH"].split(os.pathsep):
            
            path = path.strip('"')
            exe_file = os.path.join(path, program)

            if is_exe(exe_file): return exe_file

    return None