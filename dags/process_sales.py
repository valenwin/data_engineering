import json
import os
from typing import List, Dict, Any
from datetime import datetime
import requests
import fastavro
import pandas as pd

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

start_date = datetime(2022, 8, 9)
end_date = datetime(2022, 8, 11)
date_range = pd.date_range(start=start_date, end=end_date, freq="D")
raw_dir = "file_storage/raw/sales/"
API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/sales"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "catchup": True,
}

with DAG(
        dag_id="get_api_sales_result",
        description="Pipeline for processing sales data",
        default_args=default_args,
        schedule_interval="0 1 * * *",  # Every day at 1 AM UTC
        max_active_runs=1,
) as dag:
    def get_sales(date: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Get data from sales API for specified date.

        :param date: Date to retrieve the data from
        :return: List of records
        """
        page = 1
        all_records = []
        task_instance = kwargs["ti"]
        auth_token = Variable.get("AUTH_TOKEN")

        if not auth_token:
            print("AUTH_TOKEN environment variable must be set")

        while True:
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

        task_instance.xcom_push(key="json_data", value=all_records)
        return all_records


    def save_to_disk(date: str, **kwargs) -> None:
        base_dir_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_dir_path, raw_dir, date)
        print(path)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        task_instance = kwargs["ti"]
        json_content = task_instance.xcom_pull(key="json_data")

        file_name = f"sales_{date}.json"
        file_path = os.path.join(path, file_name)

        with open(file_path, "w") as file:
            json.dump(json_content, file, indent=4)


    success_task = EmptyOperator(
        task_id="success",
        dag=dag,
    )

    def read_json_file(json_file: str) -> Dict:
        if not os.path.exists(json_file):
            raise FileNotFoundError("JSON file does not exist")

        with open(json_file, "r") as f:
            json_data = json.load(f)

        return json_data


    def convert_json_data_to_avro(
            json_data: Dict, avro_path: str, date: str
    ) -> None:
        os.makedirs(avro_path, exist_ok=True)

        avro_file_name = f"sales_{date}.avro"
        avro_file_path = os.path.join(avro_path, avro_file_name)

        # Define the Avro schema
        schema = {
            "type": "record",
            "name": "Purchase",
            "fields": [
                {"name": "client", "type": "string"},
                {"name": "purchase_date", "type": "string"},
                {"name": "product", "type": "string"},
                {"name": "price", "type": "int"}
            ]
        }

        # Write JSON data to Avro file
        with open(avro_file_path, "wb") as f:
            fastavro.writer(f, schema, json_data)

        print(f"Dictionary converted to Avro: {avro_file_path}")


    def save_sales_to_local_disk(json_file: str, avro_path: str, date: str) -> None:
        # 1. reads and parses a JSON file
        json_data = read_json_file(json_file=json_file)
        # 2. save data to disk
        convert_json_data_to_avro(
            json_data=json_data, avro_path=avro_path, date=date
        )


    def transfer_data_to_avro(raw_date: str):
        base_dir_path: str = os.path.abspath(os.path.dirname(__file__))
        raw_dir: str = f"file_storage/raw/sales/{raw_date}"
        stg_dir: str = f"file_storage/stg/sales/{raw_date}"

        raw_dir_path = os.path.join(
            base_dir_path,
            raw_dir or f"file_storage/raw/sales/{raw_date}"
        )
        stg_dir_path = os.path.join(
            base_dir_path,
            stg_dir or f"file_storage/stg/sales/{raw_date}"
        )
        json_file = os.path.join(raw_dir_path, f"sales_{raw_date}.json")

        save_sales_to_local_disk(
            json_file=json_file,
            avro_path=stg_dir_path,
            date=raw_date
        )

        return {
            "message": "File transfer from json format to avro successfully.",
        }, 201


    for date in date_range:
        extract_data_task = PythonOperator(
            task_id=f"extract_data_from_api_{date.strftime('%Y-%m-%d')}",
            python_callable=get_sales,
            op_kwargs={"date": date.strftime("%Y-%m-%d")},
            provide_context=True,
        )

        save_data = PythonOperator(
            task_id=f"save_data_from_api_{date.strftime('%Y-%m-%d')}",
            python_callable=save_to_disk,
            op_kwargs={"date": date.strftime("%Y-%m-%d")},
            provide_context=True,
        )

        convert_to_avro = PythonOperator(
            task_id=f"convert_to_avro_{date.strftime('%Y-%m-%d')}",
            python_callable=transfer_data_to_avro,
            op_kwargs={"raw_date": date.strftime("%Y-%m-%d")},
            provide_context=True,
        )

        extract_data_task >> success_task >> save_data >> convert_to_avro
