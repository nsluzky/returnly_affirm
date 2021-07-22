""" end-to-end test Buy It Now newly created product """
import unittest
from random import randint

from tools.random_strings import random_name
from common.base_tests.gui_basetest import BaseTest
from common.pages.product import ProductPage
from common.pages.payment import PaymentPage
from common.pages.payment_review import PaymentReviewPage
from common.pages.payment_info import PaymentInfoPage
from common.pages.success import SuccessPage

from common.data.product import get_new_product_with_multiple_product_variants
from common.common_actions import assert_and_log
from common.common_actions import navigate_to
from common.common_actions import validate

from common.process_request import ProcessRequest

class TC302(BaseTest):
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
        self.new_product = get_new_product_with_multiple_product_variants()
        response = ProcessRequest('products.json').send_request(
            'POST',
            data=self.new_product,
            expected_return_codes=[201],
        )
        self.product_id = response.response['product']['id']
    def test_validate_catalog_page(self):
        """
        test methods names should start with "test_"
        :return:
        """
        product_page = ProductPage(self.driver)
        payment_page = PaymentPage(self.driver)
        payment_review_page = PaymentReviewPage(self.driver)
        payment_info_page = PaymentInfoPage(self.driver)
        success_page = SuccessPage(self.driver)
        navigate_to(self.driver, ProductPage.URL(self.new_product['product']['title']))
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
        ### Next 3 lines are commented out; product object can't be found with headless mode
        #payment_review_page.product.get_text()
        #assert_and_log(payment_review_page.product.get_text() == product,
        #               "Selected product is displayed")
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
