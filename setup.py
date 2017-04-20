from setuptools import setup


from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sharearray',
    version='0.1',
    py_modules=['sharearray'],

    url='https://github.com/bshillingford/python-sharearray',
    description=("Share numpy arrays across processes efficiently "
		 "(ideal for large, read-only datasets)"),
    long_description=long_description,

    author='Brendan Shillingford',
    license='Apache Software License 2.0',
    install_requires=['numpy'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
