"""Setup script for sweep CLI."""

from setuptools import setup, find_packages

setup(
    name='sweep-cli',
    version='2.0.0',
    description='Filesystem analyzer with macOS GUI for file management',
    author='Jake Ferraro',
    url='https://github.com/jakeferraro/sweep-cli',
    py_modules=['sweep', 'scanner', 'output', 'config', 'utils', 'categories', 'file_viewer'],
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.4.0',
    ],
    entry_points={
        'console_scripts': [
            'sweep=sweep:main',
            'sweep-gui=file_viewer:main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Desktop Environment',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
)