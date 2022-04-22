#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name = 'newsletter',
    version = '3.1.0',
    description = 'simple newsletter generator',
    packages = find_packages(include=['publish']),
    install_requires = [
        'icalendar',
        'pytz',
        'python-twitter',
    	'requests',
        'tzlocal',
    ],
    namespace_packages = ['publish'],
    scripts = [
        'bin/publish',
        'bin/events',
        'bin/tweets',
        'bin/quote-of-the-day'
    ],
    author = 'Todd Atkins',
    author_email = 'sbwino@gmail.com',
    license = 'BSD',
    url = 'https://github.com/ToddAtkins/newsletter',
    download_url = 'https://github.com/ToddAtkins/newsletter.git',
)
