#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=('calaccess_processed',),
            MIDDLEWARE_CLASSES=()
        )
        from django.core.management import call_command
        import django
        django.setup()
        call_command('test', 'calaccess_processed')


setup(
    name='django-calaccess-processed-data',
    version='0.2.10',
    license='MIT',
    description='A Django app to transform and refine campaign finance data from the California Secretary of State’s \
CAL-ACCESS database',
    url='http://django-calaccess.californiacivicdata.org',
    author='California Civic Data Coalition',
    author_email='cacivicdata@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including static files
    install_requires=(
        'django-calaccess-raw-data==2.0.6',
        'django-calaccess-scraped-data==2.0.0',
        'django>=1.11.*',
        'csvkit>=1.0',
        'opencivicdata>=2.0',
        'psycopg2>=2.7.3',
    ),
    cmdclass={'test': TestCommand,},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'License :: OSI Approved :: MIT License',
    ),
)
