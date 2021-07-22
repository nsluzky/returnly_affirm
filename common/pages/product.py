""" Objects and methods Related to Product Page """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy
from common.common_actions import get_test_property

class ProductPage:
    """
    Describes objects and methods of a Product Page
    """
    URL = lambda name: f"{get_test_property('baseurl')}products/{name.replace(' ', '-').lower()}"
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart = NamedBy(
            "Add To Cart", By.XPATH,
            "//button[@name='add']",
            self)
        self.buy_it_now = NamedBy(
            "Buy It Now", By.XPATH,
            "//button[starts-with(@class,'shopify-payment-button')]",
            self)
        self.facebook = NamedBy(
            "Facebook", By.XPATH,
            "//a[@class='btn btn--small btn--share share-facebook']",
            self)
        self.page_title = NamedBy(
            "Page Title", By.XPATH,
            "//h1[@class='product-single__title']",
            self)
        self.pin_it = NamedBy(
            "Pin It", By.XPATH,
            "//a[@class='btn btn--small btn--share share-pinterest']",
            self)
        self.price = NamedBy(
            "Price", By.XPATH,
             "//*[@class='price__pricing-group']",
            self)
        self.product = NamedBy(
            "Product", By.XPATH,
            "//h1[@class='product-single__title']",
            self)
        self.size_selector = NamedBy(
            "Size selector", By.XPATH,
            "//select[@class='single-option-selector single-option-selector"
            "-product-template product-form__input']",
            self)
        self.tweet = NamedBy(
            "Tweet", By.XPATH,
            "//a[@class='btn btn--small btn--share share-twitter']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.add_to_cart,
            self.buy_it_now,
            self.facebook,
            self.page_title,
            self.pin_it,
            self.price,
            self.product,
            #self.size_selector, should not be present on all products
            self.tweet,
        ]
