import os
from unittest import TestCase, mock
from job1.dal.sales_api import get_sales


class GetSalesTestCase(TestCase):
    def setUp(self) -> None:
        self.auth_token = os.getenv("API_AUTH_TOKEN")

    @mock.patch("job1.dal.sales_api.requests.get")
    def test_get_sales(self, mock_get):
        date = "2022-08-09"
        page = "1"

        # Prepare the mock response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "client": "Jane Doe",
                "purchase_date": "1970-01-01",
                "product": "Laptop",
                "price": 1000,
            },
            {
                "client": "John Snow",
                "purchase_date": "2022-08-09",
                "product": "Laptop",
                "price": 2000,
            },
        ]
        mock_get.return_value = mock_response

        # Call the function
        result = get_sales(date, page)

        # Verify results
        mock_get.assert_called_once_with(
            url="https://fake-api-vycpfa6oca-uc.a.run.app/sales",
            headers={"Authorization": self.auth_token},
            params={"date": date, "page": page},
        )
        self.assertEqual(
            result,
            [
                {
                    "client": "Jane Doe",
                    "purchase_date": "1970-01-01",
                    "product": "Laptop",
                    "price": 1000,
                },
                {
                    "client": "John Snow",
                    "purchase_date": "2022-08-09",
                    "product": "Laptop",
                    "price": 2000,
                },
            ],
        )
