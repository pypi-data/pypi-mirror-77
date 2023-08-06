
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()

# This call to setup() does all the work
setup(
    name="helloCaseULW",
    version="1.0.1",
    descp="The hello world package",
    long_descp=README,
    long_descp_content="text/markdown",
    author="Chhavi Trivedi",
    authoremail="chhavi7320@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["caseSelector2"],
    includepackagedata=True,
    install_requires=["pathlib"],
    entrypoints={
        "console_scripts": [
            "py_case=caseSelector2.__main__:main",
        ]
    },
)
