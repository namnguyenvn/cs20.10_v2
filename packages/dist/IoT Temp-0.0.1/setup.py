from setuptools import setup

__project__ = "IoT Temp"
__version__ = "0.0.1"
__description__ = "a Python module to that needs to be rolled back"
__packages__ = ["pi_temp"]
__author__ = "Nam Nguyen Hoai"
__author_email__ = "nguyenhoainam@ioit.ac.vn"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Research",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["rollback", "iot"]
__requires__ = ["guizero", "wmi", "sense_emu"]

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    packages=__packages__,
    author=__author__,
    author_email=__author_email__,
    classifiers=__classifiers__,
    keywords=__keywords__,
    requires=__requires__
)
