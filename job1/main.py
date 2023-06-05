"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask import typing as flask_typing

from job1.bll.sales_api import save_sales_to_local_disk

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
      "page": "1",
      "raw_dir": "file_storage/raw/sales/"
    }
    """
    input_data: dict = request.json
    date = input_data.get("date")
    page = input_data.get("page", "1")
    dir_path = input_data.get("raw_dir", "file_storage/raw/sales/")
    raw_dir_path = f"{dir_path}{date}"

    if not date:
        return {
            "message": "date parameter missed",
        }, 400

    save_sales_to_local_disk(date=date, page=page, raw_dir=raw_dir_path)

    return {
        "message": "Data retrieved successfully from API",
    }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)
