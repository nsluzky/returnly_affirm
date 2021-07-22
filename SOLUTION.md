Document the high-level solution in a SOLUTION.md file (general approach, frameworks you've used, how to run the solution...).

The solution includes several levels of hierarchy:
1. Jenkins job where we can specify which tests to run, which browser to take, and so on.
    That job digests that data and starts jobs on level2 in parallel. 
    These jobs run concurrently on all available resources.
    Groovy code of this job is located at jenkins/groovy/python_pipeline.gtoovy
2. Jenkins job for a single test execution.
   Currently I have only my laptop - master node that runs 5 executors concurrently - enough to support 5 webdriver sessions
   In a real project these jobs would be running on both master and slave cloud nodes.
   When needed, slaves would be added for scalability, when not needed - stopped to save money
   Groovy code of this job is located at jenkins/groovy/run_unit_test.groovy
   
3. UnitTest and basetests. Unittest is python out-of-the-box unit testing framework similar to Junit.
   It's rather simple and allows providing default setUp and tearDown and aggregating tests.
   There are basetests for cli (common/base_tests/cli_basetest.py) and gui tests ((common/base_tests/gui_basetest.py))
   Actually gui are hybrid tests as they include settings for cli testing as well
4.  Wrapper of python's requests package - script to process HTTP Requests.
    It has a simple interface, uses defaults, logging and validations.
    That makes performing these actions very easy.
    Script is located at common/process_request.py
5.  Wrapper of python's Selenium package By.
    It facilitates Selenium usage by providing good built-on actions
    like logging, error handling, waiting if needed, and many more additional options.
    Using this tool greatly facilitates creation and maintenance of gui automation and making tests
    more stable and results easy to use. 
    The script is located at common/named_by.py
    
7.  common/constants.py contains defaults and other entities used by tests including LOGGERs.
    
8.  common/common_actions.py contain many useful actions used in tests.
    For example, assert_and_log and check_failed_assertions that allow validating assertions
    with logging when assertion passed - it's convenient to as test's log becomes "steps to reproduce"
    continue_on_error parameter makes it like "soft assertion" to continue execution without aborting
    Having check_failed_assertions in tests' teardowns throws Exception if at least one assertion failed
    
9.  common/browser_init.py is used to start webdriver, and login to home page.
    According to parameters, different browsers and different options are used.
    Currently it allows starting Chrome or Firefox locally with and without headless option.
    If needed it could be extended to start SauceLabs or a remote browser (IMO it's not a good idea because of slow performance)
    
10. Folder common/pages contains descriptions of elements on Web Pages and commonly used methods.
    Pages also contain basic_validation_list that specifies which are "major" fields that should be always visible on the page
    These lists are very convenient to check whether all these fields are present and visible.
    See for example test common/tests/returnly/gui/page_verification/tc202_catalog.py
    
11. Folder common/tests contains different tests that are subclasses of base tests.

12. Folder common/data contains data to generate backend objects.

13. tools/random_strings.py contains method to generate random data

There are also scripts common/investigator.py and common/explorer.py that help creating pages,
tests, and help debugging and triaging
    
    

