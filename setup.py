from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    cleaned = ""
    for line in long_description.split('\n'):
        if '[![Build Status]' in line:
            pass
        elif '[![codecov]' in line:
            pass
        else:
            cleaned += line + "\n"
    long_description = cleaned

setup(
    name="stiqueue",
    version="1.0.0",
    description="Simple Messaging queue that is easily extendable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmad88me/stiqueue",
    author="Ahmad Alobaid",
    author_email="aalobaid@fi.upm.es",
    license="Apache2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    packages=["stiqueue"],
    python_requires='>=3.6',
)