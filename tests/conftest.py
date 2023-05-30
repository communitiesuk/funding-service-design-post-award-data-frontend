import pytest
from flask.testing import FlaskClient

import config
from app import create_app


@pytest.fixture()
def mocked_auth(monkeypatch):
    def access_token(return_app):
        return {"accountId": "test-user"}

    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        access_token,
    )


@pytest.fixture()
def flask_test_client(mocked_auth) -> FlaskClient:
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.

    NOTE: Auth is mocked here because it's required for all routes.

    :return: A flask test client.
    """
    with create_app(config.Config).test_client() as test_client:
        yield test_client


@pytest.fixture
def app_ctx(flask_test_client):
    """
    Pushes an application context to a test.

    :return: a test application context.
    """
    with flask_test_client.application.app_context():
        yield