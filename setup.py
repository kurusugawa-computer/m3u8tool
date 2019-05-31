# coding: utf-8

from setuptools import setup, find_packages
import os


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(
        filter(None, [strip_comments(l) for l in open(os.path.join(os.getcwd(), *f)).readlines()])
    )


setup(
    name='m3u8tool',
    version='0.1.0',
    description='A tool for m3u8+ts movie.',
    author='sato@kurusugawa.jp',
    url='',
    install_requires=[reqs('requirements.txt')],
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "m3u8tool = m3u8tool.app:main"
        ]
    }
)
