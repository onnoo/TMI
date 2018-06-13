from setuptools import setup, find_packages

setup(
    name             = 'tmi',
    version          = '0.6.620',
    description      = "NoStress team (2018 HU-OSS B-6)'s Open Source CLI Todo List",
    author           = 'onnoo',
    author_email     = 'sweyjw@gmail.com',
    url              = 'https://github.com/onnoo/TMI',
    download_url     = 'https://github.com/onnoo/TMI/archive/master.tar.gz',
    install_requires = [  'click>=6.0' ],
    packages         = find_packages(exclude = [ ]),
    keywords         = ['tmi', 'todo list', 'todo cli'],
    python_requires  = '>=3',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data     =  {'tmi' : [ "LICENSE" ]},
    zip_safe=False,
    classifiers      = [

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points = {
        'console_scripts' : [
            'tmi = tmi.tmi:main',
        ],
    },
)
