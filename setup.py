from setuptools import setup, find_packages
import os

version = '0.1.0'

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

long_description = '\n\n'.join([
    # open(os.path.join(PROJECT_PATH, 'README.md')).read()
])

install_requires = [
    'fabric'
]

setup(
    name='rpm-fab',
    version=version,
    packages=find_packages(),
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
    install_requires=install_requires,
    include_package_data=True,
    scripts=['rpm.py']
    # data_files=[
    #     ('templates', ['templates/{0}'.format(f) for f in os.listdir('templates')]),
    # ],
    # entry_points={
    #     'console_scripts': [
    #         'rpm_fab = rpm_fab.main:rpm_fab'
    #     ]
    # },
)
