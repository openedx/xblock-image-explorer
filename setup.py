# -*- coding: utf-8 -*-

# Imports ###########################################################

from setuptools import setup


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
