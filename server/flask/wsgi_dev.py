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
sys.path.insert(0, '/usr/local/lib/python2.7')

os.environ['DEV'] = '1'

from hydranet import app as application
