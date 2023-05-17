import pytest

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

    requests_mock.get(
        "http://example.com/api", json=expected_data, status_code=expected_status_code
    )

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
