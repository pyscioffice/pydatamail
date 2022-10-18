"""
Setuptools based setup module
"""
from setuptools import setup, find_packages
from pathlib import Path
import versioneer


setup(
    name='pydatamail',
    version=versioneer.get_version(),
    description='pydatamail - a python module to apply data science principles to email processing',
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyscioffice/pydatamail',
    author='Jan Janssen',
    author_email='jan.janssen@outlook.com',
    license='BSD',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=[
        'numpy==1.23.4',
        'tqdm==4.64.1',
        'pandas==1.5.0',
        'sqlalchemy==1.4.42',
        'matplotlib==3.6.1',
    ],
    cmdclass=versioneer.get_cmdclass()
)
