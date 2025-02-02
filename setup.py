#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import codecs
import os
import re
import sys


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    os.chdir('threadedcomments')
    try:
        from django.core import management
        management.call_command('compilemessages', stdout=sys.stderr, verbosity=1)
    except ImportError:
        if 'sdist' in sys.argv:
            raise
    finally:
        os.chdir('..')


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='wagtail-threadedcomments',
    version=find_version('threadedcomments', '__init__.py'),
    license='BSD',
    install_requires=[
        'django-contrib-comments>=1.9.0',
        'wagtail>=4.0',
    ],

    description='A simple yet flexible threaded commenting system.',
    long_description=read('README.rst'),
    keywords='wagtail,django,comments,threading',

    author='Eric Florenzano',
    author_email='floguy@gmail.com',

    maintainer='Diederik van der Boor',
    maintainer_email='vdboor@edoburu.nl',

    url='https://github.com/monneyboi/wagtail-threadedcomments',
    download_url='https://github.com/monneyboi/wagtail-threadedcomments/zipball/master',

    packages=find_packages(),
    include_package_data=True,

    test_suite = 'runtests',

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
