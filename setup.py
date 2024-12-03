import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="corderius-play",
    version="2.2.1",
    description="The easiest way to make games and media projects in Python.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Corderius-College-Amersfoort/play",
    author="koen1711",
    author_email="koenvurk1711@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.10",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pygame", "numpy", "pymunk", "screeninfo"],
)
