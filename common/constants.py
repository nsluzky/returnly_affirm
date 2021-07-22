"""Constants used in automated testing."""
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
import logging
import os

API_AUTH = os.environ.get('API_AUTH')
LOGGER = logging.getLogger(__name__)
LOG_LEVEL = "INFO"
LOG_LEVEL_DICTIONARY = {
    'c' : CRITICAL,
    'e' : ERROR,
    'w' : WARNING,
    'd' : DEBUG,
    'n' : NOTSET
}

CLI_DEFAULT_PROPERTIES = {
    'branch': 'master',
    'baseurl_api': 'https://returnly-candidates-02.myshopify.com/admin/api/2021-04/',
    'status': 200,
    'max_timeout': 5,
    'headers': {
        'Content-type': 'application/json',
    },
    'auth': ( # in a real project that should not be exposed for security reasons!!!
        'f864d05a60776ca1da81dd4b496dc261',
        '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'
    )
}
DEFAULT_PROPERTIES = {
    'baseurl': 'https://returnly-candidates-02.myshopify.com/',
    'headless': True,
    'driver': 'local',
    'browser' : 'chrome',
    'password' : 'shahll', #in a real project it should not be exposed for security reasons!!!
    'animate':True,
    'save_screenshots':False,
    'animation_time': 0.001,
    'screenshots_folder':'screenshots',
}

DEFAULT_PROPERTIES.update(CLI_DEFAULT_PROPERTIES)

def log_message(message, log_level=LOG_LEVEL):
    """
    log message with LOGGER when log_level is specified as a parameter

    :param message:
    :param log_level:
    :return:
    """
    LOGGER.log(LOG_LEVEL_DICTIONARY.get(log_level[0].lower(), INFO), message)


def get_all_properties(custom_properties={}, log_level='INFO', default=DEFAULT_PROPERTIES):
    """
    Aggregate custom and default properties and log them
    :param custom_properties:
    :param log_level:
    :param default:
    :return:
    """
    props = dict(default)
    props.update(custom_properties)
    # set testname
    if "test" not in props:
        props["test"] = "investigation"
    # set full_name
    props["full_name"] = "_".join([
        props.get("test", ""),
        props.get("branch", ""),
    ])
    os.environ['PARAMS'] = str(props)
    log_message("{} Test properties {}".format(10 * '*', 10 * '*'), log_level)
    for _key in sorted(props):
        log_message("\t{}:{}".format(_key, props[_key]), log_level)
    return props

def set_log_level(log_level="INFO"):
    """
    Set log_level

    :param log_level:
    :return:
    """
    global LOG_LEVEL
    LOGGER.setLevel(LOG_LEVEL_DICTIONARY.get(log_level[0].lower(), INFO))
    LOG_LEVEL = log_level

# Create a stream logger
set_log_level(LOG_LEVEL)
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

# Add a file logger
PROPS = eval(os.environ.get("PARAMS", "{}"))
LOG_FILE = PROPS['log_file'] if 'log_file' in PROPS else 'test.log'
if LOG_FILE:
    FILE_HANDLER = logging.FileHandler(LOG_FILE)
    FILE_HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(FILE_HANDLER)
