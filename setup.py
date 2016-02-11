import collections

from distutils.version import StrictVersion
from setuptools import setup, find_packages
from pip.req import parse_requirements
import pip

with open('README.md', 'r') as readme_fd:
    LONG_DESCRIPTION = readme_fd.read()


def get_install_requirements(fname):

    ReqOpts = collections.namedtuple('ReqOpts', [
        'skip_requirements_regex',
        'default_vcs',
        'isolated_mode',
    ])

    opts = ReqOpts(None, 'git', False)
    params = {'options': opts}

    requires = []

    pip_version = StrictVersion(pip.__version__)
    session_support_since = StrictVersion('1.5.0')
    if pip_version >= session_support_since:
        from pip.download import PipSession
        session = PipSession()
        params.update({'session': session})

    for ir in parse_requirements(fname, **params):
        if ir is not None and ir.req is not None:
            requires.append(str(ir.req))
        return requires


tests_require = get_install_requirements('requirements-tests.txt')

setup(
    name="py-look-for-timeouts",
    version="0.4",
    author="James Brown",
    author_email="jbrown@uber.com",
    url="https://github.com/uber/py-look-for-timeouts",
    description="ple python ast consumer which searches for missing timeouts",
    license='MIT (Expat)',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Security",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Alpha",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "py-look-for-timeouts = py_look_for_timeouts.main:main",
        ]
    },
    tests_require=tests_require,
    test_suite="nose.collector",
    long_description=LONG_DESCRIPTION
)
