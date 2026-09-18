# data_manager.py
# Saves and loads records from a JSON file. OWNER: Pair C.

import json
import os

FILE = "reports.json"


def save(record):
    # add the new record to the file (make the file if it is not there yet)
    records = load()
    records.append(record)
    with open(FILE, "w") as f:
        json.dump(records, f, indent=2)


def load():
    # return all records, or [] if the file is missing or broken
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read", FILE, "- starting with an empty list.")
        return []


def query(filter_fn):
    # return only the records that match the given check
    return [record for record in load() if filter_fn(record)]
