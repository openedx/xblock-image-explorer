# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging
import textwrap
from lxml import etree
from xml.etree import ElementTree as ET

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from StringIO import StringIO

from .utils import render_template, AttrDict, load_resource


# Globals ###########################################################

log = logging.getLogger(__name__)


# Classes ###########################################################

class ImageExplorerBlock(XBlock):
    """
    XBlock providing a video player for videos hosted on Brightcove
    """
    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Image Explorer"
    )

    data = String(help="XML contents to display for this module", scope=Scope.content, default=textwrap.dedent("""\
        <image_explorer schema_version='1'>
            <background src="//upload.wikimedia.org/wikipedia/commons/thumb/a/ac/MIT_Dome_night1_Edit.jpg/800px-MIT_Dome_night1_Edit.jpg" />
            <description>
                <p>
                    Enjoy using the Image Explorer. Click around the MIT Dome and see what you find!
                </p>
            </description>
            <hotspots>
                <hotspot x='370' y='20'>
                    <feedback width='300' height='240'>
                        <header>
                            <p>
                                This is where many pranks take place. Below are some of the highlights:
                            </p>
                        </header>
                        <body>
                            <ul>
                                <li>Once there was a police car up here</li>
                                <li>Also there was a Fire Truck put up there</li>
                            </ul>
                        </body>
                    </feedback>
                </hotspot>
                <hotspot x='250' y='70'>
                    <feedback width='440' height='400'>
                        <header>
                            <p>
                                Watch the Red Line subway go around the dome
                            </p>
                        </header>
                        <youtube video_id='dmoZXcuozFQ' width='400' height='300' />
                    </feedback>
                </hotspot>
            </hotspots>
        </image_explorer>
        """))

    def student_view(self, context):
        """
        Player view, displayed to the student
        """

        xmltree = etree.fromstring(self.data)

        description = self._get_description(xmltree)
        hotspots = self._get_hotspots(xmltree)
        background = self._get_background(xmltree)

        for hotspot in hotspots:
            hotspot.reveal_style = 'style="{0}{1}"'.format(
                    'width: ' + hotspot.feedback.width + 'px;' if hotspot.feedback.width else '',
                    'height: ' + hotspot.feedback.height + 'px;' if hotspot.feedback.height else ''
                )

        sprite_url = self.runtime.local_resource_url(self, 'public/images/hotspot-sprite.png')

        context = {
            'title': self.display_name,
            'description_html': description,
            'hotspots': hotspots,
            'background': background,
            'sprite_url': sprite_url,
        }


        fragment = Fragment()
        fragment.add_content(render_template('/templates/html/image_explorer.html', context))
        fragment.add_css(load_resource('public/css/image_explorer.css'))
        fragment.add_javascript(load_resource('public/js/image_explorer.js'))

        fragment.initialize_js('ImageExplorerBlock')

        self.runtime.publish(self, 'image-explorer.problem.shown',
                {'component_id': self.scope_ids.usage_id, 'user_id': self.runtime.user_id}
        )

        return fragment

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(render_template('/templates/html/image_explorer_edit.html', {
            'self': self,
        }))
        fragment.add_javascript(load_resource('public/js/image_explorer_edit.js'))

        fragment.initialize_js('ImageExplorerEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):

        self.display_name = submissions['display_name']
        xml_content = submissions['data']

        try:
            etree.parse(StringIO(xml_content))
            self.data = xml_content
        except etree.XMLSyntaxError as e:
            return {
                'result': 'error',
                'message': e.message
            }

        return {
            'result': 'success',
        }

    def _get_background(self, xmltree):
        """
        Parse the XML to get the information about the background image
        """
        background = xmltree.find('background')
        return AttrDict({
            'src': background.get('src'),
            'width': background.get('width'),
            'height': background.get('height')
        })

    def _inner_content(self, tag):
        """
        Helper met
        """
        if tag is not None:
            return u''.join(ET.tostring(e) for e in tag)
        return None

    def _get_description(self, xmltree):
        """
        Parse the XML to get the description information
        """
        description = xmltree.find('description')
        if description is not None:
            return self._inner_content(description)
        return None

    def _get_hotspots(self, xmltree):
        """
        Parse the XML to get the hotspot information
        """
        hotspots_element= xmltree.find('hotspots')
        hotspot_elements = hotspots_element.findall('hotspot')
        hotspots = []
        for hotspot_element in hotspot_elements:
            feedback_element = hotspot_element.find('feedback')

            feedback = AttrDict()
            feedback.width = feedback_element.get('width')
            feedback.height = feedback_element.get('height')
            feedback.header = self._inner_content(feedback_element.find('header'))

            feedback.body = None
            body_element = feedback_element.find('body')
            if body_element is not None:
                feedback.type = 'text'
                feedback.body = self._inner_content(body_element)

            feedback.youtube = None
            youtube_element = feedback_element.find('youtube')
            if youtube_element is not None:
                feedback.type = 'youtube'
                feedback.youtube = AttrDict()
                feedback.youtube.video_id = youtube_element.get('video_id')
                feedback.youtube.width = youtube_element.get('width')
                feedback.youtube.height = youtube_element.get('height')

            hotspot = AttrDict()
            hotspot.feedback = feedback
            hotspot.x = hotspot_element.get('x')
            hotspot.y = hotspot_element.get('y')

            hotspots.append(hotspot)

        return hotspots

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [("Image explorer scenario", "<vertical_demo><image-explorer/></vertical_demo>")]
