from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gluestick',
    version='1.0.2',
    description='ETL utility functions built on Pandas',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hotgluexyz/gluestick',
    author='hotglue',
    author_email='hello@hotglue.xyz',
    license='MIT',
    packages=['gluestick'],
    zip_safe=False
)
