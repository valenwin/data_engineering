import os

from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

if not AUTH_TOKEN:
    print("AUTH_TOKEN environment variable must be set")


def get_sales(date: str, page: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param page: data retrieve the data from
    :param date: data retrieve the data from
    :return: list of records
    """
    response = requests.get(
        url=API_URL,
        headers={'Authorization': f'{AUTH_TOKEN}'},
        params={'date': date, 'page': page}
    )

    data = response.json()

    return data