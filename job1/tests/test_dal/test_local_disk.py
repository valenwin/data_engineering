import json
import os
from unittest import TestCase

from job1.dal.local_disk import save_to_disk


class SaveToDiskTestCase(TestCase):
    def test_save_to_disk(self):
        # Prepare the test data
        json_content = [
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
        date = "2023-06-05"
        page = "1"
        path = "./test_data"

        # Call the function
        save_to_disk(json_content, date, page, path)

        # Verify that the file has been created
        file_path = f"{path}/sales_{date}_{page}.json"
        self.assertTrue(os.path.exists(file_path))

        # Verify the content of the file
        with open(file_path, "r") as file:
            loaded_json = json.load(file)
        self.assertEqual(loaded_json, json_content)

        # Clean up the test file
        os.remove(file_path)
        os.rmdir(path)
