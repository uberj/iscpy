try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys, os

version = '1.0.3'

setup(
    name='iscpy',
    version=version,
    description="Python library to parse ISC style config files.",
    long_description="""\
        ISCpy is a robust ISC config file parser. It has virtually unlimited
        possibilities for depth and quantity of ISC config files. ISC config
        files include BIND and DHCP config files among a few others.
    """,
    classifiers=[],
    keywords='isc config bind dhcp parser dns python',
    author='Jacob C. Collins',
    author_email='jc@purdue.edu',
    url='',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points="""
    """,
)
