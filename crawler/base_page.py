import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = None
        #self.logger = pytest.logger
        self.DEFAULT_TIMEOUT_SECONDS = 10

    
    def default_timeout(f):
        """
        Adds the ability to wait for the default amount of 10 seconds
        
        """
        def wrapper(self, *args, **kwargs):
            if 'wait_time_seconds' not in kwargs or kwargs['wait_time_seconds'] is None:
                kwargs['wait_time_seconds'] = self.DEFAULT_TIMEOUT_SECONDS
            return f(self, *args, **kwargs)
        return wrapper

    def navigate(self, url=None):
        if url:
            self.driver.get(url)
        elif self.url is None:
            raise ValueError("URL is not set")
        else:
            self.driver.get(self.url)

    def verify_base_elems_present(self, elems_selector_list):
        """
        Verifies that all elements are present on the page.
        Uses concatenation of selectors to optimize efficiency.
        """
        combined_selector = ", ".join(elems_selector_list)
        self.wait_for_visibility_of_elems(combined_selector)

    def elem(self, css_selector):
        """
        Return a single element based on the css_selector"""
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def elems(self, css_selector):
        """
        Return a list of elements based on the css_selector"""
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)


    @default_timeout
    def wait_for_visibility_of_elems(
        self, css_selector, wait_time_seconds=None
    ):
        """
        Waits for some elements to be visible on the page."""
        wait = WebDriverWait(self.driver, wait_time_seconds)
        elems_list = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        return elems_list
    

    @default_timeout
    def wait_for_invisibility_of_elems(
        self, css_selector, wait_time_seconds=None
    ):
        """
        Waits for some elements to be in-visible on the page."""
        wait = WebDriverWait(self.driver, wait_time_seconds)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector)))


    @default_timeout
    def click(self, css_locator, wait_time_seconds=None):
        """
        Clicks an element based on the css_locator"""
        try:
            wait = WebDriverWait(self.driver, wait_time_seconds)
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_locator))
            ).click()
        except TimeoutException as e:
            #self.logger.error(
            #     f"Element {css_locator} " f"not clickable after {wait_time_seconds}"
            # )
            raise e
        
    @default_timeout
    def enter_text(self, css_locator, text, wait_time_seconds=None):
        """
        Enters text into an element based on the css_locator"""

        wait = WebDriverWait(self.driver, wait_time_seconds)
        try:
            wait = WebDriverWait(self.driver, wait_time_seconds)
            element = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_locator))
            )
            element.send_keys(text)
        except TimeoutException:
            msg = f"Timeout while waiting for element with locator:"
            f" {css_locator} to be visible"
            #self.logger.error(msg)
            raise TimeoutException(msg)

    @default_timeout
    def wait_for_page_title(
        self, title_text, wait_time_seconds=None
    ):
        """
        waits for the page title to be equal to title_text"""
        try:
            WebDriverWait(self.driver, wait_time_seconds).until(EC.title_is(title_text))
        except TimeoutException as e:
            msg = f"times out waiting for {title_text} after {wait_time_seconds}"
            #self.logger.error(msg)
            raise TimeoutException(msg)

    def get_element_attributes(self, css_selector):
        """
        Returns a dictionary of attributes of an element.

        for use in checking for disabled status etc.
        """
        try:
            element = self.elem(css_selector)
            script = (
                "var items = {};"
                " for (index = 0; index < arguments[0].attributes.length; ++index)"
                " { "
                "items[arguments[0].attributes[index].name] "
                "= arguments[0].attributes[index].value };"
                " return items;"
            )
            attributes = self.driver.execute_script(
                script,
                element,
            )
        except JavascriptException:
            errmsg = f"Error getting attributes for {css_selector}"
            #self.logger.error(errmsg)
            raise JavascriptException(errmsg)
        except NoSuchElementException:
            errmsg = f"Element {css_selector} not found"
            #self.logger.error(errmsg)
            raise NoSuchElementException(errmsg)
        except StaleElementReferenceException:
            errmsg = f"Element {css_selector} is stale"
            #self.logger.error(errmsg)
            raise StaleElementReferenceException(errmsg)
        return attributes

    def is_element_disabled(self, css_selector):
        """
        Returns True if the element is disabled, False otherwise."""
        attributes = self.get_element_attributes(css_selector)
        return "disabled" in attributes
