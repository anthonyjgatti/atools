from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

import logging
import os
import pip
import sys
logger = logging.getLogger(__name__)

# version - ADD VERSION COMMAND.

class Tox(TestCommand):
    user_options = [('tox-args=', None, "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline(args=self.tox_args.split())
        sys.exit(errno)

def do_setup(install_list):
    setup(
        name='atools',
        license='MIT',
        version = 0.1,
        packages=find_packages(exclude=['tests*']),
        include_package_data=True,
        install_requires=install_list,
        cmdclass={
            'test': Tox
        }
    )

if __name__ == '__main__':

    with open('requirements.txt', 'r') as f:
        install_list = [line for line in f.readlines()]
    do_setup(install_list)
