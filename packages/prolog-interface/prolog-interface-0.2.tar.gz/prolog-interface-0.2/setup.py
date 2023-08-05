# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prolog', 'prolog.swipl']

package_data = \
{'': ['*']}

install_requires = \
['pexpect>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'prolog-interface',
    'version': '0.2',
    'description': 'Keep it easy! Swi-Prolog object-oriented interface for humans.',
    'long_description': None,
    'author': 'timoniq',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
