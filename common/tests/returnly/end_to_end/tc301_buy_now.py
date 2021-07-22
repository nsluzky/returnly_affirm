""" end-to-end test Buy It Now """
import unittest
from random import randint

from tools.random_strings import random_name
from common.base_tests.gui_basetest import BaseTest
from common.pages.catalog import CatalogPage
from common.pages.product import ProductPage
#from common.pages.card import CardPage
#from common.pages.card_popup import CardPopupPage
from common.pages.payment import PaymentPage
from common.pages.payment_review import PaymentReviewPage
from common.pages.payment_info import PaymentInfoPage

from common.common_actions import assert_and_log

class TC301(BaseTest):
    """
    Validating end-to-end scenario of buying one product
    """
    def test_validate_catalog_page(self):
        """
        test methods names should start with "test_"
        :return:
        """
        catalog_page = CatalogPage(self.driver)
        product_page = ProductPage(self.driver)
        payment_page = PaymentPage(self.driver)
        payment_review_page = PaymentReviewPage(self.driver)
        payment_info_page = PaymentInfoPage(self.driver)
        catalog_page.catalog.click()
        catalog_page.image.random_click()
        product = product_page.product.get_text()
        product_page.buy_it_now.click()
        payment_dic = {
            'address' : f'{randint(1, 99999)} {random_name(5, 8)}',
            'city' : "San Francisco",
            'email_or_mobile_phone_number_input' : random_name(8) + "@gmail.com",
            'last_name' : random_name(3, 12),
            'zip_code' : '94107',
        }
        if randint(0, 1):
            payment_dic['first_name'] = random_name(4, 16)
        if randint(0, 1):
            payment_dic['address2'] = random_name(5)
        for _ in payment_dic:
            exec(f"payment_page.{_}.enter(payment_dic['{_}'])")
        payment_page.continue_to_shipping.click()
        payment_review_page.product.get_text()
        assert_and_log(payment_review_page.product.get_text() == product,
                       "Selected product is displayed")
        if randint(0, 1):
            payment_review_page.change.click()
            payment_page.continue_to_shipping.click()
            assert_and_log(payment_review_page.product.get_text() == product,
                           "Selected product is displayed")
        payment_review_page.continue_to_payment.click()
        payment_info_page.full_address.get_text()
        # validate address
        for _ in ['address', 'city', 'zip_code']:
            assert_and_log(payment_dic[_] in payment_info_page.full_address.get_text(),
                           f"{_} in full address")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
