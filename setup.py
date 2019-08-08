# coding: utf-8
#
# Copyright 2019, Kurusugawa Computer Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

about = {}
with open(os.path.join(here, 'm3u8tool', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(
        filter(None, [strip_comments(l) for l in open(os.path.join(os.getcwd(), *f)).readlines()])
    )

setup(
    name='m3u8tool',
    version=about['__version__'],
    description='A HTTP Live Streaming (HLS) manipulation tool',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='squld',
    author_email='sato@kurusugawa.jp',
    url='https://github.com/kurusugawa-computer/m3u8tool',
    install_requires=[reqs('requirements.txt')],
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "m3u8tool = m3u8tool.app:main"
        ]
    },
    license='Apache License 2.0',
    python_requires='>=3.5',
    keywords='m3u8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],
)

