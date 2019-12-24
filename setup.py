# pylint: disable=line-too-long
import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="ccc-calculator",
    version="0.1.0",
    description="command-line combinatorial calculator",
    author="Alex Riley",
    entry_points={"console_scripts": ["ccc=ccc.bin.cli:ccc"]},
    install_requires=["sympy", "click"],
    include_package_data=True,
    keywords="count collection probability sequence permutation calculator",
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    project_urls={
        "Source": "https://github.com/ajcr/ccc/",
        "Tracker": "https://github.com/ajcr/ccc/issues",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    tests_require=["pytest"],
)
