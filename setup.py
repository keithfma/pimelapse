from setuptools import setup, find_packages
from setuptools import setup

setup(
    name='pimelapse',
    version='0.1.0',
    description='Timelapse videos with Raspberry Pi camera',
    url='https://github.com/keithfma/pimelapse',
    author='Keith F. Ma',
    pymodules=['pimelapse'],
    python_requires='>=3.2',
    install_requires=[
        'click',
        'boto3',
    ],
    extras_require={
        'camera': ['picamera']
    },
    entry_points={'console_scripts': [
        'pimelapse-images=pimelapse:images_cli[camera]',
        'pimelapse-video=pimelapse:video_cli',
        ]
    }
)
