from datetime import datetime

from app.main.download_data import get_returns


# January-March is Q1, April-June is Q2, July-September is Q3, and October-December is Q4
def test_return_periods(requests_mock, flask_test_client):
    requests_mock.get(
        "http://data-store/returns",
        json=[
            {"end_date": "2023-02-01T00:00:00Z", "start_date": "2023-02-12T00:00:00Z"}
        ],
    )

    output = get_returns()
    assert output["quarter"] == [1, 2, 3, 4]
    assert output["year"] == ["2022/2023"]

    requests_mock.get(
        "http://data-store/returns",
        json=[
            {"end_date": "2021-07-01T00:00:00Z", "start_date": "2019-10-21T00:00:00Z"}
        ],
    )

    output_2 = get_returns()

    assert output_2["quarter"] == [3, 4]
    assert output_2["year"] == ["2019/2020", "2020/2021", "2021/2022"]

    requests_mock.get(
        "http://data-store/returns",
        json=[
            {"end_date": "2023-04-15T00:00:00Z", "start_date": "2022-09-05T00:00:00Z"}
        ],
    )

    output_2 = get_returns()

    assert output_2["quarter"] == [2, 3, 4]
    assert output_2["year"] == ["2022/2023", "2023/2024"]
