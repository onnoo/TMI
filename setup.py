from setuptools import setup, find_packages

setup(
    name             = 'tmi',
    version          = '0.5.599',
    description      = "NoStress team (2018 HU-OSS B-6)'s Open Source CLI Todo List",
    author           = 'onnoo',
    author_email     = 'sweyjw@gmail.com',
    url              = 'https://github.com/onnoo/hu-oss-sw-2018-B-6',
    download_url     = 'https://github.com/onnoo/hu-oss-sw-2018-B-6/archive/master.tar.gz',
    install_requires = [ ],
    packages         = find_packages(exclude = [ ]),
    keywords         = ['tmi', 'todo list', 'todo cli'],
    python_requires  = '>=3',
    package_data     =  {'tmi' : [ "LICENSE" ]},
    zip_safe=False,
    classifiers      = [
        'Environment :: Consol',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points = {
        'console scripts' : [
            'tmi = tmi',
        ],
    },
)