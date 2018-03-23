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
    version='0.0.16',
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
