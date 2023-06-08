import json
import os

import fastavro


def convert_json_to_avro(json_file, avro_path, date):
    if not os.path.exists(json_file):
        print("JSON file does not exist")
        return

    with open(json_file, 'r') as f:
        json_data = json.load(f)

    if not os.path.exists(avro_path):
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
    with open(avro_file_path, 'wb') as f:
        fastavro.writer(f, schema, json_data)

    print(f"JSON file converted to Avro: {avro_file_path}")
