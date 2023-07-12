from datetime import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

dag = DAG(
    dag_id="process_sales",
    start_date=datetime(2022, 8, 9),
    catchup=True,
    max_active_runs=1,
    schedule_interval="0 1 * * *",
)

extract_data_from_api = SimpleHttpOperator(
    task_id="extract_data_from_api",
    method="POST",
    http_conn_id="http_connection_8081",
    endpoint="/",
    headers={"Content-Type": "application/json"},
    data="""
    {
        "date": "2022-08-09",
        "raw_dir": "dags/file_storage/raw/sales/"
    }
    """,
    response_check=lambda response: response.status_code == 201,
    dag=dag,
)

BUCKET_NAME = "salesbucketgetdata"
UPLOAD_FILE_PATH = "dags/file_storage/raw/sales/2022-08-09/sales_2022-08-09.json"

upload_file_to_gcs = LocalFilesystemToGCSOperator(
    task_id="upload_file_to_gcs",
    src=UPLOAD_FILE_PATH,
    dst="src1/sales/v1/year=2022/month=08/day=09/",
    bucket=BUCKET_NAME,
)

success_task = PythonOperator(
    task_id="success",
    python_callable=lambda: print("Success"),
)

extract_data_from_api >> upload_file_to_gcs >> success_task
