from main import app


def test_get_page_if_user_is_not_admin():
    with app.test_client() as client:
        response = client.get('/admin/interface')
        assert response.status_code == 401
