""" Objects and methods common to most pages"""
from common.common_actions import log_message, assert_and_log

class MainPage:
    """
    Describes objects and methods related to MainPage Menu, Title, and url
    """
    def __init__(self, driver):
        self.driver = driver
    def assert_url_equals(self, expected):
        """
        Takes the current url and verifies whether it is equal to the expected one
        :param expected:
        :return:
        """
        url = self.driver.current_url.lower()
        assert_and_log(
            url == expected.lower(),
            "url '{}' = '{}'".format(url, expected),
            True)
    def assert_url_contains(self, expected):
        """
        Takes the current url and verifies whether it contains the expected string
        :param expected:
        :return:
        """
        url = self.driver.current_url
        assert_and_log(
            url.lower().find(expected.lower()) > -1,
            "url '{}' contains '{}'".format(url, expected),
            True)
