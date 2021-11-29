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
Image Explorer XBlock
"""

# Imports ###########################################################

from __future__ import absolute_import, division

import uuid
import logging
import textwrap
import pkg_resources
from six.moves import urllib
from six import StringIO
from parsel import Selector
from lxml import etree, html

from django.conf import settings

from xblock.completable import XBlockCompletionMode
from xblock.core import XBlock
from xblock.fragment import Fragment
from xblock.fields import List, Scope, String, Boolean

from .utils import loader, AttrDict, _


log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@XBlock.needs('i18n')
class ImageExplorerBlock(XBlock):  # pylint: disable=no-init
    """
    XBlock that renders an image with tooltips
    """

    has_score = True
    has_author_view = True
    completion_mode = XBlockCompletionMode.COMPLETABLE

    display_name = String(
        display_name=_("Display Name"),
        help=_("This name appears in the horizontal navigation at the top of the page."),
        scope=Scope.settings,
        default=_("Image Explorer")
    )

    _hotspot_coordinates_centered = Boolean(
        display_name=_("Hot Spots Coordinates Centered"),
        scope=Scope.settings,
        default=False,
    )

    opened_hotspots = List(
        help=_("Store hotspots opened by student, for completion"),
        default=[],
        scope=Scope.user_state,
    )

    data = String(help=_("XML contents to display for this module"), scope=Scope.content, default=textwrap.dedent("""\
        <image_explorer schema_version='2'>
            <background src="//upload.wikimedia.org/wikipedia/commons/thumb/a/ac/MIT_Dome_night1_Edit.jpg/800px-MIT_Dome_night1_Edit.jpg" />
            <description>
                <p>
                    Enjoy using the Image Explorer. Click around the MIT Dome and see what you find!
                </p>
            </description>
            <hotspots>
                <hotspot x='48.8125%' y='8.3162%' item-id='hotspotA'>
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
                <hotspot x='33.8125%' y='18.5831%' item-id="hotspotB">
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

    def max_score(self):  # pylint: disable=no-self-use
        """
        Returns the maximum score that can be achieved (always 1.0 on this XBlock)
        """
        return 1.0

    @property
    def hotspot_coordinates_centered(self):
        """
        Returns true if the hotspot coordinates are centered
        """
        if self._hotspot_coordinates_centered:
            return True

        # hotspots are calculated from center for schema version > 1
        xmltree = etree.fromstring(self.data)
        schema_version = int(xmltree.attrib.get('schema_version', 1))

        return schema_version > 1

    def author_view(self, context=None):
        """
        Renders the Studio preview view.
        """
        return self.student_view(context, authoring=True)

    @XBlock.supports("multi_device")  # Mark as mobile-friendly
    def student_view(self, context, authoring=False):
        """
        Player view, displayed to the student
        """

        xmltree = etree.fromstring(self.data)

        description = self._get_description(xmltree)
        hotspots = self._get_hotspots(xmltree)
        background = self._get_background(xmltree)
        has_youtube = False
        has_ooyala = False

        for hotspot in hotspots:
            width = 'width:{0}px'.format(hotspot.feedback.width) if hotspot.feedback.width else 'width:300px'
            height = 'height:{0}px'.format(hotspot.feedback.height) if hotspot.feedback.height else ''
            max_height = ''
            if not hotspot.feedback.height:
                max_height = 'max-height:{0}px'.format(hotspot.feedback.max_height) if \
                             hotspot.feedback.max_height else 'max-height:300px'

            hotspot.reveal_style = 'style="{0};{1};{2}"'.format(width, height, max_height)
            if hotspot.feedback.youtube:
                has_youtube = True

            if hotspot.feedback.ooyala:
                has_ooyala = True

        context = {
            'title': self.display_name,
            'hotspot_coordinates_centered': self.hotspot_coordinates_centered,
            'description_html': description,
            'hotspots': hotspots,
            'background': background,
            'ie_uid': uuid.uuid4().hex[:15],
        }

        fragment = Fragment()
        fragment.add_content(
            loader.render_django_template(
                '/templates/html/image_explorer.html',
                context=context,
                i18n_service=self.runtime.service(self, 'i18n')
            )
        )
        hotspot_image_url = self.runtime.local_resource_url(self, 'public/images/hotspot-sprite.png')
        fragment.add_css(self.resource_string('public/css/image_explorer.css'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/image_explorer.js'))
        if has_youtube:
            fragment.add_javascript_url('https://www.youtube.com/iframe_api')

        if has_ooyala:
            fragment.add_javascript_url(
                '//player.ooyala.com/core/10efd95b66124001b415aa2a4bee29c8?plugins=main,bm'
            )
            fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/ooyala_player.js'))

        fragment.initialize_js('ImageExplorerBlock', {'hotspot_image': hotspot_image_url,
                                                      'authoring_view': 'true' if authoring else 'false'})

        return fragment

    def student_view_data(self, context=None):
        """
        Returns a JSON representation of the Image Explorer Xblock, that can be
        retrieved using Course Block API.
        """
        xmltree = etree.fromstring(self.data)

        description = self._get_description(xmltree, absolute_urls=True)
        background = self._get_background(xmltree)
        background['src'] = self._replace_static_from_url(background['src'])
        hotspots = self._get_hotspots(xmltree, absolute_urls=True)
        return {
            'description': description,
            'background': background,
            'hotspots': hotspots,
        }

    @XBlock.json_handler
    def publish_event(self, data, suffix=''):
        """
        Override XBlock method to publish event when an action is taken on the
        block. This is used to register student progress.
        """
        try:
            event_type = data.pop('event_type')
        except KeyError:
            return {'result': 'error', 'message': self.ugettext('Missing event_type in JSON data')}

        data['user_id'] = self.scope_ids.user_id
        data['component_id'] = self._get_unique_id()
        self.runtime.publish(self, event_type, data)

        if event_type == 'xblock.image-explorer.hotspot.opened':
            self.register_progress(data['item_id'])

        return {'result': 'success'}

    def register_progress(self, hotspot_id):
        """
        Registers the completion of an hotspot, identified by id
        """
        xmltree = etree.fromstring(self.data)
        hotspots_ids = [h.item_id for h in self._get_hotspots(xmltree)]

        if not hotspots_ids \
                or hotspot_id not in hotspots_ids \
                or hotspot_id in self.opened_hotspots:
            return

        self.runtime.publish(self, 'progress', {})
        self.opened_hotspots.append(hotspot_id)
        log.debug(u'Opened hotspots so far for %s: %s', self._get_unique_id(), self.opened_hotspots)

        opened_hotspots = [h for h in hotspots_ids if h in self.opened_hotspots]
        percent_completion = float(len(opened_hotspots)) / len(hotspots_ids)
        self.runtime.publish(self, 'grade', {
            'value': percent_completion,
            'max_value': 1,
        })
        log.debug(u'Sending grade for %s: %s', self._get_unique_id(), percent_completion)

    def _get_unique_id(self):
        try:
            unique_id = self.location.name
        except AttributeError:
            # workaround for xblock workbench
            unique_id = 'workbench-workaround-id'
        return unique_id

    def studio_view(self, context):
        """
        Editing view in Studio
        """
        fragment = Fragment()
        fragment.add_content(loader.render_django_template('/templates/html/image_explorer_edit.html',
                                                           context={'self': self},
                                                           i18n_service=self.runtime.service(self, 'i18n')))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/image_explorer_edit.js'))

        fragment.initialize_js('ImageExplorerEditBlock')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):
        """
        Handle the action of the submit button when using the block from Studio
        """
        self.display_name = submissions['display_name']
        if submissions.get('hotspot_coordinates_centered', False):
            self._hotspot_coordinates_centered = True

        xml_content = submissions['data']

        try:
            etree.parse(StringIO(xml_content))
            self.data = xml_content
        except etree.XMLSyntaxError as err:
            # Python 2 and 3 compatibility fix
            # Switch to _, error_message = e.args
            try:
                error_message = err.message  # pylint: disable=exception-message-attribute
            except:  # pylint: disable=bare-except
                _, error_message = err.args

            return {
                'result': 'error',
                'message': error_message,
            }

        return {
            'result': 'success',
        }

    @staticmethod
    def _get_background(xmltree):
        """
        Parse the XML to get the information about the background image
        """
        background = xmltree.find('background')
        return AttrDict({
            'src': background.get('src'),
            'width': background.get('width'),
            'height': background.get('height')
        })

    def _replace_static_from_url(self, url):
        if not url:
            return url
        try:
            from common.djangoapps.static_replace import replace_static_urls
        except ImportError:
            return url

        url = '"{}"'.format(url)
        lms_relative_url = replace_static_urls(url, course_id=self.course_id)  # pylint: disable=no-member
        lms_relative_url = lms_relative_url.strip('"')
        return self._make_url_absolute(lms_relative_url)

    @staticmethod
    def _make_url_absolute(url):
        lms_base = settings.ENV_TOKENS.get('LMS_BASE')
        scheme = 'https' if settings.HTTPS == 'on' else 'http'
        lms_base = '{}://{}'.format(scheme, lms_base)
        return urllib.parse.urljoin(lms_base, url)

    def _inner_content(self, tag, absolute_urls=False):
        """
        Helper met
        """
        if tag is not None:
            tag_content = ''.join([ html.tostring(e, encoding=str) for e in tag ])
            if absolute_urls:
                return self._change_relative_url_to_absolute(tag_content)
            return tag_content
        return None

    def _get_description(self, xmltree, absolute_urls=False):
        """
        Parse the XML to get the description information
        """
        description = xmltree.find('description')
        if description is not None:
            description = self._inner_content(description, absolute_urls)
            return description
        return None

    def _change_relative_url_to_absolute(self, text):
        if text:
            relative_urls = Selector(text=text).css('::attr(href),::attr(src)').extract()
            for url in relative_urls:
                text = text.replace(url, self._replace_static_from_url(url))
        return text

    def _get_hotspots(self, xmltree, absolute_urls=False):
        """
        Parse the XML to get the hotspot information
        """
        hotspots_element = xmltree.find('hotspots')
        hotspot_elements = hotspots_element.findall('hotspot')
        hotspots = []
        for index, hotspot_element in enumerate(hotspot_elements):
            feedback_element = hotspot_element.find('feedback')

            feedback = AttrDict()
            feedback.width = feedback_element.get('width')
            feedback.height = feedback_element.get('height')
            feedback.max_height = feedback_element.get('max-height')
            feedback.header = self._inner_content(feedback_element.find('header'), absolute_urls)
            feedback.side = hotspot_element.get('side', 'auto')

            feedback.body = None
            body_element = feedback_element.find('body')
            if body_element is not None:
                feedback.type = 'text'
                feedback.body = self._inner_content(body_element, absolute_urls)

            self._collect_video_elements(hotspot_element, feedback)

            hotspot = AttrDict()
            hotspot.item_id = hotspot_element.get('item-id')
            if hotspot.item_id is None:
                hotspot.item_id = 'hotspot' + str(index)
            hotspot.feedback = feedback

            hotspot.x = hotspot_element.get('x')
            if not hotspot.x.endswith('%'):
                hotspot.x += 'px'  # px is deprecated as it is not responsive

            hotspot.y = hotspot_element.get('y')
            if not hotspot.y.endswith('%'):
                hotspot.y += 'px'  # px is deprecated as it is not responsive

            hotspot.visited = hotspot.item_id in self.opened_hotspots

            hotspots.append(hotspot)

        return hotspots

    @staticmethod
    def _collect_video_elements(hotspot, feedback):
        """
        Parses and includes video elements contained in the hotspot
        """
        feedback_element = hotspot.find('feedback')

        feedback.youtube = None
        youtube_element = feedback_element.find('youtube')
        if youtube_element is not None:
            feedback.type = 'youtube'
            feedback.youtube = AttrDict()
            feedback.youtube.id = 'youtube-{}'.format(uuid.uuid4().hex)
            feedback.youtube.video_id = youtube_element.get('video_id')
            feedback.youtube.width = youtube_element.get('width')
            feedback.youtube.height = youtube_element.get('height')

        feedback.ooyala = None
        ooyala_element = feedback_element.find('ooyala')
        if ooyala_element is not None:
            feedback.type = 'ooyala'
            feedback.ooyala = AttrDict()
            feedback.ooyala.id = 'oo-{}'.format(uuid.uuid4().hex)
            feedback.ooyala.video_id = ooyala_element.get('video_id')
            feedback.ooyala.width = ooyala_element.get('width')
            feedback.ooyala.height = ooyala_element.get('height')

        # BC element could be anywhere in the hotspot
        bcove_element = hotspot.find(".//brightcove")
        if bcove_element is not None:
            feedback.bcove = AttrDict()
            feedback.bcove.id = 'bcove-{}'.format(uuid.uuid4().hex)
            feedback.bcove.video_id = bcove_element.get('video_id')
            feedback.bcove.account_id = bcove_element.get('account_id')
            feedback.bcove.width = bcove_element.get('width')
            feedback.bcove.height = bcove_element.get('height')

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [("Image explorer scenario", "<vertical_demo><image-explorer/></vertical_demo>")]

    def resource_string(self, path):  # pylint: disable=no-self-use
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")
