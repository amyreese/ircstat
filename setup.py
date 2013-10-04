from setuptools import setup

from os import path
import shutil

import ircstat

if path.isfile('README.md'):
    shutil.copyfile('README.md', 'README')

setup(name='ircstat',
      description='generate statistics and graphs from IRC channel logs',
      version=ircstat.VERSION,
      author='John Reese',
      author_email='john@noswap.com',
      url='https://github.com/jreese/ircstat',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Utilities',
                   'Development Status :: 2 - Pre-Alpha',
                   ],
      license='MIT License',
      install_requires=['matplotlib>=1.3.0',
                        'Jinja2>=2.6',
                        ],
      requires=['matplotlib (>=1.3.0)',
                'Jinja2 (>=2.6)',
                ],
      packages=['ircstat', 'ircstat.plugins'],
      scripts=['bin/ircstat'],
      )
