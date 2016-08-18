# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='imgtool',
    version='0.1.1',
    packages=['imgtool'],
    install_requires=['pillow'],
    author='Taehong Kim',
    author_email='peppy0510@hotmail.com',
    description='',
    long_description='',
)
