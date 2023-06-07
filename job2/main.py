"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask import typing as flask_typing

from job2.dal import file_conversion

app = Flask(__name__)

load_dotenv()
BASE_DIR_PATH = os.getenv("BASE_DIR")


@app.route("/", methods=["POST"])
def main() -> flask_typing.ResponseReturnValue:
    """
    Proposed POST body in JSON:
    {
      "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09",
      "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09"
    }
    """
    input_data: dict = request.json
    raw_dir = input_data.get("raw_dir", "file_storage/raw/sales/2022-08-09")
    stg_dir = input_data.get("stg_dir", "file_storage/stg/sales/2022-08-09")

    raw_dir_path = os.path.join(BASE_DIR_PATH, raw_dir)
    stg_dir_path = os.path.join(BASE_DIR_PATH, stg_dir)
    json_file = os.path.join(raw_dir_path, "sales_2022-08-09_1.json")

    file_conversion.convert_json_to_avro(json_file=json_file, avro_path=stg_dir_path)

    if not raw_dir:
        return {
            "message": "raw_dir parameter missed",
        }, 400

    return {
        "message": "File transfer from json format to avro successfully.",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
