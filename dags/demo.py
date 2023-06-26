from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "catchup": True,
}

dag = DAG(
    dag_id="test_get_api_sales_result",
    description="Pipeline for processing sales data",
    default_args=default_args,
    schedule_interval="0 1 * * *",  # Every day at 1 AM UTC
    max_active_runs=1,
)

start_date = datetime(2022, 8, 9)
end_date = datetime(2022, 8, 11)


def get_sales(date: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: Date to retrieve the data from
    :return: List of records
    """
    page = 1
    all_records = []

    while True:
        print(f"Token: {Variable.get('AUTH_TOKEN')}")
        auth_token = Variable.get("AUTH_TOKEN")

        if not auth_token:
            print("AUTH_TOKEN environment variable must be set")

        response = requests.get(
            url=API_URL,
            headers={"Authorization": auth_token},
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


success_task = EmptyOperator(
    task_id="success",
    dag=dag,
)

for date in [
    start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)
]:
    extract_data_task = PythonOperator(
        task_id=f"extract_data_from_api_{date.strftime('%Y-%m-%d')}",
        python_callable=get_sales,
        op_kwargs={"date": date.strftime("%Y-%m-%d")},
        provide_context=True,
        dag=dag,
    )

    extract_data_task >> success_task
