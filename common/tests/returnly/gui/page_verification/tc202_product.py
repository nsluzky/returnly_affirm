""" Navigate to catalog page, click a random product and validate its page """
import unittest
from common.base_tests.gui_basetest import BaseTest
from common.pages.catalog import CatalogPage
from common.pages.product import ProductPage
from common.common_actions import validate

class TC02(BaseTest):
    """
    Validate content of catalog page
    """
    def test_validate_catalog_page(self):
        """
        test methods names should start with "test_"
        :return:
        """
        catalog_page = CatalogPage(self.driver)
        catalog_page.catalog.click()
        catalog_page.image.random_click()
        validate(ProductPage(self.driver).basic_validation_list)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
