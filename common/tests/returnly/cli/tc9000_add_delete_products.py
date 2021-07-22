""" Verify that different sets o """
import unittest
from common.base_tests.cli_basetest import BaseTest
from common.process_request import ProcessRequest
from common.data.product import\
    get_new_product_with_multiple_product_variants,\
    get_new_product_with_the_default_product_variant,\
    get_new_draft_product, get_new_unpublished_product,\
    get_product_with_an_ceo_title_and_description,\
    get_new_product_without_title_will_return_error422


class TC9000(BaseTest):
    """
    Verify product menu
    """
    def multiple_product_variants(self):
        """
        test adding product with multiple_product_variants
        :return:
        """
        add_product_expect_success('multiple_product_variants')

def add_product_expect_success(data_type):
    """
    Add a product of the expected type
    Validate that it was added to backend
    At the end remove the product
    Validate that it's removed from the backend
    :return:
    """
    data = eval(f"get_new_product_with_{data_type}")
    try:
        r=ProcessRequest('products.json').send_request("POST", data=data)
    finally:
        pass

if __name__ == '__main__':
    unittest.main(warnings='ignore')
