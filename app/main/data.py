import requests
from flask import current_app


def get_remote_data(hostname, endpoint):
    """
        Queries the api endpoint provided and returns a
        data response in json format.

    Args:
        endpoint (str): an API get data address

    Returns:
        data (json): data response in json format
    """

    response = requests.get(hostname + endpoint)
    if response.status_code == 200:
        data = response.json()
        return data, 200
    else:
        current_app.logger.warning(
            "GET remote data call was unsuccessful with status code:"
            f" {response.status_code}."
        )
        return None, response.status_code
