''' pytradestart '''

import os.path
# import codecs  # To use a consistent encoding
import setuptools
import re
import time

now = str(round(time.time()))
here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as f:
    desc = f.read()
    desc = desc.split("<!-- content -->")[-1]
    desc = re.sub("<[^<]+?>", "", desc)  # Remove html


def get_property(prop, project):
    ''' get a project property: from init '''
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


# Package name
pname = 'pytradestart'

# Generate linkes
gurl = 'https://github.com/smacken/' + pname

setuptools.setup(
    name=pname,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version=__version__,
    version=get_property('__version__', pname) + f'.{now}',

    description='Trading Portfolio',
    long_description=desc,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url=gurl,

    # Author details
    author='Scott Mackenzie',
    author_email='scott.mac.web@gmail.com',

    # Choose your license
    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',

        # Indicate which Topics are covered by the package
        'Topic :: Software Development',
        'Topic :: Office/Business :: Financial',

        # Pick your license as you wish (should match "license" above)
        ('License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'),

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        # Operating Systems on which it runs
        'Operating System :: OS Independent',
    ],

    # What does your project relate to?
    keywords=['trading', 'development'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=setuptools.find_packages(exclude=['docs', 'docs2', 'samples']),
    # packages=['mockportfolio', '],

    # List run-time dependencies here.
    # These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['six'],

    # List additional groups of dependencies here
    # (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={'sample': ['package_data.dat'],},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={'console_scripts': ['sample=sample:main',],},

    # scripts=['tools/bt-run.py'],
)
