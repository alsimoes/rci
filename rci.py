# -*- coding: utf-8 -*-
# rci.py

"""

RCI RANDOM COPIES INDEXER


This script reads a directory recursively, generates an MD5 hash of 
each file and writes the result to a log file.
"""

"""
LICENCE:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import hashlib
from datetime import datetime 

__author__ = "Andre Simoes"
__copyright__ = "Copyright 2011, Andre Simoes"
__credits__ = ["Andre Simoes", ]
__license__ = "GPLV3"
__version__ = "0.1 (alpha)"
__maintainer__ = "Andre Simoes"
__email__ = "alsimoes@gmail.com"
__status__ = "development"

_SCRIPT_PATH = os.getcwd()
_LOG_FILE = ''.join([datetime.now().strftime("%Y%m%d%H%M%S"),'.','tmp'])


def main(args):
    """
    
    Main execution function.
    
    Usage: rci.py <directory_path>
    
    Example: rci.py C:\Temp
    """
    CWD = os.path.normcase(args)
    os.chdir(CWD)
    print "\nProcessing files. Please wait...\n"
    _start_log(CWD)
    readed_files = _read_files(CWD)
    _finish_log(readed_files)
    nfile = _set_log_name()
    print u'%i file(s) analyzed(s) in "%s".\nAnalysis results in "%s".' % (readed_files,CWD,nfile)

    
def _read_files(dir_path):
    file_counter = 0
    dir_path = os.path.normcase(dir_path)
    os.chdir(dir_path)
    files_ = os.listdir(dir_path)
    file_list = []
    dir_list = []
    
    for file_ in files_:
        if os.path.isfile(file_):
            file_list.append(file_)    
        else:
            dir_list.append(file_)
    
    for file_name_ in file_list:
        file_counter += 1
        _write_log_line('%32s %s\\%s\n' % (_md5sum(file_name_),dir_path,file_name_))
    
    for dir in dir_list:
        file_counter += _read_files(os.path.join(dir_path,dir))
    
    return file_counter

def _start_log(args):
    LOG_PATH = os.path.join(_SCRIPT_PATH,_LOG_FILE)
    file = open(LOG_PATH, 'w')
    file.write(u'RCI RANDOM COPIES INDEXER\n\nStart directory: "%s"\n\n' % args)
    file.close()    

def _write_log_line(nline):
    LOG_PATH = os.path.join(_SCRIPT_PATH,_LOG_FILE)
    file = open(LOG_PATH, 'a')
    file.write(nline)
    file.close()


def _finish_log(args):
    LOG_PATH = os.path.join(_SCRIPT_PATH,_LOG_FILE)
    file = open(LOG_PATH, 'a')
    file.write(u'\n%i file(s) analyzed(s).' % args)
    file.close() 


def _set_log_name():
    LOG_PATH = os.path.join(_SCRIPT_PATH,_LOG_FILE)
    #new_filename = ''
    new_filename = ''.join([datetime.now().strftime("%Y%m%d%H%M%S"),'-','rci','.','log'])
    os.chdir(_SCRIPT_PATH)
    os.rename(LOG_PATH,new_filename)
    return new_filename
    

def _md5sum(file_name_):
    """
    
    Returns an md5 hash for file file_name_, or stdin if file_name_ is "-".
    Source: http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python/4213255#4213255
    """
    md5 = hashlib.md5()
    f = open(file_name_,'rb')
    for chunk in iter(lambda: f.read(8192), ''): 
        md5.update(chunk)
    return md5.hexdigest()


if __name__ == '__main__':
    main(sys.argv[1])
    