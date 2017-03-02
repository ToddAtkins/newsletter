#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'newsletter',
    version = '1.0.0',
    description = 'simple newsletter generator',
    packages = findpackages(include=['publish']),
    install_requires = [
        'argparse',
        'ConfigParser',
        'datetime',
        'email'
        'icalendar',
        'json',
        'operator',
        'pytz',
        'random',
        'smtplib',
        'twitter',
        'tzlocal',
        'urllib',
    ],
    namespace_packages = ['publish'],
    entry_points = {
        'console_scripts': [
            'calendar = publish.calendar:main',
            'quote = publish.quote:main',
            'tweets = publish.tweets:main',
        ],
    },
    author = 'E. Todd Atkins',
    author_email = 'sbwino@gmail.com',
    license = 'BSD',
    url = 'https://github.com/ToddAtkins/newsletter',
    download_url = 'https://github.com/ToddAtkins/newsletter.git',
)
