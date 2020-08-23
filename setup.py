# -*- coding: utf-8 -*-
"""Setup pyhapi
Author  : Maajor
Email   : info@ma-yidong.com
"""
import io
import re

from setuptools import setup
from setuptools import find_packages

with io.open("README.md", "rt", encoding="utf8") as f:
    README = f.read()

with io.open("pyhapi/__init__.py", "rt", encoding="utf8") as f:
    VERSION = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="pyhapi",
    version=VERSION,
    url="https://github.com/maajor/pyhapi",
    project_urls={
        "Documentation": "https://pyhapi.readthedocs.io",
        "Code": "https://github.com/maajor/pyhapi",
        "Issue tracker": "https://github.com/maajor/pyhapi/issues",
    },
    license="MIT",
    author="Yidong Ma(Maajor)",
    author_email="info@ma-yidong.com",
    maintainer="Yidong Ma(Maajor)",
    maintainer_email="info@ma-yidong.com",
    description="A object-oriented python wrapper for houdini engine's C API",
    long_description=README,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    python_requires=">=3.6",
    setup_requires=['pytest-runner'],
    install_requires=['numpy>=1.15.0'],
    tests_require=['pytest', 'pytest-asyncio'],
    long_description_content_type="text/markdown",
)
