from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("http_client/requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='http_client',
    version='0.0.1',
    packages=['http_client', 'http_client.auth_client', 'http_client.test'],
    install_requires = reqs,
    scripts=['manage.py']
)
