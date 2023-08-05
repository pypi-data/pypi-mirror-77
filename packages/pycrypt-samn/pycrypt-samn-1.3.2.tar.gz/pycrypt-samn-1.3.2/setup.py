
from setuptools import setup

with open('requirements.txt') as f:
    install_packs = f.read().splitlines()
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pycrypt-samn',
    version='1.3.2',
    description='Customized Encryption module',
    long_description_content_type='text/markdown',
	long_description=long_description,
    license='Apache',
    packages=['pycrypt'],
    install_requires=install_packs,
    author='Sammy Shuck github.com/ToxicSamN',
    keywords=['pycrypt', 'pycrypt-samn'],
    url='https://github.com/ToxicSamN/pycrypt'
)
