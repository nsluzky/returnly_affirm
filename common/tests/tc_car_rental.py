import os
from pprint import pprint

from common.browser_init import LocalBrowserInit
from common.common_actions import *
from common.constants import get_all_properties
from common.constants import log_message
from common.constants import DEFAULT_PROPERTIES
from common.investigator import *
from common.browser_init import LocalBrowserInit
from common.pages.car_rental import Cars
set_test_property('browser', 'chrome')
set_test_property('headless', False)
props = get_all_properties(
            eval(os.environ.get("PARAMS", "{}")), "INFO", default=DEFAULT_PROPERTIES)
try:
        driver = LocalBrowserInit().get_driver()
        driver.delete_all_cookies()
        url = "https://www.expedia.com/carsearch?aarpcr=off&acop=2&d1=2021-09-13&d2=2021-09-26&dagv=1&date1=9%2F13%2F2021&date2=9%2F26%2F2021&dpln=5265485&drid1=&fdrp=0&loc2=&locn=Milan%20%28MXP%20-%20Malpensa%20Intl.%29&pickupIATACode=MXP&rdct=1&rdus=10&returnIATACode=&selPageIndex=0&selSort=TOTAL_PRICE_LOW_TO_HIGH&styp=4&subm=1&time1=0500PM&time2=0430AM&ttyp=2&vend="
        driver.get(url)
        Cars(driver).total_price.get_text()
finally:
        driver.quit()