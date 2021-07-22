# from investigator import *
"""
 Methods that help investigate webpage and find unique descriptions of fields
'"""
import re
import os
import sys
from time import time#, sleep
from collections import Counter
import traceback
from stringcase import snakecase
from selenium.webdriver.common.by import By

from common.named_by import NamedBy
from common.common_actions import log_message
from common.common_actions import scroll_to
from common.common_actions import animate
from common.common_actions import highlight
from common.common_actions import unhighlight
from common.pages.main_page import MainPage

DEFAULT_STORAGE = os.path.expanduser('~/default_storage')
if not os.path.exists(DEFAULT_STORAGE):
    os.mkdir(DEFAULT_STORAGE)
VISIBLE_ONLY = True


def namedbys(driver, xpath):
    """
    return a list of namedby elements
    :param driver:
    :param xpath:
    :return:
    """
    class Page():
        def __init__(self, driver):
            self.driver = driver
    page = Page(driver)
    result = []
    for index, item in enumerate(get_named_by_elements(driver, xpath)):
        print(item.keys())
        exec(f"result.append(NamedBy('item{index}', 'xpath', \"{item['xpath']}\", page))")
    print("namedby elements:", len(result))
    return result

def remove_duplicates_from_list(input_list, skip_list=[]):
    """
    return list with removed duplicates and elements in skip_list
    :param input_list:
    :return:
    """
    if not isinstance(input_list, list):
        print("input_list is not list, it's {}".format(type(input_list)))
        return input_list
    if not isinstance(skip_list, list):
        print("skip_list is not list, it's {}".format(type(skip_list)))
        skip_list = []
    result = []
    for item in input_list:
        if item not in result and item not in skip_list:
            result.append(item)
    return result

def print_status(counter, total_count, start_time, message=""):
    """ print status on console """
    if (counter + 1) % 1 and (counter + 2 < total_count or total_count < 100):
        return
    passed_time = time() - start_time
    time_to_complete = (total_count - counter) / (counter + 1) * passed_time / 60
    time_total = total_count / (counter + 1) * passed_time / 60
    print("done {} out of {}; {} out of {} min to go; {}; touch /tmp/stop to abort{}".
          format(counter + 1, total_count, round(time_to_complete, 1),
                 round(time_total, 1), message, " " * 5),
          sep='', end="\r", flush=True)

def save(what, where):
    """ save object what in file where """
    if where.find('/') < 0:
        where = os.path.join(DEFAULT_STORAGE, where)
    with open(where, "w") as file_handler:
        file_handler.write(str(what))
        file_handler.flush()
        file_handler.close()

def retrieve(from_where):
    """ retrieve object from file """
    if from_where.find('/') < 0:
        from_where = os.path.join(DEFAULT_STORAGE, from_where)
    if not os.path.exists(from_where):
        raise Exception("file {} does not exist".format(from_where))
    with open(from_where, "r") as file_handler:
        result = file_handler.read()
        return eval(result)

def aggregate_lists_of_namedby_descriptions(lists_of_namedby_descriptions):
    """
    returns an aggregated list of namedby descriptions
    order is preserved
    :param lists_of_namedby_descriptions:
    :return:
    """
    result = []
    xpaths = []
    for descs in lists_of_namedby_descriptions:
        temp = retrieve(descs)
        for item in temp:
            if item['xpath'] not in xpaths:
                xpaths.append(item['xpath'])
                result.append(item)
        print("Adding from {} {} long; got:{}".format(descs, len(temp), len(result)))
    return result

def break_it(name="/tmp/stop"):
    """ Break if file exists"""
    if os.path.exists(name):
        return True
    return False

'''
#def append_from_xpaths(base_name, to_append, new_name, log_level="INFO"):
    """
    Append records from to_append that are missing in base_name
    and save them under new_name
    :param base_name:
    :param to_append
    :param new_name:
    :param log_level:
    :return:
    """
        base_list = retrieve(base_name)
    log_message("{} is {} long".format(base_name, len(base_list)), log_level)
    to_append_list = retrieve(to_append)
    log_message("{} is {} long".format(to_append, len(to_append_list)), log_level)
    xpaths = [item['xpath'] for item in base_list]
    for item in to_append_list:
        if item['xpath'] not in xpaths:
            base_list.append(item)
    log_message("{} is {} long".format(new_name, len(base_list)), log_level)
    save(base_list, new_name)
'''

def get_xpaths(name, log_level="INFO"):
    """
    Retrieve file from storage and return a set of it's paths
    :param name:
    :return:
    """
    try:
        result = {item['xpath'] for item in retrieve(name)}
        log_message("{} is retrieved; it's {} long".format(name, len(result)), log_level)
        return result
    except Exception as exception:
        traceback.print_tb(sys.exc_info()[1])
        log_message(exception, "ERROR")
        raise Exception("Can't retrieve {} from the storage".format(name))

def diff(name1, name2, log_level="INFO"):
    """
    Retrieve xpaths from stored files and compare them
    :param name1:
    :param name2:
    :param log_level:
    :return:
    """
    set1 = get_xpaths(name1, log_level=log_level)
    set2 = get_xpaths(name2, log_level=log_level)
    if set1 == set2:
        log_message("Sets are identical")
    else:
        if set1 - set2:
            log_message("{} Missing {} in set2 {}".
                        format(10 * '*', len(set1 - set2), 10 * '*'), 'WARN')
            for counter, item in enumerate(sorted(list(set1 - set2))):
                log_message("{}. {}".format(counter + 1, item), log_level)
        if set2 - set1:
            log_message("{} Missing {} in set1 {}".
                        format(10 * '*', len(set2 - set1), 10 * '*'), 'WARN')
            for counter, item in enumerate(sorted(list(set2 - set1))):
                log_message("{}. {}".format(counter + 1, item), log_level)

def get_elements(
        driver,
        by_xpath=None, element=None, elements=None, by_css=None, by_id=None,
        visible_only=True):
    """
    Get visible elements by one of the parameters
    If container is specified, looking only in that container
    :param driver:
    :param by_xpath:
    :param element:
    :param elements:
    :param by_css:
    :param by_id:
    :param visible_only
    :return:
    """
    if by_xpath:
        result = get_by_xpath(driver, by_xpath, visible_only)['elements']
    elif by_id:
        result = get_by_id(driver, by_id, visible_only)['elements']
    elif by_css:
        result = get_by_css(driver, by_css, visible_only)['elements']
    elif element:
        result = [element]
    elif elements:
        result = elements
    else:
        raise Exception("specify one of: by_xpath, by_id, by_css, element, elements")
    return result

def show_elements(
        driver,
        by_xpath=None, element=None, elements=None, by_css=None, by_id=None,
        visible_only=VISIBLE_ONLY, container_xpath='', container_name=''):
    """
    Displays specified elements and their properties
    If container is specified, lookin in the container only
    :param driver:
    :param by_xpath:
    :param element:
    :param elements:
    :param by_css:
    :param by_id:
    :param visible_only:
    :return:
    """
    elems = get_elements(
        driver,
        by_xpath=by_xpath, element=element, elements=elements, by_css=by_css, by_id=by_id,
        visible_only=visible_only)
    highlight_elements(driver, elements=elems)
    for counter, item in enumerate(elems):
        try:
            dic = get_named_by_element(
                driver, item, visible_only=visible_only,
                container_xpath=container_xpath, container_name=container_name)
            if not dic:
                continue
            result.append(dic)
            print("{}. {}".format(counter + 1, dic['namedby_dict']['xpath']))
            for attr in dic['namedby_dict']['attrs']:
                print("\t{} = '{}'".format(attr, dic['namedby_dict']['attrs'][attr]))
        except:
            traceback.print_tb(sys.exc_info()[1])
            print("Error while processing {}".format(str(item)))
    input("Enter to continue:")
    unhighlight_elements(driver, elements=elems)

def get_attributes_by_xpath(driver, by_xpath, visible_only=VISIBLE_ONLY, container=''):
    """
    get attributes of elements matching xpath (optionally in a container)
    :param driver:
    :param by_xpath:
    :param visible_only:
    :param container:
    :return:
    """
    elements = get_by_xpath(driver, by_xpath, visible_only, container=container)['elements']
    print("There are {} elements matching xpath {}".format(len(elements), by_xpath))
    for item in elements:
        attrs = get_elements_attributes(driver, item)
        for attr in attrs:
            print("{} -> {}".format(attr, attrs[attr]))

def get_elements_attributes(driver, element):
    """ return elements attributes"""
    result = driver.execute_script(
        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) '
        '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }'
        '; return items;', element)
    result["_text"] = element.text.split('\n')[0]
    result["_tag_name"] = element.tag_name
    result['_location'] = element.location
    result['_size'] = element.size
    return result

def get_elements_css_values(driver, element):
    """
    return all elements by_css values
    :param driver:
    :param element:
    :return:
    """
    animate(driver, element)
    styleprops_dict = driver.execute_script(
        'var items = {};' +
        'var compsty = getComputedStyle(arguments[0]);' +
        'var len = compsty.length;' +
        'for (index = 0; index < len; index++)' +
        '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};' +
        'return items;', element)
    return styleprops_dict

def get_by_xpath(driver, by_xpath, desc="by_xpath", visible_only=VISIBLE_ONLY, container=''):
    """ get NamedBy element and corresponding WebElements by xpath """
    return get_by_namedby(
        NamedBy(
            desc, By.XPATH, container + by_xpath, MainPage(driver)),
        visible_only=visible_only)

def get_by_id(driver, id_value, desc="by_id", visible_only=VISIBLE_ONLY):
    """
    get NamedBy element and corresponding WebElements by id_value
    :param driver:
    :param id_value:
    :param desc:
    :param visible_only:
    :return:
    """
    return get_by_namedby(
        NamedBy(
            desc, By.ID, id_value, MainPage(driver)),
        visible_only=visible_only)

def get_by_css(driver, by_css, desc="by_css", visible_only=VISIBLE_ONLY):
    """
    get NamedBy element and corresponding WebElements by id_value
    :param driver:
    :param by_css:
    :param desc:
    :param visible_only:
    :return:
    """
    return get_by_namedby(
        NamedBy(
            desc, By.CSS_SELECTOR, by_css, MainPage(driver)),
        visible_only=visible_only)

def get_by_namedby(namedby, visible_only=VISIBLE_ONLY):
    """ return namedby and corresponding WebElements """
    try:
        result = {'namedby': namedby, 'elements': namedby.find_visible_elements(0) \
              if visible_only else namedby.find_elements(0)}
    except Exception as exception:
        traceback.print_tb(sys.exc_info()[1])
        print("Can not create namedby {}".format(str(namedby)))
        print(str(exception))
        result = {'namedby': namedby,
                  'elements': []}
    return result

def check_page(driver, page):
    """
    check descriptions on page
    :param driver:
    :param page:
    :return:
    """
    names = []
    for namedby_field in dir(page):
        if namedby_field.startswith("__"):
            continue
        by_elem = eval("page.{}".format(namedby_field))
        if isinstance(by_elem, NamedBy):
            names.append([namedby_field, by_elem])
    for counter, item in enumerate(sorted(names)):
        if break_it():
            break
        name, by_elem = item
        highlight_elements(driver, by_elem.by_definition, color='red')
        input("{}. {} {} {}".format(counter + 1, name, by_elem.description, by_elem.by_definition))
        highlight_elements(driver, by_elem.by_definition, color='blue', width=1)

def get_elements_described_on_page(page, visible_only=VISIBLE_ONLY, show_status=True):
    """ get elements described on a page's instance """
    result = []
    start_time = time()
    total_count = len(dir(page))
    print("page {} has {} elements".format(str(page), total_count))
    for counter, namedby_field in enumerate(dir(page)):
        if show_status:
            print_status(counter, total_count, start_time,
                         message="{} elements detected".format(
                             len(remove_duplicates_from_list(result))))
        if break_it():
            break
        if namedby_field.startswith("__"):
            continue
        by_elem = eval("page.{}".format(namedby_field))
        try:
            if isinstance(by_elem, NamedBy):
                if visible_only:
                    elems = by_elem.find_visible_elements(0)
                else:
                    elems = by_elem.find_elements(0)
                result.extend(elems)
                result = remove_duplicates_from_list(result)
        except:
            traceback.print_tb(sys.exc_info()[1])
            print("error while processing {}".format(namedby_field))
    print("\nfound {} {} described on {}".format(
        len(result), "visible elements" if visible_only else "elements", str(page)))
    return remove_duplicates_from_list(result)

def get_namedby_described_on_page(page):
    """ get namedby elements described on a page's instance """
    result = []
    total_count = len(dir(page))
    print("page {} has {} elements".format(str(page), total_count))
    for namedby_field in dir(page):
        if namedby_field.startswith("__"):
            continue
        by_elem = eval("page.{}".format(namedby_field))
        if isinstance(by_elem, NamedBy):
            result.append(
                {'text': namedby_field,
                 'xpath': eval("page.{}.by_definition".format(namedby_field)),
                 'response': ''})
    print("\nfound {} namedby fields described on {}".format(
        len(result), str(page)))
    return result

def set_tooltips(page, color='red', width=2):
    """
    Set tooltips to elements described on page and highlight them
    :param page:
    :return:
    """
    namedby_elements = [] # assigning as associative array didn't work :-( use an appending loop
    for item in dir(page):
        if isinstance(eval("page.{}".format(item)), NamedBy):
            namedby_elements.append([item, eval("page.{}".format(item))])
    for name, named_by in namedby_elements:
        for index, element in enumerate(named_by.find_visible_elements(0, log_level='DEBUG')):
            tooltip = "{}({}) {}".format(name, index + 1, type(page))
            page.driver.execute_script('arguments[0].setAttribute("title", "{}")'.format(
                tooltip), element)
            highlight_elements(page.driver, element=element, color=color, width=width)

def get_elements_by_namedby_description(namedby_line, visible_only=VISIBLE_ONLY):
    """
    Return elements matching mamedby_line
    :param namedby_line:
    :return:
    """
    result = list()
    try:
        matcher = re.match(r'.*(By\.[A-Z]+,.*), self\)', namedby_line)
        if matcher:
            by_elem = eval(
                "NamedBy('generated', {}, MainPage(driver))".format(matcher.group(1)))
            if visible_only:
                elems = by_elem.find_visible_elements(0)
            else:
                elems = by_elem.find_elements(0)
            result = elems
    except:
        traceback.print_tb(sys.exc_info()[1])
        print("error while processing {}".format(namedby_line))
    finally:
        return result

def get_elements_by_namedby_list(namedby_list, visible_only=VISIBLE_ONLY, show_status=True):
    """ get elements described in a list of namedby definitions """
    result = []
    total_count = len(namedby_list)
    print("list contains {} namedby definitions".format(total_count))
    start_time = time()
    for counter, namedby_field in enumerate(namedby_list):
        if show_status:
            print_status(counter, total_count, start_time,
                         message="{} elements detected".format(
                             len(remove_duplicates_from_list(result))))
        if break_it():
            break
        result.extend(get_elements_by_namedby_description(
            namedby_field, visible_only=visible_only))
    print("\nfound {} {} described in the list".format(
        len(result), "visible elements" if visible_only else "elements"))
    return result

def get_full_name(text, tag):
    """
    Join text, and tag ro get full name
    :param text_in_english:
    :param tag:
    :return:
    """
    return re.sub(' +', ' ', ' '.join([str(text), str(tag)])).strip()

def get_candidate(
        driver, params, param, attrs, visible_only=VISIBLE_ONLY,
        container_xpath='', container_name=''):
    """
    Create a NamedBy description based on element's properties
    If container is specified, looking only a specified container
    :param driver:
    :param params:
    :param param:
    :param attrs:
    :param visible_only:
    :param container_xpath:
    :param container_name:
    :return:
    """
    """ create a NamedBy element and its description based on set of its parameters """
    extended_params = params[:]
    extended_params.append(param)
    pattern_digits = '(.*?)([0-9]{4,}|-[0-9]+)(.*)'
    pattern_link = r'(https?://[^/]*)?/([^\.\?]+)'
    try:
        descriptions = []
        for para in extended_params:
            temp = attrs[para]
            matcher_link = re.match(pattern_link, temp)
            if matcher_link:
                temp = matcher_link.group(2)
            if temp.find("'") > -1 or temp.find('\n') > -1:
                continue # skip parameters with ' in values
            matcher_many_digits = re.match(pattern_digits, temp)
            if matcher_many_digits:
                while matcher_many_digits:
                    temp = '*'.join([matcher_many_digits.group(1), matcher_many_digits.group(3)])
                    matcher_many_digits = re.match(pattern_digits, temp)
                array = temp.split('*')
                to_skip = []
                for index1 in range(len(array) - 1):
                    for index2 in range(index1 + 1, len(array)):
                        if array[index1] in array[index2]:
                            to_skip.append(array[index1])
                for piece in array:
                    if piece and piece not in to_skip:
                        descriptions.append("contains(@{}, '{}')".format(para, piece))
            else:
                if temp == attrs[para]:
                    descriptions = ["@{}='{}'".format(para, temp)]
                else:
                    descriptions = ["contains(@{}, '{}')".format(para, temp.strip())]
        xpath = "{}//{}[{}]".format("" if container_xpath == "//*" else container_xpath, \
            attrs.get('_tag_name', "*"), " and ".join(descriptions))
        if attrs.get('_text', ""):
            text_in_english = attrs['_text']
        elif attrs.get('placeholder', ""):
            text_in_english = attrs['placeholder']
        elif attrs.get('title', ""):
            text_in_english = attrs['title']
        else:
            text_in_english = "TBD"
        if container_name:
            text_in_english = ':'.join([container_name, text_in_english])
        named_by_dict = get_by_xpath(driver, xpath, visible_only=visible_only)
        return {
            'elements': named_by_dict["elements"],
            'namedby_dict': {
                'xpath': xpath,
                'text': text_in_english,
                'full_text': get_full_name(text_in_english, attrs['_tag_name']),
                'triage': "l", # to be determined later
                'elements_number': len(named_by_dict["elements"]),
                'attrs': attrs  # all the attrs
            }
        }
    except Exception as exception:
        traceback.print_tb(sys.exc_info()[1])
        print("failure: params={}; param='{}'; attrs={}".format(params, param, attrs))
        print(exception)
        return None

def get_all_properties_from_elements(driver, elements):
    """ get all properties used in a list of elements """
    counter = Counter()
    for elem in elements:
        attrs = get_elements_attributes(driver, elem)
        for attr in attrs:
            if attrs[attr]:
                counter[attr] += 1
    for item in sorted(counter.keys()):
        print("{}:{}".format(item, counter[item]))

def convert_name(field):
    """ return snake_case of a string """
    result = field
    matcher = re.match('^([A-Z]{2,})(.*)', result)
    if matcher:
        result = "_".join([matcher.group(1).lower(), matcher.group(2)])
    while True:
        matcher = re.match('(.*?)([A-Z]{2,})(.*)', result)
        if matcher:
            result = "_".join([matcher.group(1), matcher.group(2).lower(), matcher.group(3)])
        else:
            break
    while True:
        matcher = re.match('(.*)([A-Z].*)', result)
        if matcher:
            result = "_".join([matcher.group(1), matcher.group(2).lower()])
        else:
            break
    if result[0] == "_":
        result = result[1:]
    if result[len(result) - 1] == "_":
        result = result[:len(result) - 1]
    return re.sub("_+", "_", result)

def get_named_by_element(
        driver, element, skip=[], visible_only=VISIBLE_ONLY,
        container_xpath="", container_name=""):
    """
    return named_by description for a webelemen
    if container is specified, looking inside it
    :param driver:
    :param element:
    :param skip:
    :param visible_only:
    :param container_xpath:
    :param container_name:
    :return:
    """
    """ return named_by description for a webelement"""
    elements = None
    if element in skip:
        return None
    attrs = get_elements_attributes(driver, element)
    best_candidate = {}
    params = []
    parameters_to_check = []
    #for item in attrs:
    #    if item.startswith("data") or item.startswith('area') and attrs[item]:
    #        parameters_to_check.append(item)
    for item in ["name", "class", "data-tracking-name", "selected", "checked", "role", "for",
                 "type", "href", "src", "id", "placeholder"]:
        if item in attrs and attrs[item]:
            parameters_to_check.append(item)
    for item in ["rel", "selected", "translate"]:
        if item in attrs and attrs[item]:
            parameters_to_check.append(item)
    if not parameters_to_check:
        return None
    for param in parameters_to_check:
        candidate_dict = get_candidate(
            driver, params, param, attrs, visible_only=visible_only,
            container_xpath=container_xpath, container_name=container_name)
        if not candidate_dict:
            continue
        candidate = candidate_dict['namedby_dict']
        if not candidate:
            print("failed to get candidate")
            for item in attrs:
                if attrs[item]:
                    print("{}:{}".format(item, attrs[item]))
            continue
        if not elements or candidate['elements_number'] < len(elements):
            elements = candidate_dict['elements']
            best_candidate = candidate
            if candidate['elements_number'] < 2:
                break
            params.append(param)
    return {'namedby_dict':best_candidate,
            'elements':elements}

def get_named_by_elements(
        driver, by_xpath=None, by_id=None, by_css=None, element=None,
        elements=None, skip=[], show_status=True, visible_only=False,
        container_xpath='', container_name=''):
    """
    Returns a list of namedbys for a specified set of elements
    First of assigned parameters: by_xpath, by_id, by_css, element, elements is taken
    If container is specified, looking in the container only
    :param driver:
    :param by_xpath:
    :param by_id:
    :param by_css:
    :param element:
    :param elements:
    :param skip:
    :param show_status:
    :param visible_only:
    :param container_xpath:
    :param container_name:
    :return:
    """
    list_of_elements = get_elements(
        driver,
        by_xpath=by_xpath, element=element, elements=elements, by_css=by_css, by_id=by_id,
        visible_only=visible_only)
    list_of_elements = remove_duplicates_from_list(list_of_elements, skip)
    skip = []
    total_count = len(list_of_elements)
    if total_count > 10:
        print("web_elements={}".format(total_count))
    start_time = time()
    named_list = []
    for counter, item in enumerate(list_of_elements):
        if show_status:
            print_status(
                counter, total_count, start_time, message="{} definitions created".format(
                    len(named_list)))
        if break_it():
            break
        if item in skip:
            continue
        namedby = get_named_by_element(
            driver, item, skip=skip,
            container_xpath=container_xpath, container_name=container_name)
        if not namedby:
            continue
        if namedby['elements']:
            skip.extend(namedby['elements'])
            named_list.append(namedby['namedby_dict'])
        skip = remove_duplicates_from_list(skip)
    return named_list

def tune_and_accept_namedby(
        driver, webelement, container_xpath="", container_name=''):
    """
    allows the user to accept or select a custom name to namedby
    If container is specified, looking in the container only
    :param driver:
    :param namedby:
    :param container_xpath:
    :param container_name:
    :return:
         dictionary
             xpath - generated or custom xpath of the element
             text - generated name of the element
             elements - web-elements corresponding xpath
             triage-response: a - accepted or s - skipped
    """
    candidate = get_named_by_element(
        driver, webelement, container_xpath=container_xpath, container_name=container_name)
    if not candidate:
        return None
    candidate_xpath = candidate['namedby_dict'].get('xpath', '')
    candidate_text = candidate['namedby_dict'].get('full_text', '')
    candidate_elements = candidate.get('elements', list())
    if not candidate_elements:
        return None
    response = ''
    while not response \
            or response != "s" \
            or (response == 'a' and not candidate_elements):
        if break_it():
            break
        highlight_elements(driver, elements=candidate_elements)
        attrs = candidate['namedby_dict'].get('attrs', [])
        print('***********attributes**********')
        for attr in attrs:
            print("\t{}:{}".format(attr, attrs[attr]))
        response = input(
            "{} element(s) match '{}' {}\nenter"
            " a-accept,"
            " s-skip"
            " or custom xpath:". \
                format(len(candidate_elements), candidate_xpath, candidate_text))
        if response == 'a':
            candidate['namedby_dict']['xpath'] = candidate_xpath
            highlight_elements(driver, elements=candidate_elements, color='blue')
            break
        unhighlight_elements(driver, elements=candidate_elements)
        if response == 's':
            candidate['namedby_dict']['xpath'] = candidate_xpath
            break
        if not response or len(response) < 3:
            response = ''
            continue
        try:
            candidate_xpath = response
            candidate_elements = get_by_xpath(driver, candidate_xpath)['elements']
            highlight_elements(driver, elements=candidate_elements)
        except:
            print("invalid xpath '{}'".format(candidate_xpath))
            candidate_elements = []
        finally:
            response = ""
    return {'text':candidate_text,
            'xpath':candidate_xpath,
            'elements':candidate_elements,
            'response':response}

def process_container(driver, container_xpath='//*', accumulated=[], container_name=""):
    """
    Process container specified by its xpath
        empty "processed_list"
        Create a list of all elements in the container - new list
    :param driver:
    :param container_xpath:
    :param accumulated:
    :return:
    """
    result = []
    driver.switch_to.window(driver.window_handles[0])
    all_elements_in_container = get_by_xpath(driver, container_xpath)['elements']
    all_elements_in_container.extend(get_by_xpath(driver, container_xpath + "//*")['elements'])
    all_elements_in_container = list(set(all_elements_in_container))
    unhighlight_elements(driver, elements=all_elements_in_container)
    processed_elements = []
    for item in accumulated:
        elements = get_by_xpath(driver, item['xpath'], visible_only=True)['elements']
        processed_elements.extend(elements)
        if item['response'] == 'a':
            highlight_elements(driver, elements=elements, color='green', width=1)
    new_list = [item for item in all_elements_in_container if item not in processed_elements]
    processed_in_loop = []
    for counter, webelement in enumerate(new_list):
        print("\n********** processing {} out of {}".format(counter + 1, len(new_list)))
        if webelement in processed_in_loop:
            continue
        while True:
            if break_it():
                break
            item = tune_and_accept_namedby(
                driver, webelement,
                container_xpath=container_xpath, container_name=container_name)
            if not item:
                break
            processed_in_loop.extend(item['elements'])
            if item['response'] and item['response'] in 'as':
                result.append(item)
            if item['response'] != 'n':
                break
    return result

def triage(driver, descriptions):
    """
    triage descriptions: delete, edit, add
    :param driver:
    :param descriptions:
    :return: updated set of descriptions
    """
    result = []
    accepted = 0
    for item in descriptions:
        if item['response'] == 'a':
            accepted += 1
            highlight_elements(driver, item['xpath'], color='blue', width=2)
    counter = 0
    for item in descriptions:
        if item['response'] != 'a':
            result.append(item)
            continue
        counter += 1
        print('\n*****{}. out of {} ("{}", "{}")'.format(
            counter + 1, accepted, item['text'], item['xpath']))
        while True:
            if break_it():
                break
            highlight_elements(driver, item['xpath'], color='red', width=10)
            item['response'] = input("a-accept; s-skip; enter new name:")
            if item['response'] == 'a':
                highlight_elements(driver, item['xpath'], color='green')
                result.append(item)
                break
            if item['response'] == 's':
                unhighlight_elements(driver, item['xpath'])
                result.append(item)
                break
            item['text'] = item['response']
    return result

def highlight_elements(
        driver, by_xpath=None, element=None, elements=None, namedby=None, page=None,
        by_css=None, by_id=None, log_level='DEBUG', width=3, color='red'):
    """
    Red-border the specified elements
    :param driver:
    :param by_xpath:
    :param element:
    :param elements:
    :param namedby: a NamedBy instance
    :param page: instance of a page with NamedBy descriptions
    :param by_css:
    :param by_id:
    :param log_level:
    :param width: width of border
    :param color: color of border
    :return:
    """
    try:
        if page:
            elems = get_elements_described_on_page(page)
        else:
            if namedby:
                if namedby.by_type == By.XPATH:
                    by_xpath = namedby.by_definition
                elif namedby.by_type == By.CSS_SELECTOR:
                    by_css = namedby.by_definition
                elif namedby.by_type == By.ID:
                    by_id = namedby.by_definition
            elems = get_elements(
                driver,
                by_xpath=by_xpath, element=element, elements=elements, by_css=by_css, by_id=by_id,
                visible_only=True)
        print("{} visible elements".format(len(elems)))
        for item in elems:
            highlight(driver, item, width=width, color=color)
        if elems:
            scroll_to(driver, elems[0], log_level)
        return True
    except:
        return False

def unhighlight_elements(
        driver, by_xpath=None, element=None, elements=None, by_css=None, by_id=None):
    """
    Remove highlighting the specified element
    :param driver:
    :param by_xpath:
    :param element:
    :param elements:
    :param by_css:
    :param by_id:
    :return:
    """
    try:
        elems = get_elements(
            driver,
            by_xpath=by_xpath, element=element, elements=elements, by_css=by_css, by_id=by_id,
            visible_only=True)
        for item in elems:
            unhighlight(driver, item)
        return True
    except:
        return False

def view_on_several_drivers(
        drivers, by_xpath=None, element=None, elements=None, by_css=None, by_id=None):
    """
    Highligt-unhighligt elements on a set of drivers
    :param drivers:
    :param by_xpath:
    :param element:
    :param elements:
    :param by_css:
    :param by_id:
    :return:
    """
    for driver, name in drivers:
        driver.switch_to.window(driver.window_handles[0])
        try:
            elems = get_elements(
                driver, by_xpath=by_xpath, element=element, elements=elements,
                by_css=by_css, by_id=by_id, visible_only=True)
            highlight_elements(driver, elements=elems)
        except Exception as exception:
            traceback.print_tb(sys.exc_info()[1])
            print(exception)
            elems = []
        finally:
            try:
                input("{} visible elements in {}".format(len(elems), name))
                unhighlight_elements(driver, elements=elems)
            except:
                pass

def write_patterns(triaged_descriptions, output, container_xpath=''):
    """
    write patterns of descriptions to a file
    :param triaged_descriptions
    :param output: resulting file
    :param container_xpath:
    :return:
    """
    sorted_descs = sorted(triaged_descriptions, key=lambda k: k['text'].lower())
    translator_dict = {
        '+':' plus',
        '-':' minus',
        '&':' and',
        '...':' dots',
    }
    with open(output, "w") as file_handler:
        file_handler.write('''""" Objects and methods Related to TEMPLATE """
from selenium.webdriver.common.by import By

from common.named_by import NamedBy

class TEMPLATE:
    """
    Describes objects and methods of TEMPLATE
    """
    def __init__(self, driver):
        self.driver = driver
''')
        if container_xpath:
            file_handler.write('{}container_xpath = "{}"\n'.format(8 * ' ', container_xpath))
        names = []
        for item in sorted_descs:
            if item['response'] == 's':
                continue
            name = item['text']
            for change in translator_dict:
                name = name.replace(change, translator_dict[change])
            name = re.sub("[^a-zA-Z _]+", " ", name)
            name = snakecase(re.sub(r'[^a-zA-Z0-9 _]', ' ', name).strip())
            name = re.sub("[ _]+", "_", name)
            names.append(name)
            file_handler.write("{}self.{} = NamedBy(\n".format(8 * ' ', name))
            file_handler.write('{}"{}", By.XPATH,\n'.format(12 * ' ', item['text']))
            if container_xpath and item['xpath'].startswith(container_xpath):
                file_handler.write(
                    '{}container_xpath + "{}",\n'.format(
                        12 * ' ', item['xpath'][len(container_xpath):]))
            else:
                file_handler.write(
                    '{}"{}",\n'.format(12 * ' ', item['xpath']))
            file_handler.write("{}self)\n".format(12 * ' '))
        file_handler.write('''
        # fields that should be visible
        self.basic_validation_list = [
''')
        for name in sorted(names):
            file_handler.write("{}self.{},\n".format(12 * " ", name))
        file_handler.write('''
        ]
    def validate_url(self):
        """
        validate url of the page
        :return:
        """
        #MainPage(self.driver).assert_url_contains("https://search.ancestry")
        #MainPage(self.driver).assert_url_equals(expected_url)

''')
