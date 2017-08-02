import unittest
from lxml import etree

from xblock.field_data import DictFieldData

from image_explorer.image_explorer import ImageExplorerBlock
from ..utils import MockRuntime

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

        self.image_explorer_data = {'data': self.image_explorer_xml}
        self.image_explorer_block = ImageExplorerBlock(
            self.runtime,
            DictFieldData(self.image_explorer_data),
            None
        )

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
