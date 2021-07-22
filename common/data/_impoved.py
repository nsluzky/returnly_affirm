""" provides sample data to create products """
from random import randint

from tools.random_strings import random_name

PRODUCT = lambda prefix: {
    "product": {
        "title": f"TEST {prefix} {random_name(5, 10)} {random_name(5, 8)}",
        "body_html": f"<strong>Good {random_name(10)}!</strong>",
        "vendor": "Burton",
        "product_type": "Snowboard",
    }
}


def get_new_product_with_default_product_variant():
    result = PRODUCT('default_product_variant').copy()
    result['product']['tags'] = [
        "Barnes & Noble",
        "Big Air",
        "John's Fav"
    ]
    return result


def get_new_unpublished_product():
    result = PRODUCT('unpublished').copy()
    result['product']["published"] = False
    return result


def get_new_draft_product():
    result = PRODUCT('draft').copy()
    result['product']["status"] = "draft"
    return result


def get_new_product_with_multiple_product_variants():
    result = PRODUCT('multiple_product_variants').copy()
    result['product']["variants"] = [
        {
            "option1": f"{random_name(5)}",
            "price": f'"{randint(1, 9999)}.{randint(11, 99)}"',
            "sku": f'"{randint(1000, 9999)}"'
        },
        {
            "option1": f"{random_name(5)}",
            "price": f'"{randint(1, 9999)}.{randint(11, 99)}"',
            "sku": f'"{randint(1000, 9999)}"'
        }
    ]
    return result


def get_new_product_without_title_will_return_error422():
    result = PRODUCT('').copy()
    del result['product']["title"]
    return result


def get_new_product_with_ceo_title():
    result = PRODUCT('ceo_title').copy()
    result['product']["metafields_global_title_tag"] = "Product SEO Title"
    result['product']["metafields_global_description_tag"] = "Product SEO Description"
    return result
