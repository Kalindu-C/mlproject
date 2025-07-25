from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    This function reads a requirements file and returns a list of packages.
    It removes any version specifiers and comments.
    """
    with open(file_path, 'r') as file:
        requirements = file.readlines()
    
    # Clean up the requirements
    cleaned_requirements = [req.replace('\n', '') for req in requirements]

    if HYPEN_E_DOT in cleaned_requirements:
        cleaned_requirements.remove(HYPEN_E_DOT)
        
    return cleaned_requirements

setup(
    name='mlproject',
    version='0.0.1',
    author='Kalindu Chathuranga',
    author_email='kctchathuranga@gmail.com',
    packages=find_packages(),   
    install_requires=get_requirements('requirements.txt')
)