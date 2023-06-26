import unittest
import os
import json
import fastavro

from job2.dal.file_conversion import convert_json_to_avro


class ConvertJsonToAvroTestCase(unittest.TestCase):
    def setUp(self):
        self.test_json_file = 'test.json'
        self.test_avro_path = 'test_avro'
        self.test_date = '2023-06-08'

        # Create a temporary test JSON file
        self.create_test_json_file()

    def tearDown(self):
        # Remove the temporary test JSON file
        os.remove(self.test_json_file)

        # Remove the generated test Avro file
        avro_file_path = os.path.join(self.test_avro_path, f"sales_{self.test_date}.avro")
        os.remove(avro_file_path)

    def create_test_json_file(self):
        json_data = [
            {
                "client": "John Doe",
                "purchase_date": "2023-06-01",
                "product": "Item A",
                "price": 10
            },
            {
                "client": "Jane Smith",
                "purchase_date": "2023-06-02",
                "product": "Item B",
                "price": 20
            }
        ]

        with open(self.test_json_file, 'w') as f:
            json.dump(json_data, f)

    def test_convert_json_to_avro(self):
        # Call the function with the test file and paths
        convert_json_to_avro(self.test_json_file, self.test_avro_path, self.test_date)

        # Check if the Avro file has been created
        avro_file_path = os.path.join(self.test_avro_path, f"sales_{self.test_date}.avro")
        self.assertTrue(os.path.exists(avro_file_path))

        # Load the Avro file and validate its contents
        with open(avro_file_path, 'rb') as f:
            avro_data = list(fastavro.reader(f))

        expected_avro_data = [
            {
                "client": "John Doe",
                "purchase_date": "2023-06-01",
                "product": "Item A",
                "price": 10
            },
            {
                "client": "Jane Smith",
                "purchase_date": "2023-06-02",
                "product": "Item B",
                "price": 20
            }
        ]

        self.assertEqual(avro_data, expected_avro_data)
