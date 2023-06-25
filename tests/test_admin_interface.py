"""
Admin Interface page tests

This module contains the test cases for the Flask application using Selenium and database queries.

The test cases cover different scenarios to ensure the proper functionality of the application.
"""


import random

import string

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from main import app

from models import Chapter, Book, Note


def test_get_page_if_user_is_not_admin():
    """
    Test case to verify that accessing the admin interface page without authentication
    returns a 401 status code.

    It uses the Flask test client to simulate a GET request to the '/admin/interface' endpoint.
    The test asserts that the response status code is 401, indicating unauthorized access.
    """

    with app.test_client() as client:
        response = client.get('/admin/interface')
        assert response.status_code == 401

def test_add_new_book(authenticated_browser):
    """
    Test case to verify adding a new book through the admin interface.

    It navigates to the admin interface, fills in the form with random data, submits the form,
    and asserts that a success message is displayed.

    This test ensures that the book form submission works correctly.
    """
    random_string = ''.join(random.choices(string.ascii_letters, k=6))

    authenticated_browser.get('http://localhost:5000/admin/interface')

    author = authenticated_browser.find_element(By.ID, 'author')
    author.click()
    author.send_keys(random_string)

    book = authenticated_browser.find_element(By.ID, 'book')
    book.click()
    book.send_keys(random_string)

    chapter = authenticated_browser.find_element(By.ID, 'chapter')
    chapter.click()
    chapter.send_keys(random_string)

    bio = authenticated_browser.find_element(By.ID, 'authorBio')
    bio.click()
    bio.send_keys(random_string)

    content = authenticated_browser.find_element(By.ID, 'content')
    content.click()
    content.send_keys(random_string)

    submit_button = authenticated_browser.find_element(By.ID, 'colorButton')
    submit_button.submit()

    wait = WebDriverWait(authenticated_browser, 2)

    success_message_locator = (By.CLASS_NAME, 'success')
    success_message = wait.until(
        EC.presence_of_element_located(success_message_locator))

    assert success_message.text == 'Form submitted successfully'

def test_book_in_the_database(authenticated_browser):
    """
    Test case to verify that a book and chapter are successfully added to the database
    after submitting the book form.

    It navigates to the admin interface, fills in the form with test data, submits the form,
    and then checks the database for the presence of the book and chapter.

    This test ensures that the book and chapter are properly stored in the database.
    """

    authenticated_browser.get('http://localhost:5000/admin/interface')

    test_data = 'TESTING'

    author = authenticated_browser.find_element(By.ID, 'author')
    author.click()
    author.send_keys(test_data)

    book = authenticated_browser.find_element(By.ID, 'book')
    book.click()
    book.send_keys(test_data)

    chapter = authenticated_browser.find_element(By.ID, 'chapter')
    chapter.click()
    chapter.send_keys(test_data)

    bio = authenticated_browser.find_element(By.ID, 'authorBio')
    bio.click()
    bio.send_keys(test_data)

    content = authenticated_browser.find_element(By.ID, 'content')
    content.click()
    content.send_keys(test_data)

    submit_button = authenticated_browser.find_element(By.ID, 'colorButton')
    submit_button.submit()

    with app.app_context():
        book = Book.query.filter_by(title=test_data).first()

        chapter = Chapter.query.filter_by(chapter_name=test_data).first()

        if book is None or chapter is None:
            pytest.fail(
                f"Book or chapter not found in the database: {test_data}")

        chapters_query = Note.query.filter_by(
            book_id=book.id, chapter_id=chapter.id, content=test_data
        ).first()

    assert chapters_query is not None
