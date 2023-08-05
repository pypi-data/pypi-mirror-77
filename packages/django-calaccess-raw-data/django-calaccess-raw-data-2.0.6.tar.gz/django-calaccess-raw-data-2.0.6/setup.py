#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='django-calaccess-raw-data',
    version='2.0.6',
    author='California Civic Data Coalition',
    author_email='cacivicdata@gmail.com',
    url='http://django-calaccess.californiacivicdata.org/',
    description=("A Django app to download, extract and load campaign "
                "finance and lobbying activity data from the California "
                "Secretary of State's CAL-ACCESS database"),
    long_description=read('README.rst'),
    license='MIT',
    packages=(
        'calaccess_raw',
        'calaccess_raw.admin',
        'calaccess_raw.management',
        'calaccess_raw.migrations',
        'calaccess_raw.management.commands',
        'calaccess_raw.models',
        'calaccess_raw.annotations'
    ),
    include_package_data=True,
    zip_safe=False,
    install_requires=(
        'django>=1.9',
        'django-postgres-copy>=2.3.7',
        'csvkit>=1.0',
        'requests',
        'clint',
        'hurry.filesize',
        'pytz'
    ),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'License :: OSI Approved :: MIT License'
    ),
    project_urls={
        'Project': 'https://www.californiacivicdata.org/',
        'Documentation': 'http://django-calaccess.californiacivicdata.org',
        'Funding': 'https://www.californiacivicdata.org/about/',
        'Source': 'https://github.com/california-civic-data-coalition/django-calaccess-raw-data',
        'Coverage': 'https://coveralls.io/github/california-civic-data-coalition/django-calaccess-raw-data?branch=master',
        'Tracker': 'https://github.com/california-civic-data-coalition/django-calaccess-raw-data/issues'
    },
)
