# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import pathlib

import pkg_resources
from setuptools import find_packages, setup

from build_helpers.build_helpers import (
    BuildPyCommand,
    CleanCommand,
    Develop,
    SDistCommand,
    find_version,
)

with pathlib.Path("requirements/requirements.txt").open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

print(find_packages(include=["pykit"]))
with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        cmdclass={
            "clean": CleanCommand,
            "sdist": SDistCommand,
            "build_py": BuildPyCommand,
            "develop": Develop,
        },
        name="pykit",
        version=find_version("pykit", "__init__.py"),
        author="Song Tao",
        author_email="1556824234@qq.com",
        description="A framework for python microservices base on grpc",
        license="MIT",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/hotttao/gostock/tree/master/pykit",
        keywords="python grcp microservices framework",
        packages=find_packages(include=["pykit"]),
        include_package_data=True,
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
        ],
        install_requires=install_requires,
        entry_points={
            'console_scripts': [

            ]
        },
        # data_files=[
        #     ('', ['pykit/config/*.yaml']),
        # ],
        package_data={
            '': ['pykit/config/*.yaml']
        }
        # Install development dependencies with
        # pip install -r requirements/dev.txt -e .
    )
