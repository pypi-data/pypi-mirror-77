import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdcsm",
    version="0.3.9.7.9",
    author="Stephen Hilton",
    author_email="Stephen@FamilyHilton.com",
    description="Teradata tools for CSMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tdcoa/tdcsm",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "requests",
        "pyyaml",
        "teradatasql",
        "matplotlib",
        "seaborn",
        "python-pptx",
        "pydantic",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['tdcsm=tdcsm.cli:main']
    },
    python_requires=">=3.6",
    include_package_data=True
)
