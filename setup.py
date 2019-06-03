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
    description='A HTTP Live Streaming (HLS) manipulation tool',
    author='sato@kurusugawa.jp',
    url='https://github.com/kurusugawa-computer/m3u8tool',
    install_requires=[reqs('requirements.txt')],
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "m3u8tool = m3u8tool.app:main"
        ]
    }
)
