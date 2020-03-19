#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'jinja2', 'google-cloud-bigquery']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Marcelo Costa",
    author_email='mesmacosta@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python code that creates properties files containing all BigQuery resources",
    entry_points={
        'console_scripts': [
            'bq_properties_creator=bq_properties_creator.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bq_properties_creator',
    name='bq_properties_creator',
    packages=find_packages(include=['bq_properties_creator', 'bq_properties_creator.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mesmacosta/bq_properties_creator',
    version='0.1.0',
    zip_safe=False,
)
