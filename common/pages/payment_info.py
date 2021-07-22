""" Objects and methods Related to Payment info page """
from random import randint

from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class PaymentInfoPage:
    """
    Describes objects and methods of Payment info page
    """
    def __init__(self, driver):
        self.driver = driver
        self.alert = NamedBy(
            "Alert", By.XPATH,
            "//p[@class='notice__text']", # i.e. payment can't be processed
            self)
        self.change = NamedBy(
            "Change", By.XPATH,
            "//a[@class='link--small']",
            self)
        "//p[@class='notice__text']"
        self.contact = NamedBy(
            "Contact", By.XPATH,
            "//div[@class='review-block__content']",
            self)
        self.credit_card_number = NamedBy(
            "Credit Card number", By.XPATH,
            "//iframe[contains(@name, 'card-fields-number-mdbr9fklq7l')"
            " and contains(@name, '-scope-returnly-candidates') "
            "and contains(@name, '.myshopify.com')]",
            self)
        self.currency = NamedBy(
            "Currency", By.XPATH,
            "//span[@class='payment-due__currency remove-while-loading']",
            self)
        self.expiration_date = NamedBy(
            "Expiration date", By.XPATH,
            "//iframe[contains(@name, 'card-fields-expiry') "
            "and contains(@name, '-scope-returnly-candidates') "
            "and contains(@name, '.myshopify.com')]",
            self)
        self.full_address = NamedBy(
            "Full address", By.XPATH,
            "//address[@class='address address--tight']",
            self)
        self.name_on_card = NamedBy(
            "Name on card", By.XPATH,
            "//iframe[contains(@name, 'card-fields-name') "
            "and contains(@name, '-scope-returnly-candidates') "
            "and contains(@name, '.myshopify.com')]",
            self)
        self.notification = NamedBy(
            "Notification", By.XPATH,
            "//p[@class='notice__text']",
            self)
        self.pay_now = NamedBy(
            "Pay Now", By.XPATH,
            "//span[@class='btn__content']",
            self)
        self.prices = NamedBy(
            "Prices", By.XPATH,
            "//span[@class='order-summary__emphasis skeleton-while-loading']",
            self)
        self.product = NamedBy(
            "Product", By.XPATH,
            "//span[@class='product__description__name order-summary__emphasis']",
            self)
        self.quantity = NamedBy(
            "Quantity", By.XPATH,
            "//span[@class='product-thumbnail__quantity']",
            self)
        self.return_to_shipping = NamedBy(
            "Return to shipping", By.XPATH,
            "//span[@class='step__footer__previous-link-content']",
            self)
        self.same_as_shipping_address = NamedBy(
            "Same as shipping address", By.XPATH,
            "//input[@checked='checked']",
            self)
        self.security_code = NamedBy(
            "Security code", By.XPATH,
            "//iframe[contains(@name, 'card-fields-verification_value') "
            "and contains(@name, '-scope-returnly-candidates') "
            "and contains(@name, '.myshopify.com')]",
            self)
        self.shipping_price = NamedBy(
            "Shipping price", By.XPATH,
            "//span[@class='skeleton-while-loading order-summary__emphasis']",
            self)
        self.size = NamedBy(
            "Size", By.XPATH,
            "//span[@class='product__description__variant order-summary__small-text']",
            self)
        self.total_price = NamedBy(
            "Total price", By.XPATH,
            "//span[@class='payment-due__price skeleton-while-loading--lg']",
            self)
        self.use_a_different_billing_address = NamedBy(
            "Use a different billing address", By.XPATH,
            "//input[@id='checkout_different_billing_address_true']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.full_address,
            self.change,
            self.contact,
            self.credit_card_number,
            self.currency,
            self.expiration_date,
            self.full_address,
            self.name_on_card,
            self.notification,
            self.pay_now,
            self.prices,
            self.product,
            self.quantity,
            self.return_to_shipping,
            self.same_as_shipping_address,
            self.security_code,
            self.shipping_price,
            self.size,
            self.total_price,
            self.use_a_different_billing_address,
        ]
    def enter_bogus_payment(self, credit_card):
        """
        Enter bogus payment info and click PayNow
            Enter 1 to simulate a successful transaction
            Enter 2 to simulate a failed transaction
            Enter 3 to simulate an exception
        :param credit_card:
        :return:
        """
        dic = {
            # Enter 1 to simulate a successful transaction
            #       2 to simulate a failed transaction
            #       3 to simulate an exception
            "credit_card_number": credit_card,
            "expiration_date": f"{randint(10, 12)}/{randint(21, 30)}",  # any date in the future
            "name_on_card": "Bogus Gateway",
            "security_code": randint(100, 999)  # any 3 - digit number
        }
        for _ in dic:
            exec(f"self.{_}.enter(dic['{_}'])")
        self.pay_now.click()
