""" Base Test for UnitTests in environment xxx """
import os
from common.base_tests.gui_basetest import BaseTest as Base
from common.browser_init import LocalBrowserInit
from common.common_actions import set_test_property, log_message
from common.constants import get_all_properties, DEFAULT_PROPERTIES
from common.pages.login import LoginPage

class BaseTest(Base.TestCase):
    """
    All GUI tests in environment XXX are expected to use it as a superclass
    """
    def setUp(self):
        """
        Adjusted for environment XXX
        :return:
        """
        log_message("*********************** setUp for XXX ***********************")
        self.props = get_all_properties(
            eval(os.environ.get("PARAMS", "{}")), "INFO", default=DEFAULT_PROPERTIES)
        self.props['baseurl'] = "<XXX-specific-property>"
        self.props['baseurl_api'] = "<XXX-specific-property>"
        log_message("*********************** core testing ***********************")
        self.driver = LocalBrowserInit().get_driver()
        LoginPage(self.driver).login()
