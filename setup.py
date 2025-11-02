#!/usr/bin/env python3
"""
Setup script for Document Extraction Learning Group

This allows the package to be installed with pip:
    pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="document-extraction-learning-group",
    version="1.0.0",
    description="A comprehensive repository for learning and experimenting with document extraction and OCR techniques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Document Extraction Learning Group",
    license="MIT",
    url="https://github.com/yourusername/document-extraction-learning-group",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "pillow>=10.0.0",
        "pyarrow>=12.0.0",
        "boto3>=1.28.0",
        "python-dotenv>=1.0.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "pytest>=7.4.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="document-extraction ocr invoice-processing machine-learning aws-bedrock claude-vision",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/document-extraction-learning-group/issues",
        "Source": "https://github.com/yourusername/document-extraction-learning-group",
        "Documentation": "https://github.com/yourusername/document-extraction-learning-group/tree/main/docs",
    },
)

