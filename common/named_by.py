"""
Description of an element of a web page
 This class is designed to:
   specify objects on Web pages
   finding corresponding WebElements
   perform actions on WebElements
   log these actions
   create and save screenshots in case of a failure
"""
from time import time, sleep
import inspect
import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from common.common_actions import \
    wait_until_page_is_loaded, \
    log_message, \
    animate, \
    handle_error, \
    scroll_to, \
    is_visible, is_visible_and_enabled, \
    get_test_property

class NamedBy:
    ''' Class that describes objects on web pages and provides methods to handle them '''
    MAX_TIMEOUT = 30

    def __init__(self, description, by_type, by_definition, parent):
        """ class is instantiated using element properties and webdriver """
        # validate parameters
        self.driver = parent.driver
        try:
            self.driver.find_elements(by_type, by_definition)
        except:
            print("invalid descriptor ('{}', '{}') in {}".format(
                by_type, by_definition, description))
            by_definition = "ERRONEUS " + str(by_definition)
        if not isinstance(by_definition, str):
            raise Exception("by definition '{}' is not a string")
        self.description = description
        self.by_type = by_type
        self.by_definition = by_definition
        self.parent = parent
        self.action = ActionChains(self.driver)

    def __str__(self, instance=1):
        """ printable representation of the class """
        if instance < 2:
            return "{}.<{}>:{}".format(type(self.parent).__name__, self.description, self.locator())
        return "{} instance of {}.<{}>:{}".format(
            instance, type(self.parent).__name__, self.description, self.locator())

    def locator(self):
        """ Returns locator of element like '("id", "username")' """
        return '("%s", "%s")' % (self.by_type, self.by_definition)

    def find_element(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                     continue_on_error=True):
        """ wait until element is present and return it"""
        try:
            log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
            element = self.find_elements(instance, wait_time, "DEBUG")[instance - 1]
            if not element:
                raise Exception("element {} not found".format(str(self)))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)
        return element

    def is_not_present(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                       continue_on_error=True):
        """ check that the specified element is not present
        and does not appear during the specified time """
        try:
            log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
            start_time = time()
            first = True
            while first or time() - start_time < wait_time:
                first = False
                sleep(1)
                result = len(
                    self.driver.find_elements(self.by_type, self.by_definition)) < instance
                if result:
                    break
            if not result:
                raise Exception("element is present")
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def is_not_visible(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                       continue_on_error=True):
        """ check that the specified element is not visible
        and does not become visible during the specified time """
        try:
            log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
            elements = self.driver.find_elements(self.by_type, self.by_definition)
            start_time = time()
            first = True
            while first or time() - start_time < wait_time:
                first = False
                sleep(1)
                elements = self.driver.find_elements(self.by_type, self.by_definition)
                result = len(elements) < instance or \
                         (hasattr(elements[instance + 1], 'is_displayed')
                          and elements[instance + 1].is_displayed())
                if result:
                    break
            if not result:
                raise Exception("element is visible")
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def is_not_enabled(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                       continue_on_error=True):
        """ check that the specified element is not enabled
        and does not become enabled during the specified time """
        try:
            log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
            elements = self.driver.find_elements(self.by_type, self.by_definition)
            result = len(elements) < instance or \
                     (hasattr(elements[instance + 1], 'is_enabled')
                      and elements[instance + 1].is_enabled())
            start_time = time()
            while result and time() - start_time < wait_time:
                sleep(1)
                elements = self.driver.find_elements(self.by_type, self.by_definition)
                result = len(elements) < instance or not elements[instance + 1].is_enabled()
            if not result:
                raise Exception("element is enabled")
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def get_visible_elements(self, elems, log_level="DEBUG", up_to=None):
        """ returns elements from the list that are visible """
        if up_to:
            try:
                up_to = int(up_to)
            except:
                log_message(
                    inspect.stack()[0][3] + ':' +
                    "parameter up_to '{}' should be None or an integer".format(up_to))
                up_to = None
        size = 0
        result = []
        for item in elems:
            if is_visible(item):
                result.append(item)
                if up_to:
                    size += 1
                    if len(result) >= up_to:
                        break
        log_message(inspect.stack()[0][3] + ':' + "from {} element(s) got {} visible".
                    format(len(elems), len(result)),
                    log_level)
        return result

    def get_visible_and_enabled_elements(self, elems, log_level="DEBUG", up_to=None):
        """ returns elements from the list that are visible and enabled """
        if up_to:
            try:
                up_to = int(up_to)
            except:
                log_message(
                    inspect.stack()[0][3] + ':' +
                    "parameter up_to '{}' should be None or an integer".format(up_to))
                up_to = None
        size = 0
        result = []
        for item in elems:
            if is_visible_and_enabled(item):
                result.append(item)
                if up_to:
                    size += 1
                    if len(result) >= up_to:
                        break
        log_message(
            inspect.stack()[0][3] + ':' + "from {} element(s) got {} visible and enabled".
            format(len(elems), len(result)), log_level)
        return result

    def find_visible_element(
            self, instance=1, wait_time=MAX_TIMEOUT, log_level="DEBUG", continue_on_error=True):
        """ Wait until the element becomes visible """
        try:
            log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
            elements = self.find_visible_elements(
                instance, wait_time, "DEBUG", continue_on_error=None, up_to=instance)
            if not elements:
                raise Exception("Failed to find visible element")
            result = elements[instance - 1]
            if result.text:
                log_message(""'{}'"".format(result.text.split('\n')))
            if get_test_property('animation_time'):
                scroll_to(self.driver, result)
                animate(self.driver, result, name=self.description)
            return result
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def find_visible_and_enabled_element(
            self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO", continue_on_error=True):
        """ Wait until the element becomes visible and enabled and return it"""
        result = None
        try:
            log_message(inspect.stack()[0][3] + ':' + self.__str__(instance),
                        log_level)
            elements = self.find_visible_and_enabled_elements(
                instance, wait_time, "DEBUG", continue_on_error=None, up_to=instance)
            if not elements:
                raise Exception("Failed to find visible and enabled element")
            result = elements[instance - 1]
            if result.text:
                log_message(""'{}'"".format(result.text.split('\n')))
            if get_test_property('animation_time'):
                scroll_to(self.driver, result)
                animate(self.driver, result, name="find_visible_and_enabled_{}".format(
                    self.description))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)
        finally:
            return result

    def switch_to_frame(self, log_level="INFO", continue_on_error=False):
        """ wait until frame is available and switch to it """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(), log_level)
        try:
            sleep(.1)
            self.driver.switch_to.frame(self.find_element(log_level="DEBUG"))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def find_visible_elements(
            self, instances=1, wait_time=MAX_TIMEOUT, log_level="INFO",
            up_to=None, continue_on_error=False):
        ''' Wait until at least <instances> number of visible elements
         match description and return all of them '''
        result = []
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instances), log_level)
        try:
            start_time = time()
            first = True
            found = False
            while time() - start_time < wait_time or first:
                first = False
                result = self.get_visible_elements(
                    self.driver.find_elements(self.by_type, self.by_definition), up_to=up_to)
                if len(result) >= instances:
                    found = True
                    break
                sleep(wait_time / 10)
            if not found:
                raise Exception("{} found only {} elements while expecting {}".format(
                    self.__str__(), len(result), instances))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)
        finally:
            return result

    def find_visible_and_enabled_elements(
            self, instances=1, wait_time=MAX_TIMEOUT, log_level="INFO",
            up_to=None, continue_on_error=False):
        ''' Wait until at least <instances> number of find_visible_and_enabled_element elements
         match description and return all of them '''
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instances), log_level)
        result = []
        try:
            start_time = time()
            not_found = True
            first = True
            while time() - start_time < wait_time or first:
                first = False
                result = self.get_visible_and_enabled_elements(
                    self.driver.find_elements(self.by_type, self.by_definition), up_to=up_to)
                if len(result) >= instances:
                    not_found = False
                    break
                sleep(wait_time / 10)
            if not_found:
                raise Exception("{} found only {} elements while expecting {}".format(
                    self.__str__(), len(result), instances))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)
        finally:
            return result

    def find_elements(self, instances=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                      continue_on_error=False):
        ''' Wait until at least <instances> number of elements
         match description and return all of them '''
        result = None
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instances), log_level)
        try:
            start_time = time()
            first = True
            found = False
            result = self.driver.find_elements(self.by_type, self.by_definition)
            while time() - start_time < wait_time or first:
                first = False
                result = self.driver.find_elements(self.by_type, self.by_definition)
                if len(result) >= instances:
                    found = True
                    break
            if not found:
                raise Exception("{} found only {} elements while expecting {}".format(
                    self.__str__(), len(result), instances))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)
        finally:
            return result

    def clear(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO", continue_on_error=False):
        """ Wait until element is clickable and clear it"""
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error) \
                .clear()
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def send_keys(self, text, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                  continue_on_error=False):
        """ Wait until element is clickable and append text """
        log_message(
            inspect.stack()[0][3] + ':' + text + "' in " + self.__str__(instance), log_level)
        try:
            self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG",
                continue_on_error=continue_on_error).send_keys(text)
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def enter(self, text, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
              continue_on_error=False):
        """ Wait until element is clickable, clear it, and enter text """
        log_message("{}:'{}' in {}".format(
            inspect.stack()[0][3], text, self.__str__(instance)), log_level)
        try:
            elem = self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error)
            elem.clear()
            elem.send_keys(text)
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def is_not_clickable(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                         continue_on_error=True):
        """
        tries to click an element and expects an exception
        Returns True if exception is raised or False otherwise
        :param instance:
        :param wait_time:
        :param log_level:
        :param continue_on_error:
        :return:
        """
        log_message(inspect.stack()[0][3] + ':', log_level='DEBUG')
        try:
            self.click(instance=instance, wait_time=wait_time, log_level=log_level,
                       continue_on_error=False, failover_to_js_click=False)
            handle_error(
                message="click was successful while it's expected to fail",
                continue_on_error=continue_on_error)
            return False
        except:
            return True

    def click(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
              continue_on_error=False, failover_to_js_click=True):
        """
        Find and click the element.
        In case of failure use js_click if failover_to_js_click is True
        :param instance:
        :param wait_time:
        :param log_level:
        :param continue_on_error:
        :param failover_to_js_click:
        :return:
        """
        """ Wait until element is clickable and click it"""
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG",
                continue_on_error=continue_on_error).click()
            sleep(2)
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            log_message(inspect.stack()[0][3] + ':' + "click on {} failed {}".
                        format(self.__str__(instance), str(exception)), "WARN")
            if failover_to_js_click:
                log_message(inspect.stack()[0][3] + ':' + "will try to js_click", "WARN")
                self.js_click(instance, wait_time=wait_time, continue_on_error=continue_on_error)

    def random_click(self, wait_time=MAX_TIMEOUT, log_level="INFO", max_pages=1):
        """
        click a random instance of corresponding webelememts.
        :param wait_time:
        :param log_level:
        :param max_pages: if the element can't be found on current page, try up to <max_pages> more
        :return:
        """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(), log_level)
        try:
            all_webelements = self.find_visible_and_enabled_elements(
                0, wait_time, log_level="DEBUG")
            additional_page = 0
            while not all_webelements:
                log_message("could not find {}. will try on the next page".format(str(self)))
                self.driver.find_element('xpath', "//a[contains(@class,'iconArrowRight')]").click()
                wait_until_page_is_loaded(self.driver)
                all_webelements = self.find_visible_and_enabled_elements(
                    0, wait_time, log_level="DEBUG")
                additional_page += 1
                if additional_page > max_pages:
                    raise Exception("Could not find {}".format(str(self)))
            total = len(all_webelements)
            index = random.randint(0, total - 1)
            all_webelements[index].click()
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            log_message(inspect.stack()[0][3] + ':' + "click on {} failed {}".
                        format(self.__str__(index + 1), str(exception)), "WARN")

    def perform_chain_action(self, action, action_alias=None, instance=1, wait_time=MAX_TIMEOUT,
                             log_level="INFO", continue_on_error=False):
        """
         Wait until element is clickable and perform one of chain actions
        """
        if not action_alias:
            action_alias = action
        log_message(
            inspect.stack()[0][3] + ':' + "{} {}".
            format(action_alias, self.__str__(instance)), log_level)
        try:
            element = self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error)
            exec("self.action.{}(element).perform()".format(action))
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def double_click(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                     continue_on_error=False):
        """ Wait until element is clickable and double_click it"""
        self.perform_chain_action("double_click", action_alias=None, instance=instance,
                                  wait_time=wait_time, log_level=log_level,
                                  continue_on_error=continue_on_error)

    def right_click(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                    continue_on_error=False):
        """ Wait until element is clickable and right_click it"""
        self.perform_chain_action("context_click", action_alias="right_click", instance=instance,
                                  wait_time=wait_time, log_level=log_level,
                                  continue_on_error=continue_on_error)

    def mouse_over(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                   continue_on_error=False):
        """ Wait until element is present ant hover it with mouse """
        self.perform_chain_action("move_to_element", action_alias="mouse_over", instance=instance,
                                  wait_time=wait_time, log_level=log_level,
                                  continue_on_error=continue_on_error)

    def get_text(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                 continue_on_error=False):
        """ Wait until element is visible and return its text """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            return self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG",
                continue_on_error=continue_on_error).text
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def get_attribute(self, attribute, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                      continue_on_error=False):
        """ Wait until element is present and return its attribute value """
        log_message(
            inspect.stack()[0][3] + ':' + attribute + " " + self.__str__(instance), log_level)
        try:
            self.find_element(instance, wait_time, log_level="DEBUG",
                              continue_on_error=True)
            return self.find_element(
                instance, wait_time, log_level="DEBUG",
                continue_on_error=continue_on_error).get_attribute(attribute)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def check(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
              continue_on_error=False):
        """
         Wait until element is clickable.
         If it's not selected, click it
         """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            element = self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error)
            if not element.is_selected():
                element.click()
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def uncheck(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                continue_on_error=False):
        """
         Wait until element is clickable.
         If it's selected, click it
         """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            element = self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error)
            if element.is_selected():
                element.click()
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def is_selected(self, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                    continue_on_error=None):
        """
         Wait until element is visible.
         Return whether it's selected
         """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            element = self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=None)
            return element.is_selected()
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def get_all_options(
            self, wait_time=MAX_TIMEOUT, log_level="INFO", continue_on_error=False):
        """
        Get all options of a list
        :param wait_time:
        :param log_level:
        :param continue_on_error:
        :return:
        """
        if self.by_type == By.XPATH:
            xpath = self.by_definition
        else:
            raise Exception("selector should be specified by xpath")
        xpath += '/option'
        options = NamedBy(
            "Options of {}".format(self.description), By.XPATH,
            xpath,
            self)
        return options.find_elements(
            0, wait_time=wait_time, continue_on_error=continue_on_error, log_level=log_level)

    def get_selected_options(
            self, wait_time=MAX_TIMEOUT, log_level="INFO", continue_on_error=False):
        """
        Get selected options of a list
        :param wait_time:
        :param log_level:
        :param continue_on_error:
        :return:
        """
        if self.by_type == By.XPATH:
            xpath = self.by_definition
        else:
            raise Exception("{} selector should be specified by xpath".format(str(self)))
        xpath += "/option[@selected]"
        options = NamedBy(
            "Selected Options of {}".format(self.description), By.XPATH,
            xpath,
            self)
        return options.find_elements(
            0, wait_time=wait_time, continue_on_error=continue_on_error, log_level=log_level)

    def select(self, selection_type, selection_value, instance=1, wait_time=MAX_TIMEOUT,
               log_level="INFO", continue_on_error=False):
        """
         Wait until select element is clickable and make selection by type and value
        """
        log_message("{} select_by_{}('{}')".format(
            self.__str__(instance), selection_type, selection_value), log_level)
        try:
            element = self.find_visible_and_enabled_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error)
            element.click()
            animate(self.driver, element, name="select_{}".format(self.description))
            element.click()
            exec('Select(element).select_by_{}({})'.format(selection_type, selection_value))
            wait_until_page_is_loaded(self.driver)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def select_by_value(self, value, instance=1, wait_time=MAX_TIMEOUT,
                        log_level="INFO", continue_on_error=False):
        """
         Wait until select element is clickable and make selection by value
        """
        self.select("value", '"{}"'.format(value), instance=instance, wait_time=wait_time,
                    log_level=log_level, continue_on_error=continue_on_error)

    def select_by_index(self, index, instance=1, wait_time=MAX_TIMEOUT,
                        log_level="INFO", continue_on_error=False):
        """
         Wait until select element is clickable and make selection by index
        """
        self.select("index", index, instance=instance, wait_time=wait_time,
                    log_level=log_level, continue_on_error=continue_on_error)

    def select_by_visible_text(self, text, instance=1, wait_time=MAX_TIMEOUT,
                               log_level="INFO", continue_on_error=False):
        """
         Wait until select element is clickable and make selection by visible text
        """
        self.select("visible_text", '"{}"'.format(text), instance=instance,
                    wait_time=wait_time, log_level=log_level, continue_on_error=continue_on_error)

    def js_click(self, instance=1, wait_time=MAX_TIMEOUT,
                 log_level="INFO", continue_on_error=False):
        """
         Wait until select element is clickable and click it using javascript
        """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        element = self.find_visible_and_enabled_element(
            instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error)
        self.driver.execute_script("arguments[0].click();", element)

    def get_css_value(self, property_name, instance=1, wait_time=MAX_TIMEOUT, log_level="INFO",
                      continue_on_error=None):
        """ Wait until element is visible and return its css_value """
        log_message(inspect.stack()[0][3] + ':' + property_name + " of {}".format(
            self.__str__(instance)), log_level)
        try:
            self.find_visible_and_enabled_element(instance, wait_time, log_level="DEBUG",
                                                  continue_on_error=continue_on_error)
            return self.find_element(
                instance, wait_time, log_level="DEBUG", continue_on_error=continue_on_error) \
                .value_of_css_property(property_name)
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def wait_until_not_present(self, instance=1, wait_time=MAX_TIMEOUT, log_level="DEBUG",
                               continue_on_error=True):
        """ Wait until element is not present """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            not_found = True
            start_time = time()
            while not_found:
                not_found = (len(self.driver.find_elements(
                    self.by_type, self.by_definition)) >= instance)
                if time() - start_time > wait_time:
                    break
            if not_found:
                raise Exception("{} is still present".format(str(self)))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)

    def wait_until_not_visible(self, instance=1, wait_time=MAX_TIMEOUT, log_level="DEBUG",
                               continue_on_error=True):
        """ Wait until element is not visible """
        log_message(inspect.stack()[0][3] + ':' + self.__str__(instance), log_level)
        try:
            not_found = True
            start_time = time()
            while not_found:
                elements = self.driver.find_elements(self.by_type, self.by_definition)
                not_found = (len(elements) >= instance) or elements[instance - 1].is_displayed()
                if time() - start_time > wait_time:
                    break
            if not_found:
                raise Exception("{} is still visinle".format(str(self)))
        except Exception as exception:
            return handle_error(exception, continue_on_error=continue_on_error)
