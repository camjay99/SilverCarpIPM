import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MetaIPM_rerickson-USGS",
    version="1.0.0",
    author="Richard A. Erickson, James P. Pierce, Greg J. Sandland",
    author_email="rerickson@usgs.gov, jpeirce@uwlax.edu, gsandland@uwlax.edu",
    description="A meta-population model with Integral Population Models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.usgs.gov/umesc/metaIPM",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib','numpy','pandas','scipy','seaborn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
