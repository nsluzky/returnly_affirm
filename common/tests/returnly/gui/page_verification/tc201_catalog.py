""" Navigate to catalog page and  validate its content """
import unittest
from common.base_tests.gui_basetest import BaseTest
from common.pages.catalog import CatalogPage
from common.common_actions import validate

class TC01(BaseTest):
    """
    Validate content of catalog page
    """
    def test_validate_catalog_page(self):
        """
        test methods names should start with "test_"
        :return:
        """
        page = CatalogPage(self.driver)
        page.catalog.click()
        validate(page.basic_validation_list)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
