import unittest
from unittest.mock import patch, MagicMock

from airflow.models import DagBag

from dags.process_sales import get_sales, save_to_disk, API_URL


class TestDag(unittest.TestCase):
    def setUp(self):
        self.dagbag = DagBag(dag_folder="dags")

    def test_dag_load(self):
        dag_id = "get_api_sales_result"
        try:
            dag = self.dagbag.get_dag(dag_id)
            self.assertIsNotNone(dag)
        except Exception as e:
            print(f"Error loading DAG '{dag_id}': {str(e)}")

    @patch('requests.get')
    @patch('airflow.models.Variable.get')
    def test_get_sales(self, mock_auth, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'client': 'John', 'purchase_date': '2022-08-09', 'product': 'Item1', 'price': 10}]
        mock_auth.return_value = "MOCKED_AUTH_TOKEN"
        mock_get.return_value = mock_response

        # Call the function and pass a mock TaskInstance
        mock_ti = MagicMock()
        result = get_sales('2022-08-09', ti=mock_ti)

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['client'], 'John')
        self.assertEqual(result[0]['purchase_date'], '2022-08-09')
        self.assertEqual(result[0]['product'], 'Item1')
        self.assertEqual(result[0]['price'], 10)
        mock_get.assert_called_with(
            url=API_URL, headers={'Authorization': 'MOCKED_AUTH_TOKEN'},
            params={'date': '2022-08-09', 'page': '1'}
        )
        self.assertEqual(mock_get.call_count, 1)
        mock_ti.xcom_push.assert_called_once_with(key='json_data', value=[
            {'client': 'John', 'purchase_date': '2022-08-09', 'product': 'Item1', 'price': 10}])

    def test_save_to_disk(self):
        # Mock TaskInstance and its xcom_pull method
        mock_ti = MagicMock()
        mock_ti.xcom_pull.return_value = [
            {'client': 'John', 'purchase_date': '2022-08-09', 'product': 'Item1', 'price': 10}]

        # Call the function
        save_to_disk(date='2022-08-09', ti=mock_ti)

        # Assertions
        mock_ti.xcom_pull.assert_called_once_with(key='json_data')
        mock_ti.xcom_push.assert_not_called()  # Ensure that xcom_push is not called in this function


if __name__ == '__main__':
    unittest.main()
