#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "Click>=7.0",
    "camelot-py",
    "pillow",
    "PyMuPDF",
    "opencv-python",
    "peewee",
    "psycopg2-binary",
    "tqdm",
    "click",
    "python-dotenv",
]

setup(
    author="Ivan Devyaterikov",
    author_email="9kin.github@mail.ru",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="exam-reader",
    entry_points={
        "console_scripts": [
            "exam_reader=exam_reader.cli:cli",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="exam_reader",
    name="exam_reader",
    packages=find_packages(include=["exam_reader", "exam_reader.*"]),
    test_suite="tests",
    url="https://github.com/9kin/exam_reader",
    version="0.1.0",
    zip_safe=False,
)
