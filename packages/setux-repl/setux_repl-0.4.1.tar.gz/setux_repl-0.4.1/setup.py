from os.path import join, dirname, abspath

from setuptools import setup, find_namespace_packages

from setux.repl import __version__

curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()

setup(
    name             = 'setux_repl',
    version          = __version__,
    description      = 'System deployment',
    long_description = readme,
    keywords         = ['utility', ],
    url              = 'https://framagit.org/louis-riviere-xyz/setux_repl',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages = find_namespace_packages(include=['setux.*']),
)
