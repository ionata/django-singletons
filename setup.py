#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='django-singleton',
    version='0.1.8',
    description='Reusable singleton models for Django',
    author='Chris Davis',
    author_email='defbyte@gmail.com',
    url='https://github.com/defbyte/django-singleton',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)