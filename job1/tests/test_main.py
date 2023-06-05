from unittest import TestCase, mock

# NB: avoid relative imports when you will write your code
from .. import main


class MainFunctionTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        main.app.testing = True
        cls.client = main.app.test_client()

    @mock.patch("job1.main.save_sales_to_local_disk")
    def test_return_400_date_param_missed(self, get_sales_mock: mock.MagicMock):
        """
        Raise 400 HTTP code when no 'date' param
        """
        resp = self.client.post(
            "/",
            json={"page": "1", "raw_dir": "/foo/bar/"},
        )

        self.assertEqual(400, resp.status_code)

    @mock.patch("job1.main.save_sales_to_local_disk")
    def test_save_sales_to_local_disk_page_params_missed(
        self, save_sales_to_local_disk_mock: mock.MagicMock
    ):
        self.client.post(
            "/",
            json={"date": "1970-01-01", "raw_dir": "/foo/bar/"},
        )

        save_sales_to_local_disk_mock.assert_called_with(
            date="1970-01-01",
            page="1",
            raw_dir="/foo/bar/1970-01-01",
        )

    @mock.patch("job1.main.save_sales_to_local_disk")
    def test_save_sales_to_local_disk_raw_dir_params_missed(
        self, save_sales_to_local_disk_mock: mock.MagicMock
    ):
        self.client.post(
            "/",
            json={"date": "1970-01-01", "page": "1"},
        )

        save_sales_to_local_disk_mock.assert_called_with(
            date="1970-01-01",
            page="1",
            raw_dir="file_storage/raw/sales/1970-01-01",
        )

    @mock.patch("job1.main.save_sales_to_local_disk")
    def test_save_sales_to_local_disk(
        self, save_sales_to_local_disk_mock: mock.MagicMock
    ):
        """
        Test whether api.get_sales is called with proper params
        """
        fake_date = "1970-01-01"
        fake_page = "1"
        fake_raw_dir = "/foo/bar/"
        self.client.post(
            "/",
            json={
                "date": fake_date,
                "page": fake_page,
                "raw_dir": fake_raw_dir,
            },
        )

        save_sales_to_local_disk_mock.assert_called_with(
            date=fake_date,
            page=fake_page,
            raw_dir="/foo/bar/1970-01-01",
        )

    @mock.patch("job1.main.save_sales_to_local_disk")
    def test_return_201_when_all_is_ok(self, get_sales_mock: mock.MagicMock):
        resp = self.client.post(
            "/",
            json={
                "date": "1970-01-01",
                "page": "1",
                "raw_dir": "/foo/bar/",
            },
        )

        self.assertEqual(201, resp.status_code)
