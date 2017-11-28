'''
This file needs to be renamed to wsgi.py and placed in
the development apache directory
In my case, that's /var/www/hydranet_dev

The only difference bethween this and the live version
is the addition of the 'DEV' environment variable

'''
import sys
import os

sys.path.insert(0, '/usr/local/bin')

os.environ['DEV'] = '1'

from hydranet_dev import app as application
