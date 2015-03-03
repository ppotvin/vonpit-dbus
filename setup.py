# coding: utf-8
from setuptools import setup, find_packages


setup(
    name='vonpit-dbus',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    license='MIT',
    author='Pascal Potvin',
    author_email='pascal.potvin@gmail.com',
    description='',
    install_requires=[
        'six',
        'mock',
    ],
)
