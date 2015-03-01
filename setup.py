# coding: utf-8
from setuptools import setup


setup(
    name='vonpit-dbus',
    version='0.1',
    packages=['vonpit_dbus', 'vonpit_dbus.tests'],
    package_dir={'': 'src'},
    url='',
    license='',
    author='Pascal Potvin',
    author_email='pascal.potvin@gmail.com',
    description='',
    install_requires=[
        'six',
        'mock',
    ],
)
