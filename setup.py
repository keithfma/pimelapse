from setuptools import setup, find_packages
from setuptools import setup

setup(
    name='pimelapse',
    version='0.0.0',
    description='Timelapse videos with Raspberry Pi camera',
    url='https://github.com/keithfma/pimelapse',
    author='Keith F. Ma',
    pymodules=['pimelapse'],
    packages=find_packages(),
    python_requires='>=3.2',
    install_requires=[],
    entry_points={'console_scripts': []}
)
