from setuptools import setup, find_packages

setup(
    name="techdebtzero",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "techdebtzero = techdebtzero.cli:main",
        ],
    },
    python_requires=">=3.8",
)
