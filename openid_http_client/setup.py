#   Copyright (c) 2018, EPFL/Human Brain Project PCO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
from setuptools import setup

if os.path.exists("../README.md"):
    try:
        import pypandoc
        long_description = pypandoc.convert('../README.md', 'rst')
    except(IOError, ImportError):
        long_description = open('../README.md').read()
else:
    long_description = "This library provides an Http client for Pyxus with support of OpenID token authentication."

setup(
    name='openid_http_client',
    version='0.0.22',
    packages=['openid_http_client', 'openid_http_client.auth_client'],
    install_requires = ["requests", "curlify"],
    scripts=['manage.py'],
    description = 'OpenID HTTP Client with auth',
    author = 'HumanBrainProject',
    author_email = 'platform@humanbrainproject.eu',
    keywords = ['OpenID', 'http', 'client'],
    classifiers = [],
    url = 'https://github.com/HumanBrainProject/openid_http_client',
    download_url = 'https://github.com/HumanBrainProject/openid_http_client/archive/master.zip',
    long_description = long_description
)
