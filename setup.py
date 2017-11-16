from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]

setup(
    name='pymdwizard',
    version='2.0.0',
    description='A CSDGM Metadata Editor',
    long_description=long_description,
    url='https://github.com/usgs/fort-pymdwizard',
    author='Colin B. Talbert',
    author_email='talbertc@usgs.gov',
    license='CC0 4.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Build Tools',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='metadata FGDC BDP CSDGM',
    packages=find_packages(exclude=['tests']),
    extras_require={'testing': ['pytest'], },
    install_requires=install_requires,
)
