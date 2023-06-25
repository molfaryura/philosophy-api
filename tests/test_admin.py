"""
Admin Login Page Selenium Tests

This module contains test cases for the Admin Login Page using Selenium WebDriver.
The Selenium WebDriver is used to interact with the web page
and perform actions such as form submission, URL navigation, and title verifying.
"""

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv


load_dotenv()


def fill_forms(browser, **kwargs):
    """
    Helper function to fill in form fields and submit the form in a Selenium browser instance.

    Args:
        browser (WebDriver): The Selenium WebDriver instance representing the browser.
        **kwargs: Keyword arguments containing form field values. Expected keys are:
            - 'username': Value for the username field.
            - 'password': Value for the password field.
            - 'secret_word': Value for the secret word field.

    Returns:
        None
    """

    username = browser.find_element(By.ID, 'typeUsernameX')
    username.click()
    username.send_keys(kwargs['username'])

    password = browser.find_element(By.ID, 'typePasswordX')
    password.click()
    password.send_keys(kwargs['password'])

    secret_word = browser.find_element(By.ID, 'typeSecretX')
    secret_word.click()
    secret_word.send_keys(kwargs['secret_word'])

    submit_button = browser.find_element(By.TAG_NAME, 'button')
    submit_button.submit()


def test_get_admin_page(browser):
    """
    Test case to verify accessing the admin page.

    It navigates to the admin page URL.
    The test asserts that the title of the page contains the word 'Login'.

    This test ensures that the admin page can be accessed successfully
    and the login form is present.
    """

    browser.get('http://localhost:5000/admin')

    assert 'Login' in browser.title


def test_login_admin_invalid_secret_word(browser):
    """
    Test case to verify login functionality with invalid secret word.

    The test enters an invalid secret word and invalid username and passowrd, and submits the form.
    It asserts that the user is redirected to the youtube video.
    """

    browser.get('http://localhost:5000/admin')

    fill_forms(browser, username='admin',
               password='admin', secret_word='admin')

    assert browser.current_url == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


def test_login_admin_valid_secret_word(browser):
    """
    Test case to verify login functionality with valid secret word and
    invalid username and password.

    The test enters an invalid username and password, submits the form,
    and waits for the error message to appear.
    It asserts that the displayed error message is 'Error : Invalid username or password'.
    """

    secret = os.environ.get('TEST_SECRET')

    browser.get('http://localhost:5000/admin')

    fill_forms(browser, username='admin', password='admin', secret_word=secret)

    wait = WebDriverWait(browser, 10)

    error_message_locator = (By.CLASS_NAME, 'error')
    error_message = wait.until(
        EC.presence_of_element_located(error_message_locator))

    assert error_message.text == 'Error : Invalid username or password'


def test_login_admin_valid_all(browser):
    """
    Test case to verify login functionality with valid credentials.
    It enters the valid admin credentials, submits the form,
    and asserts that the user is redirected to the admin interface page.
    Finally, it simulates logging out by visiting the '/logout' endpoint.
    """

    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    secret = os.environ.get('TEST_SECRET')

    browser.get('http://localhost:5000/admin')

    fill_forms(browser, username=admin_username,
               password=admin_password, secret_word=secret)

    redirected_url = browser.current_url
    expected_url = 'http://localhost:5000/admin/interface'

    assert redirected_url == expected_url

    browser.get('http://localhost:5000/logout')
