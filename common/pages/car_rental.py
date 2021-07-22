""" Objects to find the best price for car renting """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class Cars:
    """
    Describes objects to find the best price for car renting
    """
    def __init__(self, driver):
        self.driver = driver
        self.total_price = NamedBy(
            "Totals", By.XPATH,
            "//span[@class='total-price']",
            self)
        self.reserve = NamedBy(
            "Reserve Button", By.XPATH,
            "//button[@name='textonly']",
            self)
