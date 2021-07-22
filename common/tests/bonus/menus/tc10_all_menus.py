""" Base Test for UnitTests; uses a parameter that passes dictionary of properties """
import unittest
from common.base_tests.gui_basetest import BaseTest
from common.pages.returnly.menus import Menus
from common.constants import log_message
from common.common_actions import navigate_to

class TC10(BaseTest):
    """
    Verify product menu
    """
    def test_validate_all_menus(self):
        """
        test methods names should start with "test_"
        :return:
        """
        navigate_to(self.driver, "https://returnly.com/")
        menu_page = Menus(self.driver)
        for item in menu_page.menu:
            log_message(f"validate menu {item}")
            menu_page.validate_menu(item)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
