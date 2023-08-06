import sys

from setuptools import setup, find_packages
from snmp_collector import __version__


if sys.version_info[0] < 3:
    with open('README.rst') as f:
        long_description = f.read()
else:
    with open('README.rst', encoding='utf-8') as f:
        long_description = f.read()


setup(
    name='simple_snmp_collector',
    version=__version__,
    description='SNMP collector through an asyncio loop',
    long_description=long_description,
    url='https://github.com/agn-7/simple-snmp-collector',
    author='agn-7',
    author_email='benyaminjmf@gmail.com',
    license='MIT',
    packages=find_packages(),
    keywords=[
        'snmp',
        'snmp-collector',
        'asyncio',
        'python3',
        'python',
        'docker',
        'docker-compose'
    ],
    download_url='https://github.com/agn-7/simple-snmp-collector/archive/1.0.0.zip',
    install_requires=[
        'pyserial',
        'easydict',
        'pysnmp==4.4.9',
        'async-timeout'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
