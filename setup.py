# -*- coding: utf-8 -*-

# Imports ###########################################################

import os
from setuptools import setup


# Functions #########################################################

def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


# Main ##############################################################

setup(
    name='xblock-image-explorer',
    version='1.1.4',
    description='XBlock - Image Explorer',
    packages=['image_explorer'],
    install_requires=[
        'XBlock>=1.2',
    ],
    entry_points={
        'xblock.v1': 'image-explorer = image_explorer:ImageExplorerBlock',
    },
    package_data=package_data("image_explorer", ["static", "templates", "public", "translations"]),
)
