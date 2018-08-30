# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging
import pkg_resources

from django.template import Context, Template
from lxml import etree

from xblockutils.resources import ResourceLoader

log = logging.getLogger(__name__)
loader = ResourceLoader(__name__)


def _(text):
    """
    Dummy `gettext` replacement to make string extraction tools scrape strings marked for translation
    """
    return text


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load_scenario_xml_data(scenario):
    xmltree = etree.Element('image-explorer')
    xml = loader.load_unicode('../tests/scenarios/{}_data.xml'.format(scenario))
    xmltree.set('data', xml)
    return etree.tostring(xmltree)
