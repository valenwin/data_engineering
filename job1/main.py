"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
from flask import Flask, request
from flask import typing as flask_typing

from job1.dal import sales_api


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main() -> flask_typing.ResponseReturnValue:
    query_parameters = request.args
    date = query_parameters.get("date", "2022-08-09")
    page = query_parameters.get("page", "1")

    return sales_api.get_sales(date=date, page=page)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)
