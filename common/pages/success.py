""" Objects and methods Related to Successful Order page """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class SuccessPage:
    """
    Describes objects and methods of Successful Order page
    """
    def __init__(self, driver):
        self.driver = driver
        self.card_ending = NamedBy(
            "card ending", By.XPATH,
            "//span[@class='payment-method-list__item__info']",
            self)
        self.continue_shopping = NamedBy(
            "Continue shopping", By.XPATH,
            "//span[@class='btn__content']",
            self)
        self.currency = NamedBy(
            "Currency", By.XPATH,
            "//span[@class='payment-due__currency remove-while-loading']",
            self)
        self.help = NamedBy(
            "Help", By.XPATH,
            "//p[@class='step__footer__info']",
            self)
        self.map = NamedBy(
            "Map", By.XPATH,
            "//iframe[@class='map__iframe']",
            self)
        self.order_number = NamedBy(
            "Order number", By.XPATH,
            "//span[@class='os-order-number']",
            self)
        self.prices = NamedBy(
            "Prices", By.XPATH,
            "//span[@class='order-summary__emphasis skeleton-while-loading']",
            self)
        self.quantity = NamedBy(
            "Quantity", By.XPATH,
            "//span[@class='product-thumbnail__quantity']",
            self)
        self.thank_you = NamedBy(
            "Thank you", By.XPATH,
            "//h2[@class='os-header__title']",
            self)
        self.title = NamedBy(
            "Title", By.XPATH,
            "//span[@class='product__description__name order-summary__emphasis']",
            self)
        self.total_price = NamedBy(
            "Total price", By.XPATH,
            "//span[@class='payment-due__price skeleton-while-loading--lg']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.card_ending,
            self.continue_shopping,
            self.currency,
            self.help,
            self.map,
            self.order_number,
            self.prices,
            self.quantity,
            self.thank_you,
            self.title,
            self.total_price,
        ]
