""" Objects and methods of menus of Returnly pages"""
import re
from selenium.webdriver.common.by import By

from common.named_by import NamedBy
from common.common_actions import log_message, assert_and_log

class Menus:
    """
    Describes objects and methods of Menus on Returnly pages
    """
    def __init__(self, driver):
        self.driver = driver
        container_xpath = "//ul[@id='menu-header-menu']"
        self.menu = {
            'Products': [
                'Overview',
                'Returns',
                'Exchanges',
                'Tracking',
                'Analytics',
                'Returnly Credit',
                'Green Returns',
                'International Returns',
                'In-Store Returns',
                'Returns Optimization',
            ],
            'Integrations': [
                'Integrations',
                'API',
            ],
            'Plans': [],
            'Customers': [],
            'Resources': [
                'Content Library',
                'Blog',
                'Help Center',
            ],
        }
        for item in self.menu:
            exec(f"self.{create_name(item)}"
                 f" = NamedBy('{item}', By.XPATH,"
                 f" container_xpath + \"//a[text()='{item}']\", self)")
            for subitem in self.menu[item]:
                exec(f"self.{create_name(subitem)}"
                     f" = NamedBy('{subitem}', By.XPATH,"
                     f" container_xpath + \"//a[text()='{subitem}']\", self)")
    def validate_menu(self, menu_name, wait_time=5):
        """
        Validate whether all submenu items are visible
        :param menu_name:
        :param wait_time:
        :return:
        """
        condition = f"'{menu_name}' in self.menu.keys()"
        assert_and_log(eval(condition), condition, continue_on_error=False)
        exec(f"self.{create_name(menu_name)}.click()")
        for subitem in self.menu[menu_name]:
            assert_and_log(
                eval(f"self.{create_name(subitem)}.find_visible_element(log_level='DEBUG',"
                     f" wait_time={wait_time})"),
                f'{subitem} is visible')


def create_name(display_name):
    """
    Create name of item out of its display name that might have spaces, dashes, ...
    :param display_name:
    :return:
    """
    return re.sub('[^0-9a-zA-Z_]', '_', display_name).lower()
