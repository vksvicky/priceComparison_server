#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

# extensions = [
#     'extname',
#     'sphinx.ext.todo',
# ]

# # Display todos by setting to True
# todo_include_todos = True

test_requirements = ['pytest>=3', ]

setup(
    author="Vivek Krishnan",
    author_email='vksvicky@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Compare high-street stores product price",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pricecomparison',
    name='pricecomparison',
    packages=find_packages(include=['pricecomparison', 'pricecomparison.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/vksvicky/pricecomparison',
    version='0.2.0',
    zip_safe=False,
)
