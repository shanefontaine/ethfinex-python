import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ethfinex-python",
    version="0.1.0",
    author="Shane Fontaine",
    author_email="shane6fontaine@gmail.com",
    description="An unofficial python wrapper for the Ethfinex exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shanefontaine/ethfinex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
