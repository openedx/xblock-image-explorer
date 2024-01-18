import unittest
from mock import patch
from lxml import etree

from parsel import Selector

from django.test import override_settings
from xblock.field_data import DictFieldData

from image_explorer.image_explorer import ImageExplorerBlock
from .utils import MockRuntime, patch_static_replace_module
from image_explorer.utils import AttrDict


class TestImageExplorerBlock(unittest.TestCase):
    """
    Tests for XBlock Image Explorer.
    """
    def setUp(self):
        """
        Test case setup
        """
        super(TestImageExplorerBlock, self).setUp()
        self.runtime = MockRuntime()
        patch_static_replace_module()

        self.processed_absolute_url = 'https://lms/a/dynamic/url'
        self.image_url = '/static/test.jpg'
        self.image_explorer_description = '<p>Test Descrption</p><img src="/static/test.jpg" />'
        self.image_explorer_xml = """
            <image_explorer schema_version='1'>
                <background src='{0}' />
                <description>{1}</description>
                <hotspots>
                    <hotspot x='370' y='20' item-id='hotspotA'>
                        <feedback width='300' height='240'>
                            <header><p>Test Header</p></header>
                            <body>
                                <p>Test Body</p>
                                <img src="/static/test.jpg" />
                            </body>
                        </feedback>
                    </hotspot>
                </hotspots>
            </image_explorer>
            """.format(self.image_url, self.image_explorer_description)

        self.image_explorer_xml_version2 = """
            <image_explorer schema_version='2'>
                <background src='{0}' />
                <description>{1}</description>
                <hotspots>
                    <hotspot x='370' y='20' item-id='hotspotA'>
                        <feedback width='300' height='240'>
                            <header><p>Test Header</p></header>
                            <body><p>Test Body</p></body>
                        </feedback>
                    </hotspot>
                </hotspots>
            </image_explorer>
            """.format(self.image_url, self.image_explorer_description)

        self.image_explorer_data = {'data': self.image_explorer_xml}
        self.image_explorer_block = ImageExplorerBlock(
            self.runtime,
            DictFieldData(self.image_explorer_data),
            None
        )
        self.image_explorer_block.course_id = 'abc/xyz/123'

    @override_settings(ENV_TOKENS={'LMS_BASE': 'lms'}, HTTPS='on')
    def test_student_view_data(self):
        """
        Test the student_view_data results.
        """
        xmltree = etree.fromstring(self.image_explorer_xml)
        hotspots = self.image_explorer_block._get_hotspots(xmltree, absolute_urls=True)
        expected_image_explorer_data = {
            'description': self.image_explorer_block._get_description(xmltree, absolute_urls=True),
            'background': {
                'src': self.processed_absolute_url,
                'height': None,
                'width': None
            },
            'hotspots': hotspots,
        }

        student_view_data = self.image_explorer_block.student_view_data()
        self.assertEqual(student_view_data, expected_image_explorer_data)

    @override_settings(ENV_TOKENS={'LMS_BASE': 'lms'}, HTTPS='on')
    def test_static_urls_conversion(self):
        """
        Test static urls are processed to absolute if
        `absolute_urls` is set
        """
        xmltree = etree.fromstring(self.image_explorer_xml)
        description = self.image_explorer_block._inner_content(
            xmltree.find('description'), absolute_urls=True
        )

        relative_urls = Selector(text=description).css('::attr(href),::attr(src)').extract()
        for url in relative_urls:
            self.assertEqual(url, self.processed_absolute_url)

    def test_student_view_multi_device_support(self):
        """
        Test student_view multi device support is set
        """
        self.assertEqual(
            self.image_explorer_block.has_support(
                getattr(self.image_explorer_block, 'student_view', None),
                'multi_device'
            ),
            True
        )

    def test_hotspot_coordinates_property(self):
        """
        Test hotspot coordinates centered property for different schema versions
        """
        image_explorer_data = {'data': self.image_explorer_xml_version2}
        image_explorer_block_schema2 = ImageExplorerBlock(
            self.runtime,
            DictFieldData(image_explorer_data),
            None
        )

        # for schema version 1 hotsport coordinates are not centered
        self.assertFalse(self.image_explorer_block.hotspot_coordinates_centered)

        # for schema version 2 hotspot coordinates are centered
        self.assertTrue(image_explorer_block_schema2.hotspot_coordinates_centered)

    @patch('image_explorer.image_explorer.ImageExplorerBlock._inner_content')
    def test__get_hotspots(self, mock__inner_content):
        """
        Test _get_hotspots return all hotspots.
        """
        image_explorer_data = {'data': self.image_explorer_xml_version2}
        image_explorer_block_schema2 = ImageExplorerBlock(
            self.runtime,
            DictFieldData(image_explorer_data),
            None
        )
        hotspots = image_explorer_block_schema2._get_hotspots(xmltree=etree.fromstring(self.image_explorer_xml))
        self.assertEqual(len(hotspots), 1)
        self.assertFalse(hotspots[0].visited)
        image_explorer_block_schema2.opened_hotspots.append('hotspotA')
        hotspots = image_explorer_block_schema2._get_hotspots(xmltree=etree.fromstring(self.image_explorer_xml))
        self.assertEqual(len(hotspots), 1)
        self.assertTrue(hotspots[0].visited)

    def test_collect_video_elements(self):
        """
        Test video elements parsing
        """
        image_explorer_with_video = """
            <image_explorer schema_version='2'>
                <background src='{0}' />
                <description>{1}</description>
                <hotspots>
                    <hotspot x='370' y='20' item-id='hotspotA'>
                        <feedback width='300' height='240'>
                            <header><p>Test Header</p></header>
                            <body>
                                <p>Test Body</p>
                                <brightcove video_id="1234" account_id="789" width="320px" height="260px" />
                            </body>
                            <youtube video_id="dmoZXcuozFQ" width="400" height="300" />
                            <ooyala video_id="xyz123" width="400" height="300" />
                        </feedback>
                    </hotspot>
                </hotspots>
            </image_explorer>
            """.format(self.image_url, self.image_explorer_description)

        image_explorer_data = {'data': image_explorer_with_video}
        image_explorer_block = ImageExplorerBlock(
            self.runtime,
            DictFieldData(image_explorer_data),
            None
        )

        xmltree = etree.fromstring(image_explorer_with_video)
        hotspots_element = xmltree.find('hotspots')
        hotspot_with_videos = hotspots_element.findall('hotspot')[0]
        feedback = AttrDict()
        image_explorer_block._collect_video_elements(hotspot_with_videos, feedback)

        # check if feedback has video elements attached
        self.assertTrue('youtube' in feedback)
        self.assertEqual(feedback.youtube.video_id, 'dmoZXcuozFQ')
        self.assertTrue('bcove' in feedback)
        self.assertEqual(feedback.bcove.video_id, '1234')
