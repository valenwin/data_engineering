from datetime import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

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
        "date": "{{ execution_date.strftime('%Y-%m-%d') }}",
        "raw_dir": "file_storage/raw/sales/year={{ execution_date.year }}/month={{ execution_date.month }}/day={{ execution_date.day }}/"
    }
    """,
    response_check=lambda response: response.status_code == 201,
    dag=dag,
)

success_task = PythonOperator(
    task_id="success",
    python_callable=lambda: print("Success"),
)

extract_data_from_api >> success_task
