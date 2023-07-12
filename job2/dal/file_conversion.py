import json
import os
from typing import Dict

import fastavro


def read_json_file(json_file: str) -> Dict:
    """Reads and parses a JSON file.

    Args:
        json_file (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.

    Raises:
        FileNotFoundError: If the JSON file does not exist.

    """
    if not os.path.exists(json_file):
        raise FileNotFoundError("JSON file does not exist")

    with open(json_file, "r") as f:
        json_data = json.load(f)

    return json_data


def convert_json_data_to_avro(json_data: Dict, avro_path: str, date: str) -> None:
    """Converts a dictionary to Avro format and saves it to a file.

    Args:
        json_data (dict): JSON data to convert to Avro.
        avro_path (str): Path to the directory where the Avro file will be saved.
        date (str): Date string used in the Avro file name.

    Returns:
        None: The function does not return any value.

    """
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
