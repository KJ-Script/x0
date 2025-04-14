from setuptools import setup, find_packages

setup(
    name="exo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
    ],
    python_requires=">=3.8",
) 