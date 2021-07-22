""" Objects and methods Related to Shopping Card Page """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class CardPage:
    """
    Describes objects and methods of Shopping Card Page
    """
    def __init__(self, driver):
        self.driver = driver
        self.continue_shopping = NamedBy(
            "Continue shopping", By.XPATH,
            "//*[contains(text(),'Continue shopping')]",
            self)
        self.price_for_product = NamedBy(
            "Price for product", By.XPATH,
            "//td[@class='cart__final-price text-right small--hide']",
            self)
        self.product_image = NamedBy(
            "Product image", By.XPATH,
            "//img[@class='cart__image']",
            self)
        self.product_name = NamedBy(
            "Product Name", By.XPATH,
            "//div[@class='list-view-item__title']",
            self)
        self.qiantity = NamedBy(
            "Qiantity", By.XPATH,
            "//div[@class='cart__qty']",
            self)
        self.remove = NamedBy(
            "Remove", By.XPATH,
            "//a[contains(@href, 'cart/change')]",
            self)
        self.size = NamedBy(
            "Size", By.XPATH,
            "//ul[@class='product-details']",
            self)
        self.subtotal = NamedBy(
            "Subtotal", By.XPATH,
            "//span[@class='cart-subtotal__price']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.continue_shopping,
            self.price_for_product,
            self.product_image,
            self.product_name,
            self.qiantity,
            self.remove,
            self.size,
            self.subtotal,
        ]
