#!/usr/bin/python

""" Module for reading Hydranet configuration.
"""

import ConfigParser
import os

FILEPATHS = [
    os.path.expanduser('test/hydranetrc'),
    os.path.expanduser('/etc/hydranetrc'),
    os.path.expanduser('~/hydranetrc'),
    os.path.expanduser('~/.hydranetrc'),
]

class Config(ConfigParser.ConfigParser):

    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)
        self.read(FILEPATHS)


