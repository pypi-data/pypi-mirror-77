"""
matterhook
"""

import os
import sys

from pkg_resources import get_distribution, parse_version
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read(fname: str):
    """Read README file
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top
    level README file and 2) it's easier to type in the README file than to
    put a raw string in below ...

    :param fname: README filename
    :type fname: str
    :return: File contents
    :rtype: str
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)

        # https://bitbucket.org/pypa/setuptools/commits/cf565b6
        if get_distribution("setuptools").parsed_version < parse_version("18.4"):
            self.test_args = []
            self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    author="numberly",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={"test": PyTest},
    description="Interact with Mattermost incoming webhooks easily.",
    download_url="https://github.com/numberly/matterhook/tags",
    include_package_data=True,
    install_requires=[],
    license="BSD",
    long_description=read("README.rst"),
    name="matterhook",
    packages=find_packages(),
    platforms="any",
    tests_require=["pytest"],
    url="https://github.com/numberly/matterhook",
    version="0.2",
    zip_safe=True,
)
