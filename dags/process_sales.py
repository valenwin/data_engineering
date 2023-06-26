from datetime import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 8, 9),
    "catchup": True,
    "max_active_runs": 1,
}

dag = DAG(
    dag_id="process_sales",
    default_args=default_args,
    schedule_interval="0 1 * * *",
)

extract_data_from_api = SimpleHttpOperator(
    task_id="extract_data_from_api",
    method="POST",
    http_conn_id="http_connection_8081",  # add host of your local machine with port 8081 in Admin/Connections
    endpoint="/",
    headers={"Content-Type": "application/json"},
    data="""{
        "date": "2022-08-09",
        "raw_dir": "file_storage/raw/sales/"
    }""",
    response_check=lambda response: response.status_code == 201,
    dag=dag,
)

convert_to_avro = SimpleHttpOperator(
    task_id="convert_to_avro",
    method="POST",
    http_conn_id="http_connection_8082",  # add host of your local machine with port 8082 in Admin/Connections
    endpoint="/",
    headers={"Content-Type": "application/json"},
    data="""{
        "stg_dir": "file_storage/stg/sales/2022-08-09",
        "raw_dir": "file_storage/raw/sales/2022-08-09"
    }""",
    response_check=lambda response: response.status_code == 201,
    dag=dag,
)

# extract_data_from_api.params = {
#     'date': date,
#     'raw_dir': raw_dir,
# }

# convert_to_avro.extra_options = {
#     'raw_dir': raw_dir,
#     'stg_dir': stg_dir,
# }

extract_data_from_api >> convert_to_avro
