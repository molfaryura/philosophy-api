"""Flask Selenium Test Configuration

This conftest.py file contains configuration and fixtures for
performing Selenium tests on a Flask application.

The file sets up a Selenium WebDriver instance using the Chrome WebDriver and provides
fixtures for managing the WebDriver during the test session.
"""

import sys

import os

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Add the parent directory of the current file to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope='session')
def browser():
    """
    Fixture for creating and managing the Selenium WebDriver instance.

    This fixture sets up the Chrome WebDriver with specified options and
    a provided ChromeDriver executable path.
    The WebDriver instance is created at the beginning of the test session
    and is available to all test functions.
    After the test session is complete, the WebDriver instance is closed.

    Returns:
        webdriver.Chrome: The configured Chrome WebDriver instance.
    """

    chrome_driver_path = '~/Chromedriver/chromedriver'

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(service=Service(
        chrome_driver_path), options=options)

    yield driver

    driver.quit()
