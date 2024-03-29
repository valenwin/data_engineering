from job1.dal import local_disk, sales_api


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    # 1. get data from the API
    json_content = sales_api.get_sales(date=date)
    # 2. save data to disk
    local_disk.save_to_disk(
        json_content=json_content, date=date, path=raw_dir
    )
