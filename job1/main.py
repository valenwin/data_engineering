"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask import typing as flask_typing

from job1.bll.sales_api import save_sales_to_local_disk
from validation import date_validation

app = Flask(__name__)

load_dotenv()


@app.route("/", methods=["POST"])
def main() -> flask_typing.ResponseReturnValue:
    """
    Controller that accepts command via HTTP and
    trigger business logic layer

    Proposed POST body in JSON:
    {
      "date": "2022-08-09",
      "raw_dir": "file_storage/raw/sales/"
    }
    """
    input_data: dict = request.json
    date: str = input_data.get("date")
    dir_path: str = input_data.get("raw_dir", "file_storage/raw/sales/")

    base_dir_path = os.getenv("BASE_DIR")
    raw_dir_path = os.path.join(base_dir_path, dir_path, date)

    if not date:
        return {
            "message": "date parameter missed",
        }, 400

    if not date_validation.validate_date_format(date, "%Y-%m-%d"):
        return {
            "message": "Invalid date format",
        }, 400

    save_sales_to_local_disk(date=date, raw_dir=raw_dir_path)

    return {
        "message": "Data retrieved successfully from API",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)
