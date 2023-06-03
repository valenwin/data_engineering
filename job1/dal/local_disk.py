import json
import os
from typing import List, Dict, Any


def save_to_disk(json_content: List[Dict[str, Any]], path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    file_date = path.split('/')[-1]
    file_path = f"{path}/{file_date}.json"

    with open(file_path, "w") as file:
        json.dump(json_content, file)
