#!/usr/bin/env python
# Copyright (C) 2020 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - https://cuckoosandbox.org/.
# See the file 'docs/LICENSE' for copying permission.

import setuptools
import sys

if sys.version[0] == "2":
    sys.exit(
        "The latest version of Cuckoo is Python >=3.6 only. Any Cuckoo version "
        "earlier than 3.0.0 supports Python 2."
    )

setuptools.setup(
    name="Cuckoo-common",
    version="0.1.0",
    author="Stichting Cuckoo Foundation",
    author_email="info@hatching.io",
    packages=setuptools.find_namespace_packages(include=["cuckoo.*"]),
    classifiers=[],
    python_requires=">=3.6",
    url="https://cuckoosandbox.org/",
    license="GPLv3",
    description="Cuckoo Sandbox common and utility code",
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "jinja2",
        "requests",
        "python-dateutil",
        "sflock",
        "sqlalchemy>=1.3.13, <1.4",
        "elasticsearch>=7.8.1, <8.0",
        "elasticsearch-dsl>=7.2.1, <7.3"
    ]
)
