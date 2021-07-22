""" commands to manually start selenium for investigation """
import os
from pprint import pprint
from common.browser_init import LocalBrowserInit
from common.common_actions import *
from common.constants import *
from common.pages.login import LoginPage
from common.investigator import *
from random import randint
from common.pages.main_page import MainPage

from tools.random_strings import random_name
from common.base_tests.gui_basetest import BaseTest
from common.pages.catalog import CatalogPage
from common.pages.product import ProductPage
from common.pages.card import CardPage
from common.pages.card_popup import CardPopupPage
from common.pages.payment import PaymentPage
from common.pages.payment_review import PaymentReviewPage
from common.pages.payment_info import PaymentInfoPage

set_test_property("headless", False)
get_all_properties(eval(os.environ.get("PARAMS", "{}")), "INFO", default=DEFAULT_PROPERTIES)

driver = LocalBrowserInit().get_driver()
self = LoginPage(driver)
LoginPage(driver).login()

catalog_page = CatalogPage(self.driver)
product_page = ProductPage(self.driver)
payment_page = PaymentPage(self.driver)
payment_review_page = PaymentReviewPage(self.driver)
payment_info_page = PaymentInfoPage(self.driver)
catalog_page.catalog.click()
