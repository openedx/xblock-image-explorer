import types

from xblockutils.base_test import SeleniumXBlockTest
from xblockutils.resources import ResourceLoader

from image_explorer.utils import load_scenario_xml_data

loader = ResourceLoader(__name__)


class TestImageExplorerBase(SeleniumXBlockTest):
    module_name = __name__
    default_css_selector = 'div.image-explorer-xblock-wrapper'

    def load_xml_data(self, scenario):
        self.set_scenario_xml(load_scenario_xml_data(scenario))

    def assert_page_content(self, block):
        self.assertIn("Image Explorer", block.text)
        self.assertIn("Enjoy using the Image Explorer.", block.description.text)
        self.assertIn("Click around the MIT Dome and see what you find!", block.description.text)

    def hotspots(self, block):
        hotspots = block.find_elements_by_css_selector(".image-explorer-hotspot")
        for h in hotspots:
            h.content = h.find_element_by_css_selector(".image-explorer-hotspot-reveal")
            h.close_button = h.find_element_by_css_selector(".image-explorer-close-reveal")
            h.is_clickable = types.MethodType(lambda s: s.is_displayed() and s.is_enabled(), h, type(h))
        return {h.get_attribute("data-item-id"): h for h in hotspots}

    def decorate_block(self, block):
        hotspots = self.hotspots(block)
        block.hotspotA = hotspots["hotspotA"]
        block.hotspotB = hotspots["hotspotB"]
        block.background = block.find_element_by_css_selector(".image-explorer-background")
        block.description = block.find_element_by_css_selector(".image-explorer-description")

        self.assert_page_content(block)

        return block

    def assert_in_default_state(self, block):
        self.wait_until_hidden(block.hotspotA.content)
        self.wait_until_hidden(block.hotspotB.content)
        self.assertTrue(block.hotspotA.is_clickable())
        self.assertTrue(block.hotspotB.is_clickable())

    def assert_only_hotspotA_revealed(self, block):
        self.wait_until_clickable(block.hotspotA.content)
        self.wait_until_hidden(block.hotspotB.content)
        self.assertTrue(block.hotspotA.is_clickable())
        self.assertTrue(block.hotspotB.is_clickable())

        self.assertIn("This is where many pranks take place.", block.hotspotA.content.text)
        self.assertIn("Below are some of the highlights:", block.hotspotA.content.text)
        self.assertIn("Once there was a police car up here", block.hotspotA.content.text)
        self.assertIn("Also there was a Fire Truck put up there", block.hotspotA.content.text)

    def assert_only_hotspotB_revealed(self, block):
        self.wait_until_hidden(block.hotspotA.content)
        self.wait_until_clickable(block.hotspotB.content)
        self.assertTrue(block.hotspotA.is_clickable())
        self.assertTrue(block.hotspotB.is_clickable())

        self.assertIn("Watch the Red Line subway go around the dome", block.hotspotB.content.text)
        self.assertTrue(block.hotspotB.find_element_by_css_selector(".image-explorer-hotspot-reveal-youtube"))


class TestImageExplorerV1(TestImageExplorerBase):

    def test_simple_scenario(self):
        self.load_xml_data('image_explorer_v1')
        view = self.go_to_view()
        block = self.decorate_block(view)

        self.assert_in_default_state(block)

        block.hotspotA.click()
        self.assert_only_hotspotA_revealed(block)

        block.hotspotA.content.click()
        self.assert_only_hotspotA_revealed(block)

        block.hotspotA.close_button.click()
        self.assert_in_default_state(block)

        block.hotspotB.click()
        self.assert_only_hotspotB_revealed(block)

        block.hotspotB.content.click()
        self.assert_only_hotspotB_revealed(block)

        block.description.click()
        self.assert_in_default_state(block)

        block.hotspotA.click()
        self.assert_only_hotspotA_revealed(block)

        block.hotspotB.click()
        self.assert_only_hotspotB_revealed(block)

        block.hotspotB.close_button.click()
        self.assert_in_default_state(block)

        block.hotspotB.click()
        self.assert_only_hotspotB_revealed(block)

        block.hotspotA.click()
        self.assert_only_hotspotA_revealed(block)

        block.background.click()
        self.assert_in_default_state(block)


class TestImageExplorerV2(TestImageExplorerBase):
    def test_simple_scenario(self):
        self.load_xml_data('image_explorer_v2')
        view = self.go_to_view()
        block = self.decorate_block(view)
        popup = block.find_element_by_css_selector("#hide-tutorial")
        popup.click()

        self.assert_in_default_state(block)

        block.hotspotA.click()
        self.assert_only_hotspotA_revealed(block)

        block.hotspotA.content.click()
        self.assert_only_hotspotA_revealed(block)

        block.hotspotA.close_button.click()
        self.assert_in_default_state(block)

        block.hotspotB.click()
        self.assert_only_hotspotB_revealed(block)

        block.hotspotB.content.click()
        self.assert_only_hotspotB_revealed(block)

        block.description.click()
        self.assert_in_default_state(block)

        block.hotspotA.click()
        self.assert_only_hotspotA_revealed(block)

        block.hotspotB.click()
        self.assert_only_hotspotB_revealed(block)

        block.hotspotB.close_button.click()
        self.assert_in_default_state(block)

        block.hotspotB.click()
        self.assert_only_hotspotB_revealed(block)

        block.hotspotA.click()
        self.assert_only_hotspotA_revealed(block)

        block.background.click()
        self.assert_in_default_state(block)
