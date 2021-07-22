""" end-to-end test Buy It Now old and newly created product """
import unittest
from random import randint

from tools.random_strings import random_name
from common.base_tests.gui_basetest import BaseTest
from common.pages.catalog import CatalogPage
from common.pages.product import ProductPage
from common.pages.payment import PaymentPage
from common.pages.payment_review import PaymentReviewPage
from common.pages.payment_info import PaymentInfoPage
from common.pages.success import SuccessPage

from common.data._impoved import *
from common.common_actions import assert_and_log, back
from common.common_actions import navigate_to
from common.common_actions import validate

from common.process_request import ProcessRequest

class TC303(BaseTest):
    """
    Validating end-to-end scenario of buying one product
    """
    def setUp(self):
        """
        Create a new product for the scenario
        It would be deleted at the tearDown
        :return:
        """
        super().setUp()
        list_of_product_types = [
            'default_product_variant',
            'multiple_product_variants',
            'ceo_title'
        ]
        self.new_product = eval(f"get_new_product_with_" \
               f"{list_of_product_types[randint(0, len(list_of_product_types) - 1)]}()")
        response = ProcessRequest('products.json').send_request(
            'POST',
            data=self.new_product,
            expected_return_codes=[201],
        )
        self.product_id = response.response['product']['id']
    def test_buy_now(self):
        """
        Create a new product and buy it along with existing one
        :return:
        """
        catalog_page = CatalogPage(self.driver)
        product_page = ProductPage(self.driver)
        payment_page = PaymentPage(self.driver)
        payment_review_page = PaymentReviewPage(self.driver)
        payment_info_page = PaymentInfoPage(self.driver)
        success_page = SuccessPage(self.driver)
        # buy the new product
        navigate_to(self.driver, ProductPage.URL(self.new_product['product']['title']))
        product = product_page.product.get_text()
        product_page.buy_it_now.click()
        assert_and_log(payment_info_page.product.get_text() == product,
                       f"{product} is in the order")
        assert_and_log(len(payment_info_page.product.find_visible_elements()) == 1,
                       "there is only 1 item in the order")
        payment_info_page.product.get_text()
        # by an old product
        back(self.driver)
        catalog_page.catalog.click()
        # Sort products to move the newly created to last page
        catalog_page.sorting_order.select_by_visible_text("Date, old to new")
        catalog_page.image.random_click()
        product = product_page.product.get_text()
        product_page.buy_it_now.click()
        assert_and_log(payment_info_page.product.get_text() == product,
                       f"{product} is in the order")
        assert_and_log(len(payment_info_page.product.find_visible_elements()) == 1,
                       "there is only 1 item in the order")
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
        payment_review_page.continue_to_payment.click()
        payment_info_page.full_address.get_text()
        # validate address
        for _ in ['address', 'city', 'zip_code']:
            assert_and_log(payment_dic[_] in payment_info_page.full_address.get_text(),
                           f"{_} in full address")
        payment_info_page.enter_bogus_payment(1)
        assert_and_log(success_page.thank_you.find_visible_element(),
                       "'Thank you' appeared as a sign of successful transaction",
                       continue_on_error=False)
        validate(success_page.basic_validation_list)

    def tearDown(self):
        """
        in addition to default tearDown delete new product that was created in setUp
        :return:
        """
        ProcessRequest(f"products/{self.product_id}.json").send_request(
            'DELETE', continue_on_error=True)
        super().tearDown()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
