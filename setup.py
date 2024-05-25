from setuptools import setup, find_packages

# Read the requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='certificate_generator',  
    version='1.0.0',
    author='Rishitha',
    author_email='ervarishitha@gmail.com',
    description='A Python package for generating custom certificates.',
    long_description='Certificate Generator is a Python package that provides a simple and flexible way to create custom certificates for various events and purposes.',
    long_description_content_type='text/plain',
    url='https://github.com/johndoe/certificate_generator',
    packages=find_packages(),
    install_requires=requirements,  # Use requirements from requirements.txt
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
