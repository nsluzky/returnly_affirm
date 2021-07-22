""" provides sample data to create products """
from random import randint

from tools.random_strings import random_name


def get_new_product_with_the_default_product_variant():
    """
    return data to post new product
    :return:
    """
    return {
        "product": {
            "title": f"TEST default_product_variant {random_name(5, 10)} {random_name(5, 8)}",
            "body_html": f"<strong>Good {random_name(10)}!</strong>",
            "vendor": "Burton",
            "product_type": "Snowboard",
            "tags": [
                "Barnes & Noble",
                "Big Air",
                "John's Fav"
            ]
        }
    }


def get_new_unpublished_product():
    """
    return data to post new product
    :return:
    """
    return {
        "product": {
            "title": f"TEST unpublished {random_name(5, 10)} {random_name(5, 8)}",
            "body_html": f"<strong>Good {random_name(10)}!</strong>",
            "vendor": "Burton",
            "product_type": "Snowboard",
            "published": False
        }
    }


def get_new_draft_product():
    """
    return data to post new product
    :return:
    """
    return {
        "product": {
            "title": f"TEST draft {random_name(5, 10)} {random_name(5, 8)}",
            "body_html": f"<strong>Good {random_name(10)}!</strong>",
            "vendor": "Burton",
            "product_type": "Snowboard",
            "status": "draft"
        }
    }


def get_new_product_with_multiple_product_variants():
    """
    return data to post new product
    :return:
    """
    return {
        "product": {
            "title": f"TEST multiple_product_variants {random_name(5, 10)} {random_name(5, 8)}",
            "body_html": f"<strong>Good {random_name(10)}!</strong>",
            "vendor": "Burton",
            "product_type": "Snowboard",
            "variants": [
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
        }
    }


def get_new_product_without_title_will_return_error422():
    """
    return data to post new product
    :return:
    """
    return {
        "product": {
            #"title": f"TEST without_title {random_name(5, 10)} {random_name(5, 8)}",
            "body_html": f"<strong>Good {random_name(10)}!</strong>",
            "vendor": "Burton",
            "product_type": "Snowboard",
        }
    }


def get_new_product_with_an_ceo_title():
    """
    return data to post new product
    :return:
    """
    return {
        "product": {
            "title": f"TEST with_an_ceo_title {random_name(5, 10)} {random_name(5, 8)}",
            "body_html": f"<strong>Good {random_name(10)}!</strong>",
            "vendor": "Burton",
            "product_type": "Snowboard",
            "metafields_global_title_tag": "Product SEO Title",
            "metafields_global_description_tag": "Product SEO Description"
        }
    }
