import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    'IPython[all]==3.2.3',
    'plotly==1.12.2'
]


setup(
    name = "SysBio simulator",
    version = "0.0.1",
    author = "Ana Bulovic",
    author_email = "bulovic.ana@gmail.com",
    description = ("Dockerized system to facilitate systems biology ODE model simulation and visualization"),
    license = "GPLv3",
    keywords = "sysbio visualization docker",
    packages = find_packages(),
    long_description = read('README.md'),
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Framework :: IPython",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    install_requires = requirements,
    entry_points = {
        "distutils.commands": [
            "build_docker=docker.build:DockerBuild",
        ],
    },
)