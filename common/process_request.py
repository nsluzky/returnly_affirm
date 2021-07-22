""" Send and process HTTP request """
import time
import json
import os
from requests import request

from common.constants import log_message
from common.common_actions import get_test_property
from common.common_actions import assert_and_log

METHODS = ['GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE']

class ProcessRequest:
    """
    Base test for http-get-related tests
    """
    def __init__(self,
                 url_suffix="",
                 full_url=None,
                 ):
        """
        If full_url is not specified, concatenate base_url and url_suffix
        :param url_suffix:
        :param full_url:
        """
        self.url = full_url if full_url \
            else os.path.join(get_test_property('baseurl_api'), url_suffix)
    def send_request(self,
                     method,
                     log_level='INFO',
                     timeout=get_test_property('max_timeout'),
                     data=None,
                     expected_return_codes=None,
                     expected_exception=None,
                     continue_on_error=False):
        """
        Send http request and validate output by return_code and Exception
        :param method:
        :param log_level:
        :param timeout:
        :param data:
        :param expected_return_codes:
        :param expected_exception:
        :param continue_on_error: if True, throw Exception; else log error and continue
        :return:
        """
        assert method in METHODS, f'method {method} should be in {METHODS}'
        self.start_time = time.time()
        if not expected_return_codes:
            expected_return_codes = [get_test_property('status')]
        message = f'\n\tsending {method} {self.url}'
        for item in [
            'timeout',
            'data',
            'expected_return_codes',
            'expected_exception']:
            if eval(item):
                message += f'\n\t{item} = {eval(item)}'
        log_message(message)
        try:
            if data is None:
                response = request(method=method,
                                   url=self.url,
                                   headers=get_test_property('headers'),
                                   auth=get_test_property('auth'),
                                   timeout=timeout)
            else:
                response = request(method=method,
                                   url=self.url,
                                   headers=get_test_property('headers'),
                                   auth=get_test_property('auth'),
                                   timeout=timeout,
                                   data=json.dumps(data))
            self.execution_time = round(time.time() - self.start_time, 1)
            self.return_code = response.status_code
            self.response = json.loads(response.text)
            if isinstance(self.response, list):
                log_message("returned_records:", log_level=log_level)
                for index, record in enumerate(self.response):
                    log_message(f"\t{index + 1}.{record}", log_level=log_level)
                self.returned_records = len(self.response)
            elif isinstance(self.response, dict):
                self.returned_records = {}
                for _ in self.response:
                    if isinstance(self.response[_], list):
                        self.returned_records[_] = len(self.response[_])
            else:
                self.returned_records = 0
            for item in ['execution_time', 'return_code', 'returned_records']:
                log_message(f"{item}: " + eval(f"str(self.{item})"), log_level=log_level)
            log_message(f"response: {self.response}", log_level='DEBUG')
            condition = f"{self.return_code} in {expected_return_codes}"
            assert_and_log(eval(condition), 'Return Code:' + condition,
                           continue_on_error=continue_on_error)
            if expected_exception is not None:
                assert_and_log(False, f"expected exception {expected_exception} was not raised")
        except Exception as actual_exception:
            if expected_exception and isinstance(actual_exception, expected_exception):
                assert_and_log(True, f'Exception {expected_exception} was thrown as expected')
            else:
                assert_and_log(False, f"Unexpected Exception:{type(actual_exception)}"
                                      f"\n response.text={self.response}",
                               continue_on_error=continue_on_error)
        finally:
            return self
