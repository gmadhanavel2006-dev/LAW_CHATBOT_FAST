import json
import os

def load_latest_law_data(country: str):
    base_path = os.path.join("law_data", country)

    if not os.path.exists(base_path):
        raise FileNotFoundError("Country law data not available")

    versions = sorted(
        [f for f in os.listdir(base_path) if f.endswith(".json")]
    )

    if not versions:
        raise FileNotFoundError("No law versions found")

    latest_version = versions[-1]
    file_path = os.path.join(base_path, latest_version)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["laws"], data["meta"]