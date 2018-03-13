import os
from optparse import Option

from setuptools import setup
import pip
from pip.req import parse_requirements

# This is a hack to work with newer versions of pip
if (pip.__version__.startswith('1.5') or
   int(pip.__version__[:1]) > 5):
    from pip.download import PipSession  # pylint:disable=E0611
    OPTIONS = Option("--workaround")
    OPTIONS.skip_requirements_regex = None
    OPTIONS.isolated_mode = False
    # pylint:disable=E1123
    INSTALL_REQS = parse_requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"),
                                      options=OPTIONS,
                                      session=PipSession)
else:  # this is the production path, running on RHEL
    OPTIONS = Option("--workaround")
    OPTIONS.skip_requirements_regex = None
    INSTALL_REQS = parse_requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"),
                                      options=OPTIONS)

reqs = [str(ir.req) for ir in INSTALL_REQS]

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
