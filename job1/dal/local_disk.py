import json
import os
from typing import List, Dict, Any


def save_to_disk(
    json_content: List[Dict[str, Any]], date: str, path: str
) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    file_name = f"sales_{date}.json"
    file_path = os.path.join(path, file_name)

    with open(file_path, "w") as file:
        json.dump(json_content, file, indent=4)
