#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'requests>=2.13.0',
]

tests_require = [
    'pytest',
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ethfinex-python",
    version="0.1.2",
    author="Shane Fontaine",
    author_email="shane6fontaine@gmail.com",
    license='MIT',
    description="An unofficial python wrapper for the Ethfinex exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shanefontaine/ethfinex",
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    keywords=['ethfinex', 'ethfinex-api', 'orderbook', 'trade', 'bitcoin', 'ethereum', 'BTC', 'ETH', 'client', 'api', 'wrapper',
              'exchange', 'crypto', 'currency', 'trading', 'trading-api', 'ethfinex-trustless', 'bitfinex'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3.6",
    ],
)
