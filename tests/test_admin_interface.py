from main import app

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
