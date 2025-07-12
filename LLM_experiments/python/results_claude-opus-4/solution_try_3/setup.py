"""Setup configuration for phylogenetic clustering package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phylogenetic-clustering",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Phylogenetic tree construction and clustering analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phylogenetic-clustering",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.0",
        "matplotlib>=3.6.0",
        "scipy>=1.10.0",
    ],
    entry_points={
        "console_scripts": [
            "phylogenetic-analysis=src.main_complete_pipeline:main",
        ],
    },
)