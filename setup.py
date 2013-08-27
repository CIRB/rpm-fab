#from distutils.core import setup
from setuptools import setup
import os

version = '0.1.0'

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

long_description = '\n\n'.join([
    #open(os.path.join(PROJECT_PATH, 'README.md')).read()
    ])

install_requires = [
    'fabric'
    ]

setup(name='rpm-fab',
    version=version,
    description="Build rpm from eggs",
    long_description=long_description,
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords=[],
    author='CIRB',
    author_email='irisline@cirb.irisnet.be',
    url='',
    license='GPL',
    packages=['rpm_fab'],
    install_requires=install_requires,
    include_package_data=True,
    # data_files=[
    #     ('templates', ['templates/{0}'.format(f) for f in os.listdir('templates')]),
    # ],
    # scripts = ['manage.py'],
    entry_points={
        'console_scripts': [
            'rpm_fab = rpm_fab.main:rpm_fab'
        ]
    },
    )
