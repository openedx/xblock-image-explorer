import unittest

from lxml import etree

from ..utils import make_block


class TestImageExplorerBlock(unittest.TestCase):
    """
    Tests for XBlock Image Explorer.
    """
    def setUp(self):
        """
        Test case setup
        """
        super(TestImageExplorerBlock, self).setUp()
        self.image_url = 'http://example.com/test.jpg'
        self.image_explorer_description = '<p>Test Descrption</p>'
        self.image_explorer_xml = """
            <image_explorer schema_version='1'>
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

        self.image_explorer_xml_version3 = """
            <image_explorer schema_version='3'>
                <background src='{0}' />
                <description>{1}</description>
                <hotspots>
                    <hotspot x='370' y='20' item-id='hotspotA'>
                        <feedback>
                            <header><p>Test Header</p></header>
                            <body><p>Test Body</p></body>
                        </feedback>
                    </hotspot>
                </hotspots>
            </image_explorer>
            """.format(self.image_url, self.image_explorer_description)

        self.image_explorer_block = make_block(self.image_explorer_xml)
        self.maxDiff = None

    def test_student_view_data(self):
        """
        Test the student_view_data results.
        """
        xmltree = etree.fromstring(self.image_explorer_xml)
        hotspots = self.image_explorer_block._get_hotspots(xmltree)
        expected_image_explorer_data = {
            'description': self.image_explorer_description,
            'background': {
                'src': self.image_url,
                'height': None,
                'width': None
            },
            'hotspots': hotspots,
        }

        student_view_data = self.image_explorer_block.student_view_data()
        self.assertEqual(student_view_data, expected_image_explorer_data)

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
        image_explorer_block_schema2 = make_block(self.image_explorer_xml_version2)

        # for schema version 1 hotsport coordinates are not centered
        self.assertFalse(self.image_explorer_block.hotspot_coordinates_centered)

        # for schema version 2 hotspot coordinates are centered
        self.assertTrue(image_explorer_block_schema2.hotspot_coordinates_centered)
