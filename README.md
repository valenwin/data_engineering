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
2. Run AirFlow locally
```	
docker compose up
```
3. Add AUTH_TOKEN value to Admin/Variables

4. Connect Airflow docker container with Flask server using address of your local machine

- task_id='extract_data_from_api'
```	
create connection in Admin/Connections in Airflow with 
Connection Id=http_connection_8081,
Connection Type=HTTP,
Host=your local machine address,
Port=8081
```
```	
Увійдіть до веб-інтерфейсу Apache Airflow.
В бічному меню виберіть "Admin" і потім "Variables".
Натисніть кнопку "Create" або "Add" для створення нової змінної.
У полі "Key" введіть назву змінної, наприклад, "target_date".
У полі "Val" введіть значення дати, яке ви хочете зберегти. Наприклад, "2022-08-09".
Натисніть кнопку "Save" або "Add" для збереження змінної.
```

- task_id='upload_file_to_gcs'
```	
create connection in Admin/Connections in Airflow with 
Connection Id=google_cloud_default,
Connection Type=Google Cloud,
Project ID=de2023-valentyna-lysenok,
Keyfile JSON=...->>>>>>>>>>>>>>>>>>

Увійдіть до консолі Google Cloud: https://console.cloud.google.com.
Виберіть проект, пов'язаний з вашими бакетами Google Cloud.
У бічному меню виберіть "IAM і адміністрування" (IAM & Admin).
Виберіть "Сервісні облікові записи" (Service Accounts).
Знайдіть службовий обліковий запис, пов'язаний з google_cloud_default або створіть новий, якщо потрібно.
У розділі "Ключі" (Keys) облікового запису виберіть "Додати ключ" (Add Key) та оберіть "Створити ключ" (Create Key).
Виберіть формат ключа JSON та натисніть "Створити" (Create).
Завантажте отриманий ключ доступу у форматі JSON.
```

Before you start your Flask server, run it on your local machine address
```	
app.run(debug=True, host="your local machine address", port=8081)
```
