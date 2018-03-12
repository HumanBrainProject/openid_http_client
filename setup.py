from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='oidc_login_client',
    version='0.0.1',
    packages=['oidc_login_client', 'oidc_login_client.auth_client'],
    install_requires = reqs,
    scripts=['manage.py']
)
