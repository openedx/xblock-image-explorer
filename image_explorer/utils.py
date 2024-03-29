# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2015 Harvard, edX, OpenCraft
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3". If not, see <http://www.gnu.org/licenses/>.
#
"""
Image Explorer XBlock utils
"""

# Imports ###########################################################

from __future__ import absolute_import

import logging

try:
    from xblock.utils.resources import ResourceLoader
except ModuleNotFoundError:
    from xblockutils.resources import ResourceLoader


log = logging.getLogger(__name__)
loader = ResourceLoader(__name__)


def _(text):
    """
    Dummy `gettext` replacement to make string extraction tools scrape strings marked for translation
    """
    return text


class AttrDict(dict):
    """
    Attribute Dictionary for storing properties
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
