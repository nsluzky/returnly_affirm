""" Objects and methods Related to PaymentPage """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class PaymentPage:
    """
    Describes objects and methods of PaymentPage
    """
    def __init__(self, driver):
        self.driver = driver
        self.address = NamedBy(
            "Address", By.XPATH,
            "//input[@name='checkout[shipping_address][address1]']",
            self)
        self.address2 = NamedBy(
            "Address", By.XPATH,
            "//input[@name='checkout[shipping_address][address2]']",
            self)
        self.city = NamedBy(
            "City", By.XPATH,
            "//input[@name='checkout[shipping_address][city]']",
            self)
        self.continue_to_shipping = NamedBy(
            "Continue to shipping", By.XPATH,
            "//span[@class='btn__content']",
            self)
        self.country_selector = NamedBy(
            "Country selector", By.XPATH,
            "//div[@class='field__caret']",
            self)
        self.email_or_mobile_phone_number_input = NamedBy(
            "Email or mobile phone number input", By.XPATH,
            "//input[@type='email']",
            self)
        self.first_name = NamedBy(
            "First name", By.XPATH,
            "//input[@id='checkout_shipping_address_first_name']",
            self)
        self.image = NamedBy(
            "Image", By.XPATH,
            "//div[@class='product-thumbnail ']",
            self)
        self.keep_me_up_to_date = NamedBy(
            "Keep me up to date", By.XPATH,
            "//input[@name='checkout[buyer_accepts_marketing]']",
            self)
        self.last_name = NamedBy(
            "Last Name", By.XPATH,
            "//input[@name='checkout[shipping_address][last_name]']",
            self)
        self.prices = NamedBy(
            "Prices", By.XPATH,
            "//span[@class='order-summary__emphasis skeleton-while-loading']",
            self)
        self.product_name = NamedBy(
            "Product name", By.XPATH,
            "//span[@class='product__description__name order-summary__emphasis']",
            self)
        self.quantity = NamedBy(
            "Quantity", By.XPATH,
            "//span[@class='product-thumbnail__quantity']",
            self)
        self.return_to_cart = NamedBy(
            "Return to cart", By.XPATH,
            "//span[@class='step__footer__previous-link-content']",
            self)
        self.save_this_info = NamedBy(
            "Save this info", By.XPATH,
            "//input[@name='checkout[remember_me]']",
            self)
        self.size = NamedBy(
            "Size", By.XPATH,
            "//span[@class='product__description__variant order-summary__small-text']",
            self)
        self.state_selector = NamedBy(
            "State selector", By.XPATH,
            "//div[@class='field__caret shown-if-js']",
            self)
        self.total = NamedBy(
            "Total", By.XPATH,
            "//span[@class='payment-due__price skeleton-while-loading--lg']",
            self)
        self.zip_code = NamedBy(
            "Zip code", By.XPATH,
            "//input[@name='checkout[shipping_address][zip]']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.address,
            self.address2,
            self.city,
            self.continue_to_shipping,
            self.country_selector,
            self.email_or_mobile_phone_number_input,
            self.first_name,
            self.image,
            self.keep_me_up_to_date,
            self.last_name,
            self.prices,
            self.product_name,
            #self.quantity,
            #self.return_to_cart, # missing on buy it now
            self.save_this_info,
            self.size,
            self.state_selector,
            self.total,
            self.zip_code,
        ]
