import os

from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

if not AUTH_TOKEN:
    print("AUTH_TOKEN environment variable must be set")


# def get_sales(date: str, page: str) -> List[Dict[str, Any]]:
#     """
#     Get data from sales API for specified date.
#
#     :param page: data retrieve the data from
#     :param date: data retrieve the data from
#     :return: list of records
#     """
#     response = requests.get(
#         url=API_URL,
#         headers={"Authorization": f"{AUTH_TOKEN}"},
#         params={"date": date, "page": page},
#     )
#
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Error API call:", response.status_code)


def get_sales(date: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: Date to retrieve the data from
    :return: List of records
    """
    page = 1
    all_records = []

    while True:
        response = requests.get(
            url=API_URL,
            headers={"Authorization": f"{AUTH_TOKEN}"},
            params={"date": date, "page": str(page)},
        )

        if response.status_code == 200:
            records = response.json()
            all_records.extend(records)
            page += 1
        else:
            print("Error API call:", response.status_code)
            break

    return all_records
