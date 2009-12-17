from setuptools import setup, find_packages
import sys

sys.path += ['src']
import tempel

setup(
    name = "tempel",
    version = tempel.__version__,
    url = 'http://bitbucket.org/fajran/tempel/',
    license = 'AGPL',
    description = 'Tempel sana tempel sini',
    author = 'Fajran Iman Rusadi',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'pygments']
)

