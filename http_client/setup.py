from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("http_client/requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='pyxus_http_client',
    version='0.0.1',
    packages=['http_client', 'http_client.auth_client'],
    install_requires = reqs,
    scripts=['manage.py'],
    description = 'HTTP Client with auth for Pyxus',
    author = 'HPB Team',
    author_email = 'platform@humanbrainproject.eu',
    keywords = ['pyxus', 'http', 'client'],
    classifiers = [],
    url = 'https://gitlab.humanbrainproject.org/HumanBrainProject/pyxus_http_client',
    download_url = 'https://gitlab.humanbrainproject.org/HumanBrainProject/pyxus_http_client/repository/master/archive.zip'
)
