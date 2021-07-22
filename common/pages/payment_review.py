""" Objects and methods Related to Payment review page """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class PaymentReviewPage:
    """
    Describes objects and methods of Payment review page
    """
    def __init__(self, driver):
        self.driver = driver
        self.change = NamedBy(
            "Change", By.XPATH,
            "//a[@class='link--small']",
            self)
        self.continue_to_payment = NamedBy(
            "Continue to payment", By.XPATH,
            "//span[@class='btn__content']",
            self)
        self.currency = NamedBy(
            "Currency", By.XPATH,
            "//span[@class='payment-due__currency remove-while-loading']",
            self)
        self.full_address = NamedBy(
            "Full address", By.XPATH,
            "//address[@class='address address--tight']",
            self)
        self.prices = NamedBy(
            "Prices", By.XPATH,
            "//span[@class='order-summary__emphasis skeleton-while-loading']",
            self)
        self.product = NamedBy(
            "Product", By.XPATH,
            "//span[@class='product__description__name order-summary__emphasis']",
            self)
        self.return_to_information = NamedBy(
            "Return to information", By.XPATH,
            "//span[@class='step__footer__previous-link-content']",
            self)
        self.shipping_price = NamedBy(
            "Shipping price", By.XPATH,
            "//span[@class='skeleton-while-loading order-summary__emphasis']",
            self)
        self.size = NamedBy(
            "Size", By.XPATH,
            "//span[@class='product__description__variant order-summary__small-text']",
            self)
        self.total_label = NamedBy(
            "Total label", By.XPATH,
            "//span[@class='payment-due-label__total']",
            self)
        self.total_price = NamedBy(
            "Total price", By.XPATH,
            "//span[@class='payment-due__price skeleton-while-loading--lg']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.full_address,
            self.change,
            self.continue_to_payment,
            self.currency,
            self.full_address,
            self.prices,
            self.product,
            self.return_to_information,
            self.shipping_price,
            self.size,
            self.total_label,
            self.total_price,
        ]
