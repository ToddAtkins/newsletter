#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'newsletter',
    version = '1.0.1',
    description = 'simple newsletter generator',
    packages = find_packages(include=['publish']),
    install_requires = [
        'icalendar',
        'pytz',
        'python-twitter',
        'tzlocal',
    ],
    namespace_packages = ['publish'],
    entry_points = {
        'console_scripts': [
            'mycalendar = publish.mycalendar:main',
            'quote = publish.quote:main',
            'mytweets = publish.mytwitter:main',
        ],
    },
    author = 'E. Todd Atkins',
    author_email = 'sbwino@gmail.com',
    license = 'BSD',
    url = 'https://github.com/ToddAtkins/newsletter',
    download_url = 'https://github.com/ToddAtkins/newsletter.git',
)
