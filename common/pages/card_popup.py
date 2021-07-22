""" Objects and methods Related to Card Popup Page """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class CardPopupPage:
    """
    Describes objects and methods of  Card Popup Page
    """
    def __init__(self, driver):
        self.driver = driver
        self.close = NamedBy(
            "Close", By.XPATH,
            "//*[@class='cart-popup']//button[@class='cart-popup__close']",
            self)
        self.continue_shopping_button = NamedBy(
            "Continue shopping button", By.XPATH,
            "//*[@class='cart-popup']//button[@class='cart-popup__dismiss-button"
            " text-link text-link--accent']",
            self)
        self.desription = NamedBy(
            "Desription", By.XPATH,
            "//*[@class='cart-popup']//h3[@class='cart-popup-item__title']",
            self)
        self.image = NamedBy(
            "Image", By.XPATH,
            "//*[@class='cart-popup']//img[@class='cart-popup-item__image']",
            self)
        self.just_added_to_your_card = NamedBy(
            "Just Added To Your Card", By.XPATH,
            "//*[@class='cart-popup']//h2[@class='cart-popup__heading']",
            self)
        self.quantity = NamedBy(
            "Quantity", By.XPATH,
            "//*[@class='cart-popup']//div[@class='cart-popup-item__quantity']",
            self)
        self.size = NamedBy(
            "Size", By.XPATH,
            "//*[@class='cart-popup']//li[@class='product-details__item product-details__item--variant-option']",
            self)
        self.view_card = NamedBy(
            "View Card", By.XPATH,
            "//*[@class='cart-popup']//a[@class='cart-popup__cta-link btn btn--secondary-accent']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.close,
            self.continue_shopping_button,
            self.desription,
            self.image,
            self.just_added_to_your_card,
            self.quantity,
            self.size,
            self.view_card,
        ]
