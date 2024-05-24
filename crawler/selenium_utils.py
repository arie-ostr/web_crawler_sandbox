# Lib imports
import pytest
import logging
import os
from datetime import datetime

# object imports
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_chromedriver():
    """
    Using selenium driver manager for effective driver management.
    Con : downlaod webdriver each test run(it's cached tho)
    """
    #logger.debug("Getting chromedriver")
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    service = Service(ChromeDriverManager().install())
    driver_instance = webdriver.Chrome(service=service, options=chrome_options)

    #driver_version = service.service_url.split("/")[-1]
    # logger.info(
    #     f"ChromeDriver initialized successfully with " f"version: {driver_version}"
    # )

    return driver_instance
