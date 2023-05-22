import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True 
    app.config['SERVICE_NAME'] = 'Mock Service'
    app.config['SERVICE_PHASE'] = 'Mock Phase'
    app.config['CONTACT_EMAIL'] = 'mock@example.com'
    app.config['DEPARTMENT_URL'] = 'mock.com'
    app.config['DEPARTMENT_NAME'] = 'Mock'
    yield app



def test_index_page(app):
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 302


def test_download_page(app):
    with app.test_client() as client:
        with app.app_context():
            app.jinja_env.globals['assetPath'] = '/static'
            response = client.get("/download", follow_redirects=True)
            assert response.status_code == 200
