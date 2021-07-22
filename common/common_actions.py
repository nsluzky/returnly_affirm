""" The module implements common options  like wait until page is loaded """
import os
from time import time, sleep
from datetime import datetime

from common.constants import log_message

MAX_WAIT_TIME = 180
FAILED_ASSERTIONS = 0
TOTAL_ASSERTIONS = 0

def add_cookie(driver, cookie_name, cookie_value, log_level='WARN'):
    """
    Add Cookie
    :param driver:
    :param cookie_name:
    :param cookie_value:
    :param log_level:
    :return:
    """
    log_message("Adding cookie '{}' with value '{}'".format(cookie_name, cookie_value), log_level)
    driver.add_cookie({'name': cookie_name, 'value': cookie_value})

def delete_cookie(driver, cookie_name, log_level='WARN'):
    """
    Add Cookie
    :param driver:
    :param cookie_name:
    :param log_level:
    :return:
    """
    log_message("Deleting cookie '{}'".format(cookie_name), log_level)
    driver.delete_cookie(cookie_name)

def set_attribute(driver, element, attribute_name, attribute_value):
    """
    set attribute of an element
    :param driver:
    :param element:
    :param attribute_name:
    :param attribute_value:
    :return:
    """
    if is_visible(element):
        scroll_to(driver, element)
    driver.execute_script(
        "arguments[0].setAttribute('{}', '{}');".format(
            attribute_name, attribute_value), element)

def highlight(driver, element, width=3, color='red'):
    """
    Highlight an element
    :param driver:
    :param element:
    :param width: width of border
    :param color: color of border
    :return:
    """
    set_attribute(driver, element, 'style', 'border: {}px solid {};'.format(
        width, color))

def unhighlight(driver, element):
    """
    Unhighlight an element
    :param driver:
    :param element:
    :return:
    """
    set_attribute(driver, element, 'style', 'border: 0px solid green;')

def animate(driver, element=None, name='highlight'):
    """
    Red-border the element for a moment
    :param driver:
    :param element:
    :param log_level:
    :return: None
    """
    if not get_test_property("animate"):
        return
    try:
        if is_visible(element):
            animation_time = get_test_property("animation_time")
            highlight(driver, element=element)
            save_screenshot(driver, name='{}'.format(name))
            sleep(animation_time)
            unhighlight(driver, element=element)
    except Exception as exception:
        log_message("Error in animate {}".format(exception), 'WARN')


def check_failed_assertions(log_level="WARN"):
    """
    :param log_level:
    :return:
    This function should be called at the end of a test to check whether there were failures
    """
    if FAILED_ASSERTIONS:
        message = "{} assertion(s) failed during the run".format(FAILED_ASSERTIONS)
        log_message(message, "ERROR")
        raise Exception(message)
    if TOTAL_ASSERTIONS:
        log_message("All {} assertions passed".format(TOTAL_ASSERTIONS), log_level)
    else:
        log_message("None assertions were verified")


def assert_and_log(assertion, message="", continue_on_error=True):
    """
    validate assertion and log the result
    if it failed either increase number of failed assertions or raise exception

    :param assertion:
    :param message:
    :param continue_on_error:
    :return:
    """
    global FAILED_ASSERTIONS, \
        TOTAL_ASSERTIONS
    TOTAL_ASSERTIONS += 1
    message = "{}. asserting:{}".format(TOTAL_ASSERTIONS, message)
    try:
        if assertion:
            log_message(message)
        else:
            FAILED_ASSERTIONS += 1
            message += " NOT TRUE"
            log_message(message, "ERROR")
            if not continue_on_error:
                raise Exception(message)
    except Exception as exception:
        return handle_error(exception, continue_on_error=continue_on_error)

def save_screenshot(driver, name='', log_level='INFO'):
    """
    Save screenshot in a file
    If file name is not set, use timestamp with extension png
    :param driver:
    :param name:
    :return:
    """
    try:
        if not driver:
            return
    except:
        return
    folder = get_test_property('screenshots_folder')
    if not folder:
        folder = 'screenshots'
    extension = '.png'
    full_name = os.path.join(folder, "{}_{}{}".format(
        datetime.now().strftime("%Y-%M-%d_%H-%M-%S.%f")[:-3], name, extension))
    driver.get_screenshot_as_file(full_name)
    log_message('saved screenshot {}'.format(full_name), log_level)

def handle_error(exception=None, message="", continue_on_error=True):
    """
    If continue_on_error:
    - None: return None
    - True: construe as a failed soft assertion and continue execution
    - False: re-raise exception

    :param exception:
    :param message:
    :param continue_on_error:
    :return:
    """
    if continue_on_error is None:
        return None
    global FAILED_ASSERTIONS
    log_message("{} execution continues\n{}".format(message, str(exception)), "ERROR")
    FAILED_ASSERTIONS += 1
    if continue_on_error:
        return None
    if exception:
        raise exception
    raise exception(message)

def is_visible(element, log_level="DEBUG"):
    """
     returns whether the element is visible
    it checks that:
        element is not Null
        if is_displayed method is available, it's value is True
        if size is available, and only one of (width, length) is 0
    """
    if not element:
        log_message("element is None -> not visible", log_level)
        return False
    if hasattr(element, 'is_displayed') and not element.is_displayed():
        log_message("element.is_displayed() = False -> not visible", log_level)
        return False
    _class = element.get_attribute('class')
    if _class and _class.find('_hide') > -1:
        log_message("element's class {} contains _hide -> not visible".format(_class))
    try:
        if element.size['height'] + element.size['width'] and \
                not element.size['height'] * element.size['width']:
            log_message("elements height or width is 0 -> not visible", log_level)
            return False
    except:
        log_message("element does not have width or height")
    log_message("element is visible", log_level)
    return True

def is_visible_and_enabled(element, log_level="DEBUG"):
    """
     returns whether the element is visible and enabled
    """
    if not is_visible(element, log_level):
        log_message("element is not visible", log_level)
        return False
    if hasattr(element, 'is_enabled') and not element.is_enabled():
        log_message("element.is_displayed() = False -> not visible and enabled", log_level)
        return False
    log_message("element is visible and enabled", log_level)
    return True

def back(driver, log_level="INFO"):
    """
    go back and wait until page is loaded
    :param driver:
    :param log_level:
    :return:
    """
    log_message("Go back", log_level)
    driver.back()
    wait_until_page_is_loaded(driver, wait_time=MAX_WAIT_TIME)

def navigate_to(driver, url, log_level="INFO"):
    """
    navigate to url and wait until it's loaded

    :param driver:
    :param url:
    :param wait_time:
    :return:
    """
    log_message("Navigate to " + url, log_level)
    driver.get(url)
    wait_until_page_is_loaded(driver, wait_time=MAX_WAIT_TIME)

def refresh(driver, wait_time=MAX_WAIT_TIME):
    """
    refresh and wait until pageis reloaded
    :param driver:
    :param wait_time:
    :return:
    """
    log_message("Refreshing page ...")
    driver.refresh()
    wait_until_page_is_loaded(driver, wait_time)

def refresh_if_asked(driver, wait_time=MAX_WAIT_TIME):
    """
    If message asking to refresh appears, refresh until message disappears or wait_time expires
    :param driver:
    :param wait_time:
    :return:
    """
    to_refresh_xpath = "//button[@class='link' and @onclick='location.reload()']"
    to_refresh = driver.find_elements('xpath', to_refresh_xpath)
    start_time = time()
    while to_refresh and (time() < start_time + wait_time):
        if to_refresh:
            log_message("Refreshing page requested", "WARN")
            refresh(driver, wait_time)
        to_refresh = driver.find_elements('xpath', to_refresh_xpath)
    if to_refresh:
        log_message("Request to refresh the page didn't dissapear", "WARN")

def wait_until_page_is_loaded(driver, wait_time=MAX_WAIT_TIME):
    """
    wait until page is loaded
    :param driver:
    :param wait_time:
    :return:
    """
    start_time = time()
    source = driver.page_source
    first = True
    loaded = False
    while first or (
            source != driver.page_source and not loaded and time() < start_time + wait_time):
        sleep(.2)
        first = False
        loaded = (driver.execute_script("return document.readyState") == "complete")
        source = driver.page_source
    refresh_if_asked(driver, wait_time=wait_time)
    if get_test_property('save_screenshots'):
        save_screenshot(driver, name="page_loaded")
    if source != driver.page_source:
        log_message("Page is still updating ...", "WARN")

def scroll_to(driver, element=None, log_level="DEBUG", continue_on_error=True):
    """
    Scroll to the element
    :param driver:
    :param element:
    :param log_level:
    :return:
    """
    try:
        log_message("scroll_to {}".format(str(element)), log_level)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    except:
        handle_error(message="error while scrolling to the item",
                     continue_on_error=continue_on_error)

def get_test_property(property_name, log_level="DEBUG"):
    """
    return test property from environment variable PARAMS
    if such property is not set, return None
    :param property_name:
    :return:
    """
    content = os.environ.get("PARAMS", "{}")
    try:
        result = eval(content).get(property_name, None)
        log_message("Value of property {} is {}".format(property_name, result), log_level)
        return result
    except:
        log_message("Can't process environment variable PARAMS '{}'".format(content), "WARN")
        return None

def set_test_property(property_name, property_value, log_level="DEBUG"):
    """
    set test property to environment variable PARAMS
    if such property is not set, return None
    :param property_name:
    :return:
    """
    try:
        content = eval(os.environ.get("PARAMS", "{}"))
        log_message("variable PARAMS '{}'".format(content), log_level)
    except:
        log_message("wrong value of environment variable PARAMS '{}'".format(content), "WARN")
        content = {}
    content[property_name] = property_value
    os.environ['PARAMS'] = str(content)

def validate(basic_list, to_add=list(), to_exclude=list(), log_level="INFO", wait_time=1):
    """
    validate that items in the list are visible.
    Basic list is optionally adjusted with to_add and to_exclude list
        to comply with requirements with different pages and tests
    :param to_add: items to be added to basic validation list
    :param to_exclude: items to be excluded from basic validation list
    :param log_level:
    :param wait_time:
    :return:
    """
    for item in basic_list:
        if item not in to_exclude:
            assert_and_log(
                item.find_visible_element(log_level="DEBUG", wait_time=wait_time),
                "{} is visible".format(str(item)), True)
    first = True
    for item in to_add:
        if first:
            first = False
            log_message("{stars} validating additional fields {stars}".format(
                stars=20 * '*'), log_level)
        if item in to_add and item not in to_exclude:
            assert_and_log(
                item.find_visible_element(log_level="DEBUG", wait_time=wait_time),
                "{} is visible".format(str(item)), True)

def validate_negative(item):
    """
    validate that item is not visible.
    :param item
    :return:
    """
    assert_and_log(
        not item.find_visible_elements(0, log_level="DEBUG", wait_time=0),
        "{} is not visible".format(str(item)), True)