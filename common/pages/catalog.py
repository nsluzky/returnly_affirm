""" Objects and methods of Catalog page """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class CatalogPage:
    """
    Describes objects and methods of Catalog page
    """
    def __init__(self, driver):
        self.driver = driver
        self.product_prices = NamedBy(
            "Product prices", By.XPATH,
             "//dl[starts-with(@class,'price price--listing')]",
            self)
        self.cart = NamedBy(
            "Cart", By.XPATH,
            "//a[@class='site-header__icon site-header__cart']",
            self)
        self.catalog = NamedBy(
            "Catalog TAB", By.XPATH,
            "//*[text()='Catalog' and starts-with(@class, 'site-nav')]",
            self)
        self.email_address_input = NamedBy(
            "Email address input", By.XPATH,
            "//input[@name='contact[email]']",
            self)
        self.filter = NamedBy(
            "Filter Selector", By.XPATH,
            "//select[@name='FilterTags']",
            self)
        self.image = NamedBy(
            "Image", By.XPATH,
            "//*[@class='grid-view-item product-card']",
            self)
        self.home = NamedBy(
            "Home TAB", By.XPATH,
            "//*[text()='Home' and starts-with(@class, 'site-nav')]",
            self)
        self.number_of_products = NamedBy(
            "Number of products", By.XPATH,
            "//span[@class='filters-toolbar__product-count']",
            self)
        self.pages_range = NamedBy(
            "Pages range", By.XPATH,
            "//li[@class='pagination__text']",
            self)
        self.payment_options = NamedBy(
            "Payment options", By.XPATH,
            "//li[@class='payment-icon']",
            self)
        self.powered_by_shopify = NamedBy(
            "Powered by Shopify", By.XPATH,
            "//a[@href='https://www.shopify.com?utm_campaign=poweredby"
            "&utm_medium=shopify&utm_source=onlinestore']",
            self)
        self.previous_and_next_pages = NamedBy(
            "Previous and Next page buttons", By.XPATH,
            "//*[@class='btn btn--tertiary btn--narrow']",
            self)
        self.product_titles = NamedBy(
            "Product titles", By.XPATH,
            "//div[@class='h4 grid-view-item__title product-card__title']",
            self)
        self.search_button = NamedBy(
            "Search button", By.XPATH,
            "//button[@class='btn--link site-header__icon site-header__search-toggle"
            " js-drawer-open-top']",
            self)
        self.search_quick_link = NamedBy(
            "Search quick link", By.XPATH,
            "//a[contains(@href, 'search')]",
            self)
        self.site_logo = NamedBy(
            "Site Logo", By.XPATH,
            "//div[@class='h2 site-header__logo']",
            self)
        self.sort_by_label = NamedBy(
            "SORT BY label", By.XPATH,
            "//label[@for='SortBy']",
            self)
        self.sorting_order = NamedBy(
            "Sorting order selector", By.XPATH,
            "//select[@name='sort_by']",
            self)
        self.subscribe = NamedBy(
            "SUBSCRIBE span", By.XPATH,
            "//span[@class='newsletter__submit-text--large']",
            self)
        self.trademark = NamedBy(
            "Trademark", By.XPATH,
            "//small[@class='site-footer__copyright-content']",
            self)
        # fields that should be visible
        self.basic_validation_list = [
            self.cart,
            self.catalog,
            self.email_address_input,
            self.filter,
            self.image,
            self.home,
            self.number_of_products,
            self.previous_and_next_pages,
            self.pages_range,
            self.payment_options,
            self.powered_by_shopify,
            self.product_titles,
            self.sort_by_label,
            self.subscribe,
            self.search_button,
            self.search_quick_link,
            self.site_logo,
            self.sorting_order,
            self.product_prices,
            self.trademark,
        ]
