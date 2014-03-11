# -*- coding: utf-8 -*-

# Imports ###########################################################

import os
from setuptools import setup


# Functions #########################################################

def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


# Main ##############################################################

setup(
    name='xblock-image-explorer',
    version='0.1',
    description='XBlock - Image Explorer',
    packages=['image_explorer'],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': 'image-explorer = image_explorer:ImageExplorerBlock',
    },
)
