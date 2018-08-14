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
    name='xblock-image-explorer-v2',
    version='1.99.0',
    description='XBlock - Image Explorer v2',
    packages=['image_explorer_v2'],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': 'image-explorer-v2 = image_explorer_v2:ImageExplorerBlock',
    },
    package_data=package_data("image_explorer_v2", ["static", "templates", "public", "translations"]),
)
