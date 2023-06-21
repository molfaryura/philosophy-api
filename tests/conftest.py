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
from selenium.webdriver.common.by import By

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


@pytest.fixture(scope='session')
def authenticated_browser():
    """
    Pytest fixture that provides an authenticated Selenium WebDriver instance.

    The fixture sets up a Chrome WebDriver with specified options and launches
    the browser. It then authenticates the user by navigating to the admin login page,
    entering the admin username and password, and submitting the login form.

    The fixture yields the WebDriver instance for the test to use.

    After the test completes, it logs out the user by navigating to the logout page.

    Finally, it quits the WebDriver to clean up the resources.

    Returns:
        webdriver.Chrome: An authenticated Selenium WebDriver instance.
    """

    chrome_driver_path = '~/Chromedriver/chromedriver'

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(service=Service(
        chrome_driver_path), options=options)

    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password = os.environ.get('ADMIN_PASSWORD')

    driver.get('http://localhost:5000/admin')

    username = driver.find_element(By.ID, 'typeUsernameX')
    username.click()
    username.send_keys(admin_username)

    password = driver.find_element(By.ID, 'typePasswordX')
    password.click()
    password.send_keys(admin_password)

    submit_button = driver.find_element(By.TAG_NAME, 'button')
    submit_button.submit()

    yield driver

    driver.get('http://localhost:5000/logout')

    driver.quit()
