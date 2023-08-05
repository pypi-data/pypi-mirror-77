# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from ._path import GUMMY_DIR
from .coloring_utils import toBLUE, toGREEN, toRED
from .generic_utils import print_log, getLatestFileName, try_wrapper

def get_chrome_options(browser=False):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if not browser:
        chrome_options.add_argument('--headless')
    else:
        chrome_options.add_experimental_option("prefs", {
            # "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": 1,
            "download.default_directory": GUMMY_DIR,
            "directory_upgrade": True,
        })
        chrome_options.add_argument('--kiosk-printing')

    return chrome_options

def check_driver(chrome_options=get_chrome_options(browser=False), selenium_port="4444"):
    DRIVER_TYPE = "none"
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            DRIVER_TYPE = "local"
            print_log(is_succeed=True, pos="local")
    except:
        print_log(is_succeed=False, pos="local")

    try:
        with webdriver.Remote(
            command_executor=f'http://selenium:{selenium_port}/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME.copy(),
            options=chrome_options) as driver:
            DRIVER_TYPE = "remote"
            print_log(is_succeed=True, pos="remote")
    except:
        print_log(is_succeed=False, pos="remote")
    return DRIVER_TYPE

############################
#  START: Check driver
############################

try:
    __DRIVER_SETUP__
except NameError:
    DRIVER_TYPE = check_driver(chrome_options=get_chrome_options(browser=False))
    print(f"DRIVER_TYPE: {toGREEN(DRIVER_TYPE)}")
    __DRIVER_SETUP__ = True

############################
#  END: Check driver
############################


def get_driver(chrome_options=None, browser=False, selenium_port="4444"):
    print(f"DRIVER_TYPE: {toGREEN(DRIVER_TYPE)}")
    if chrome_options is None:
        chrome_options = get_chrome_options(browser=browser)
    if DRIVER_TYPE=="remote":
        driver = webdriver.Remote(command_executor=f'http://selenium:{selenium_port}/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME.copy(),
                                  options=chrome_options)
        return driver
    elif DRIVER_TYPE=="local":
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    else:
        msg = "Could not create an instance of the 'chromedriver'. " + \
        "If you can not prepare 'chromedriver' executable locally, " + \
        "please build the environment with Dockerfile. Please see" + \
        toBLUE("https://github.com/iwasakishuto/Translation-Gummy/tree/master/docker")
        raise ValueError(msg)

def try_find_element(driver, identifier, by, timeout=3):
    return try_wrapper(
        func=WebDriverWait(driver=driver, timeout=timeout).until,
        msg_=f"locate element with {toGREEN(by)}={toBLUE(identifier)}",
        method=lambda x: x.find_element(by=by, value=identifier)
    )

def try_find_element_send_keys(driver, by, identifier, values=(), target=None, timeout=3, verbose=True):
    if target is None:
        target = try_find_element(driver=driver, identifier=identifier, by=by, timeout=timeout)
    try_wrapper(
        target.send_keys,
        *tuple(values),
        msg_=f"fill {toBLUE(values)} in element with {toGREEN(by)}={toBLUE(identifier)}",
        verbose_=verbose,
    )
    
def try_find_element_click(driver, by, identifier, target=None, timeout=3, verbose=True):
    if target is None:
        target = try_find_element(driver=driver, identifier=identifier, by=by, timeout=timeout)
    if target is not None:
        def element_click(driver, target):
            try:
                driver.execute_script("arguments[0].click();", target)
            except StaleElementReferenceException:
                target.click()
        try_wrapper(
            func=element_click,
            msg_=f"click the element with {toGREEN(by)}={toBLUE(identifier)}",
            verbose_=verbose,
            driver=driver,
            target=target,
        )

def click():
    """ function for differentiation """

def pass_forms(driver, **kwargs):
    for k,v in kwargs.items():
        if callable(v) and v.__qualname__ == "click":
            try_find_element_click(driver=driver, by="id", identifier=k)
        else:
            try_find_element_send_keys(driver=driver, by="id", identifier=k, values=v)

def download_PDF_with_driver(url, dirname=".", verbose=True, timeout=3):
    chrome_options = get_chrome_options(browser=True)
    if "prefs" not in chrome_options._experimental_options:
        chrome_options._experimental_options["prefs"] = {}
    chrome_options._experimental_options["prefs"]["download.default_directory"] = dirname
    chrome_options._experimental_options["prefs"]["plugins.always_open_pdf_externally"] = True
    if verbose: print(f"Downloading PDF from {toBLUE(url)}")
    with get_driver(chrome_options=chrome_options) as driver:
        driver.get(url)
        for _ in range(timeout):
            time.sleep(1)
            path = getLatestFileName(dirname=dirname)
            if not path.endswith(".crdownload"):
                break
    if verbose: print(f"Save PDF at {toBLUE(path)}")
    return path

def wait_until_all_elements(driver, timeout, verbose=True):
    if verbose: print(f"Wait up to {timeout}[s] for all page elements to load.")
    WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_all_elements_located)
    time.sleep(timeout)

def scrollDown(driver, verbose=True):
    if verbose: print("Scroll down to the bottom of the page.")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")     
    # driver.find_element_by_tag_name('body').click()
    # driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)    
