import pytest
<<<<<<< HEAD

from app import create_app
from app.main.data import get_remote_data


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_remote_data_success(requests_mock, app):
    expected_data = {"key": "value"}
    expected_status_code = 200
=======
from werkzeug.exceptions import HTTPException

from app.main.data import get_response


def test_get_response_success(requests_mock, app_ctx):
    requests_mock.get("http://example.com/api/endpoint", text="Success")
>>>>>>> cb76ff51838d29ef83eac962e79f762e0ab9c007

    response = get_response("http://example.com", "/api/endpoint")

<<<<<<< HEAD
    with app.app_context():
        actual_data, actual_status_code = get_remote_data("http://example.com", "/api")

        assert actual_data == expected_data
        assert actual_status_code == expected_status_code


def test_get_remote_data_failure(requests_mock, app):
    expected_status_code = 404

    requests_mock.get("http://example.com/api", status_code=expected_status_code)

    with app.app_context():
        actual_data, actual_status_code = get_remote_data("http://example.com", "/api")
        assert actual_data is None
        assert actual_status_code == expected_status_code
=======
    assert response.status_code == 200
    assert response.text == "Success"


def test_get_response_failure(requests_mock, app_ctx):
    requests_mock.get("http://example.com/api/endpoint", status_code=404)

    with pytest.raises(HTTPException) as exc:
        get_response("http://example.com", "/api/endpoint")

    assert exc.value.code == 500
>>>>>>> cb76ff51838d29ef83eac962e79f762e0ab9c007
