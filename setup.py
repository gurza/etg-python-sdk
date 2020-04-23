# -*- coding: utf-8 -*-
from setuptools import setup
import os
import sys
if sys.version_info[0] < 3:
    from io import open

here = os.path.abspath(os.path.dirname(__file__))

packages = ['etg']

requires = [
    'requests>=2.21.0, <3',
]
test_requirements = [
    'pytest>=5.4',
]

about = {}
with open(os.path.join(here, 'etg', '__version__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', encoding='utf-8') as f:
    readme = f.read()
with open('HISTORY.md', encoding='utf-8') as f:
    history = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_dir={'etg': 'etg'},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    tests_require=test_requirements,
    project_urls={
        'Source': 'https://bitbucket.org/anyticket/ostrovok-client',
    },
)
