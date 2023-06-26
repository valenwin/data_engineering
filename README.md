# data_engineering

## Project Instructions

### Instructions

1. Clone the repository and navigate to the downloaded folder.
```	
git clone https://github.com/valenwin/data_engineering.git
cd data_engineering
```

1. Run Makefile script.
```	
make all
```

2. Connect Airflow docker container with Flask server using address of your local machine
- task_id='extract_data_from_api'
```	
create connection in Admin/Connections in Airflow with 
Connection Id=http_connection_8081,
Connection Type=HTTP,
Host=your local machine address,
Port=8081
```
- task_id='convert_to_avro'
```	
create connection in Admin/Connections in Airflow with 
Connection Id=http_connection_8082,
Connection Type=HTTP,
Host=your local machine address,
Port=8082
```

3. Before you start your Flask server, run it on your local machine address
```	
app.run(debug=True, host="your local machine address", port=8081)
```
```	
app.run(debug=True, host="your local machine address", port=8082)
```