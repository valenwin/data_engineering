from job2.dal import file_conversion


def save_sales_to_local_disk(json_file: str, avro_path: str, date: str) -> None:
    # 1. reads and parses a JSON file
    json_data = file_conversion.read_json_file(json_file=json_file)
    # 2. save data to disk
    file_conversion.convert_json_data_to_avro(
        json_data=json_data, avro_path=avro_path, date=date
    )
