# code for code management 

from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements= f.read().splitlines()
   
setup(
    name="Required_packages",
    version="0.1",
    author="Akshay Rao",
    packages=find_packages(),
    install_requires= requirements
)