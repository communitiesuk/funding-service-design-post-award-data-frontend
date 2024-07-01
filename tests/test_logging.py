import pytest


@pytest.fixture
def mock_get_response_basic_download(flask_test_client, mocker):
    mocker.patch("app.main.routes.process_async_download", return_value=True)


def test_download_logging(flask_test_client, caplog, mock_get_response_basic_download):
    flask_test_client.post("/download", data={"file_format": "xlsx"})
    log_line = [record for record in caplog.records if hasattr(record, "request_type")]
    assert len(log_line) == 1
    assert log_line[0].request_type == "download"
    assert log_line[0].user_id == "test-user"
    assert log_line[0].query_params == {"file_format": "xlsx", "email_address": None}
