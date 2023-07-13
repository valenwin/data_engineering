import unittest
from dags.process_sales import dag


class MyDagTestCase(unittest.TestCase):

    def test_extract_data_from_api(self):
        dag.clear()

        task = dag.get_task("extract_data_from_api")

        expected_data = '''
        {
            "date": "2023-07-13",
            "raw_dir": "dags/file_storage/raw/sales/"
        }
        '''
        self.assertEqual(task.data.strip(), expected_data.strip())

        self.assertEqual(task.headers["Content-Type"], "application/json")
        self.assertEqual(task.method, "POST")

    def test_upload_file_to_gcs(self):
        dag.clear()

        task = dag.get_task("upload_file_to_gcs")

        expected_upload_path = "dags/file_storage/raw/sales/2023-07-13/sales_2023-07-13.json"
        self.assertEqual(task.src, expected_upload_path)

        expected_destination_path = "src1/sales/v1/year=2023/month=07/day=13/"
        self.assertEqual(task.dst, expected_destination_path)

        self.assertEqual(task.bucket, "salesbucketgetdata")


if __name__ == '__main__':
    unittest.main()
