# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oceandata']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'numpy>=1.16,<2.0', 'pandas>0.25', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'oceandata',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'Bror Jonsson',
    'author_email': 'brorfred@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
