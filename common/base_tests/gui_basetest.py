""" Base Test for UnitTests; uses a parameter that passes dictionary of properties """
import unittest
import os

from common.browser_init import LocalBrowserInit
from common.common_actions import check_failed_assertions
from common.common_actions import save_screenshot
from common.constants import get_all_properties
from common.constants import log_message
from common.constants import DEFAULT_PROPERTIES
from common.pages.login import LoginPage

class BaseTest(unittest.TestCase):
    """
    All GUI tests are expected to use it as a superclass
    """

    def setUp(self):
        """
        Default setup for the tests using dictionary of properties from environment variable PARAMS
        If driver is set, open either local or SauceLabs driver
        :return:
        """
        log_message("*********************** setUp ***********************")
        self.props = get_all_properties(
            eval(os.environ.get("PARAMS", "{}")), "INFO", default=DEFAULT_PROPERTIES)
        log_message("*********************** core testing ***********************")
        self.driver = LocalBrowserInit().get_driver()
        LoginPage(self.driver).login()

    def tearDown(self):
        """
        If driver was specified(and opened in setUp), close it
        :param self:
        :return:
        """
        log_message("*********************** tearDown ***********************")
        if self.driver:
            try:
                save_screenshot(self.driver, "final")
            except:
                pass
            log_message("Closing webdriver")
            self.driver.quit()
        check_failed_assertions()
