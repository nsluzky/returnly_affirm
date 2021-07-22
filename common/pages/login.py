""" Objects and methods of Login Page"""
from selenium.webdriver.common.by import By

from common.named_by import NamedBy
from common.common_actions import get_test_property
from common.common_actions import navigate_to

class LoginPage:
    """ Objects and methods of Login Page """
    def __init__(self, driver):
        self.driver = driver
        self.description = NamedBy(
            "Description", By.XPATH,
            "//p[@class='description']",
            self)
        self.enter_button = NamedBy(
            "Enter button", By.XPATH,
            "//button[@type='submit']",
            self)
        self.login_for_store_owner = NamedBy(
            "Login for store owner", By.XPATH,
            "//a[contains(@href, 'admin')]",
            self)
        self.logo = NamedBy(
            "Logo", By.XPATH,
            "//div[@class='hero']",
            self)
        self.password = NamedBy(
            "Password", By.XPATH,
            "//input[@name='password']",
            self)

    def login(self):
        """
        login using password
        :return:
        """
        navigate_to(self.driver, get_test_property('baseurl'))
        self.password.enter(get_test_property('password'))
        self.enter_button.click()
