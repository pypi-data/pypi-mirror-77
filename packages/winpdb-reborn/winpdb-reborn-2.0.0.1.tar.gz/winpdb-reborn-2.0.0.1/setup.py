"""
    setup.py

    Setup script for winpdb

    Copyright (C) 2013-2018 Philippe Fremy
    Copyright (C) 2005-2009 Nir Aides

    This program is free software; you can redistribute it and/or modify it 
    under the terms of the GNU General Public License as published by the 
    Free Software Foundation; either version 2 of the License, or any later 
    version.

    This program is distributed in the hope that it will be useful, 
    but WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along 
    with this program; if not, write to the Free Software Foundation, Inc., 
    59 Temple Place, Suite 330, Boston, MA 02111-1307 USA    
"""



from setuptools import setup

import os, re

# strip out build status
LONG_DESC = ''.join( open('README.md').readlines()[1:] )

WINPDB_VERSION = re.search( r'WINPDB_VERSION\s*=\s*"(.*)"', open('winpdb.py').read() ).group(1).replace('-alpha', 'a')
print( 'Packaging winpdb version: "%s"' % WINPDB_VERSION )

setup(
    name = 'winpdb-reborn',
    version = WINPDB_VERSION,
    description = 'A platform independent GPL Python debugger.',
    long_description = LONG_DESC,
    long_description_content_type="text/markdown",
    author = 'Philippe Fremy, Nir Aides',
    author_email = 'phil.fremy@free.fr',
    url = 'https://github.com/bluebird75/winpdb',
    license = 'GNU GPL',

    project_urls={
        'Source': 'https://github.com/bluebird75/winpdb/',
        'Documentation': "http://www.winpdb.org/?page_id=5",
        'Tracker': 'https://github.com/bluebird75/winpdb/issues',
    },

    python_requires='>=3.4',
    install_requires='wxpython>=4',
    packages = ['rpdb'],
    py_modules = ['rpdb2', 'winpdb'],

    entry_points={
        'console_scripts': [
            'rpdb2=rpdb2:run_rpdb2',
        ],
        'gui_scripts': [
            'winpdb=winpdb:run_winpdb',
        ],
    },




    keywords = 'debugger',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',

        # Runs in different environments
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',

        # GNU GPL v2 or above
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',

        # Runs on Windows, unix and MacOs 
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        # This version is for python 2 only
        'Programming Language :: Python :: 3 :: Only',


        'Topic :: Software Development :: Debuggers',
        'Topic :: Utilities',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Debuggers',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
    ],

)



