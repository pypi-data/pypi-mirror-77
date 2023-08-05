#!/usr/bin/env python
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


version = '1.1.0'


class ToxTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--recreate']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import detox.main
        errno = detox.main.main(self.test_args)
        sys.exit(errno)


dirname = os.path.dirname(__file__)

long_description = (
    open(os.path.join(dirname, 'README.rst')).read() + '\n' +
    open(os.path.join(dirname, 'CHANGES.rst')).read()
)

setup(
    name='pytest-fixture-tools',
    description='Plugin for pytest which provides tools for fixtures',
    long_description=long_description,
    author='Paylogic International',
    license='MIT license',
    author_email='developers@paylogic.com',
    version=version,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ] + [('Programming Language :: Python :: %s' % x) for x in '2.6 2.7 3.0 3.1 3.2 3.3'.split()],
    cmdclass={'test': ToxTestCommand},
    install_requires=[
        'pytest', 'pydot'
    ],
    # the following makes a plugin available to py.test
    entry_points={
        'pytest11': [
            'pytest-fixture-tools = pytest_fixture_tools.plugin',
        ]
    },
    tests_require=['detox'],
    packages=['pytest_fixture_tools'],
)
