from setuptools import find_packages, setup

setup(
    name="ccc",
    version="0.1.0",
    description="ccc: command-line combinatorial calculator",
    author="Alex Riley",
    python_requires=">=3.6.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["ccc=ccc.bin.cli:ccc"]},
    install_requires=["sympy", "click"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
