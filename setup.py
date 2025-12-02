"""Setup script for sweep CLI."""

from setuptools import setup, find_packages

setup(
    name='sweep-cli',
    version='2.0.0',
    description='Filesystem analyzer with hardlink organization',
    author='Jake Ferraro',
    url='https://github.com/jakeferraro/sweep-cli',
    py_modules=['sweep', 'scanner', 'linker', 'output', 'config', 'utils', 'categories'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sweep=sweep:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
)