""" Base Test for UnitTests; uses a parameter that passes dictionary of properties """
import unittest
import os
import re

from common.common_actions import check_failed_assertions
from common.constants import log_message
from common.constants import CLI_DEFAULT_PROPERTIES
from common.constants import get_all_properties

class BaseTest(unittest.TestCase):
    """
    All CLI tests are expected to use it as a superclass
    """

    def setUp(self):
        """
        Default setup for the tests using dictionary of properties from environment variable PARAMS
        :return:
        """
        log_message("*********************** setUp ***********************")
        self.props = get_all_properties(
            eval(os.environ.get("PARAMS", "{}")), "INFO", default=CLI_DEFAULT_PROPERTIES)
        os.environ["PARAMS"] = str(self.props)
        # set testname
        testid_pattern = ".*(TC[0-9]+)"
        if "test" not in self.props:
            self.props["test"] = self.__class__.__name__
            if re.match(testid_pattern, self.props["test"]):
                self.props["test"] = re.match(testid_pattern, self.props["test"]).group(1)

        log_message("*********************** core testing ***********************")

    def tearDown(self):
        """
        If driver was specified(and opened in setUp), close it
        :param self:
        :return:
        """
        log_message("*********************** tearDown ***********************")
        check_failed_assertions()
