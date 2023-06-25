"""
API tests

This module contains pytest test cases for the application.

It includes test cases for retrieving books and notes from the application's API endpoints.

"""

import logging

from app import app


def test_get_all_books():
    """
    Test case to verify retrieving all books.

    It sends a GET request to the '/get/all_books' endpoint.
    The test asserts that the response contains a non-empty 'books' field.

    This test ensures that all books can be retrieved successfully.
    """

    with app.test_client() as client:
        response = client.get('/get/all_books')

        logging.info(response.json['books'][0])

        assert response.json['books'] is not None


def test_get_all_books_by_correct_author():
    """
    Test case to verify retrieving all books by a specific author.

    It sends a GET request with a query parameter specifying the author's name.
    The test asserts that the response contains the expected author name as the first element.

    This test ensures that books by a correct author can be retrieved successfully.
    """

    with app.test_client() as client:
        author_name = 'Сенека'
        response = client.get(f'/get/all_books?author={author_name}')

        logging.info(response.json)

        assert next(iter(response.json)) == author_name


def test_get_all_books_by_wrong_author():
    """
    Test case to verify retrieving books by a wrong author.

    It sends a GET request with a query parameter specifying a non-existent author's name.
    The test asserts that the response status code is 404, indicating not found.

    This test ensures that attempting to retrieve books by a wrong author results in failure.
    """

    with app.test_client() as client:
        author_name = 'WrongAuthorName'
        response = client.get(f'/get/all_books?author={author_name}')

        logging.info(response.json)

        assert response.status_code == 404


def test_get_all_notes():
    """
    Test case to verify retrieving all notes.

    It sends a GET request to the '/get/notes' endpoint.
    The test asserts that the response status code is 200, indicating success.

    This test ensures that all notes can be retrieved successfully.
    """

    with app.test_client() as client:
        response = client.get('/get/notes')

        logging.info(response.json)

        assert response.status_code == 200


def test_get_notes_by_book():
    """
    Test case to verify retrieving notes by book.

    It sends a GET request with a query parameter specifying the book's name.
    The test asserts that the response contains the expected book name as the first element.

    This test ensures that notes by a specific book can be retrieved successfully.
    """

    with app.test_client() as client:
        book_name = 'test'
        response = client.get(f'/get/notes?book={book_name}')

        logging.info(response.json)

        assert next(iter(response.json)) == book_name


def test_get_authors():
    """
    Test case to verify retrieving all authors.

    It sends a GET request to the 'get/authors' endpoint.
    The test asserts that the response status code is 200, indicating success.

    This test ensures that all authors can be retrieved successfully.
    """

    with app.test_client() as client:
        response = client.get('/get/authors')

        logging.info(response.json)

        assert response.status_code == 200
