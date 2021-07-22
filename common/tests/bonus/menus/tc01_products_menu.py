""" Base Test for UnitTests; uses a parameter that passes dictionary of properties """
import unittest
from common.base_tests.gui_basetest import BaseTest
from common.pages.returnly.menus import Menus
from common.common_actions import navigate_to

class TC01(BaseTest):
    """
    Verify product menu
    """
    def test_validate_product_menu(self):
        """
        test methods names should start with "test_"
        :return:
        """
        navigate_to(self.driver, "https://returnly.com/")
        Menus(self.driver).validate_menu("Products")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
