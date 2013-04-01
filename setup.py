#!/usr/bin/env python
from distutils.core import setup
import glob
import os

setup(
    name = "rainbow",
    version = "2.5.0",
    author = "Julien Nicoulaud",
    author_email = "julien.nicoulaud@gmail.com",
    description = ("Colorize commands output or STDIN using patterns."),
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license = "GPLv3",
    url = "https://github.com/nicoulaj/rainbow",
    keywords = "color colorize colorizer pattern",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Topic :: System",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    scripts=['rainbow'],
    data_files=[
      ('/usr/share/rainbow/configs', glob.glob('configs/*')),
      ('/etc/bash_completion.d', ['completion/bash/rainbow']),
      ('/usr/share/zsh/site-functions', ['completion/zsh/_rainbow'])
    ],
)
