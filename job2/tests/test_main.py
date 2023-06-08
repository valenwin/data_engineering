from unittest import TestCase, mock

from ..main import app


class ControllerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()

    @mock.patch('job2.dal.file_conversion.convert_json_to_avro')
    def test_main_success(self, mock_convert_json_to_avro):
        # Prepare test data
        data = {
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
            "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
        }
        expected_message = "File transfer from json format to avro successfully."
        expected_status_code = 201

        # Perform the HTTP POST request
        response = self.client.post('/', json=data)

        # Verify the response
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json["message"], expected_message)

        # Verify the function calls
        mock_convert_json_to_avro.assert_called_once_with(
            json_file='/path/to/my_dir/raw/sales/2022-08-09/sales_2022-08-09.json',
            avro_path='/path/to/my_dir/stg/sales/2022-08-09',
            date='2022-08-09'
        )

    def test_main_missing_dir_parameters(self):
        # Prepare test data
        data = {
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
            # Missing "stg_dir" parameter
        }
        expected_message = "raw_dir or stg_dir parameter is missing"
        expected_status_code = 400

        # Perform the HTTP POST request
        response = self.client.post('/', json=data)

        # Verify the response
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json["message"], expected_message)

    def test_main_invalid_date_format(self):
        # Prepare test data
        data = {
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
            "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
        }
        expected_message = "Invalid date format for raw_dir"
        expected_status_code = 400

        with mock.patch('job2.dal.date_validation.validate_date_format') as mock_validate_date_format:
            mock_validate_date_format.return_value = False

            # Perform the HTTP POST request
            response = self.client.post('/', json=data)

            # Verify the response
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(response.json["message"], expected_message)

    def test_main_different_dates(self):
        # Prepare test data
        data = {
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
            "stg_dir": "/path/to/my_dir/stg/sales/2022-08-10"  # Different date from raw_dir
        }
        expected_message = "raw_dir and stg_dir dates must be the same"
        expected_status_code = 400

        # Perform the HTTP POST request
        response = self.client.post('/', json=data)

        # Verify the response
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json["message"], expected_message)
