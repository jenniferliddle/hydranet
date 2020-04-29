#!/usr/bin/env python

import setuptools

setuptools.setup(name='Hydranet',
      version='0.1',
      description='Hydranet Telemetry System',
      author='Jennifer Liddle',
      author_email='jennifer@jsquared.co.uk',
      url='http://hydranet.co.uk',
      packages=setuptools.find_packages(),
      install_requires=['pika'],
     )

