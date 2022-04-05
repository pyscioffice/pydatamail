"""
Setuptools based setup module
"""
from setuptools import setup, find_packages
import versioneer


setup(
    name='pydatamail',
    version=versioneer.get_version(),
    description='pydatamail - a python module to apply data science principles to email processing',
    url='https://github.com/pyscioffice/pydatamail',
    author='Jan Janssen',
    author_email='jan.janssen@outlook.com',
    license='BSD',
    packages=find_packages(exclude=["*tests*"]),
    install_requires=[
        'tqdm==4.64.0',
        'pandas==1.4.2',
        'sqlalchemy==1.4.34',
        'numpy==1.22.3',
        'matplotlib==3.5.1',
        'scikit-learn==1.0.2'
    ],
    cmdclass=versioneer.get_cmdclass()
)
