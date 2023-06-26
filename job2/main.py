"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask import typing as flask_typing

from job2.bll import save_file
from validation import date_validation

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
    raw_dir: str = input_data.get("raw_dir")
    stg_dir: str = input_data.get("stg_dir")

    if not raw_dir or not stg_dir:
        return {
            "message": "raw_dir or stg_dir parameter is missing",
        }, 400

    raw_date = raw_dir.split("/")[-1]
    stg_date = stg_dir.split("/")[-1]

    if not date_validation.validate_date_format(raw_date, "%Y-%m-%d"):
        return {
            "message": "Invalid date format for raw_dir",
        }, 400

    if not date_validation.validate_date_format(stg_date, "%Y-%m-%d"):
        return {
            "message": "Invalid date format for stg_dir",
        }, 400

    if raw_date != stg_date:
        return {
            "message": "raw_dir and stg_dir dates must be the same",
        }, 400

    raw_dir_path = os.path.join(
        BASE_DIR_PATH,
        raw_dir or "file_storage/raw/sales/2022-08-09"
    )
    stg_dir_path = os.path.join(
        BASE_DIR_PATH,
        stg_dir or "file_storage/stg/sales/2022-08-09"
    )
    json_file = os.path.join(raw_dir_path, f"sales_{raw_date}.json")

    save_file.save_sales_to_local_disk(
        json_file=json_file,
        avro_path=stg_dir_path,
        date=raw_date
    )

    return {
        "message": "File transfer from json format to avro successfully.",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
