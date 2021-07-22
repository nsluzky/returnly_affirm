"""classes to start Selenium session."""
import os
from selenium import webdriver

from common.common_actions import get_test_property


class LocalBrowserInit:
    """Initiate a browser locally."""

    def __init__(self):
        """Create a local Selenium session and open a browser."""
        browser_types = {
            'firefox': 'webdriver.Firefox()',
            'chrome': 'webdriver.Chrome()'
        }
        browser_type = get_test_property('browser').lower()
        assert browser_type in browser_types.keys() ,\
            f"browser type {browser_type} should be one of {browser_types.keys()}"
        if get_test_property('headless'):
            if browser_type == 'chrome':
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.options import Options
                opt = Options()
                opt.add_argument('--headless')
                self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)
            elif browser_type == 'firefox':
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.headless = True
                self.driver = webdriver.Firefox(options=options)
        else:
            self.driver = eval(browser_types[browser_type])
        self.driver.delete_all_cookies()

    def get_driver(self):
        """ Get driver """
        return self.driver
