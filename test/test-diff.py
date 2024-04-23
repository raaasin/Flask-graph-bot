
import requests
import csv
import json
from itertools import chain
from collections.abc import Iterable
from dotenv import load_dotenv
import os
load_dotenv()

def flatten_json(data, parent_key='', sep='_'):
    items = []
    for k, v in data.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            items.extend(flatten_json({str(i): item for i, item in enumerate(v)}, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def write_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def convert_to_csv(json_data):
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    if isinstance(data, dict):
        flattened_data = flatten_json(data)
        write_csv([flattened_data])
    elif isinstance(data, list):
        flattened_data = [flatten_json(item) for item in data]
        write_csv(flattened_data)
    else:
        print("Unsupported data format.")

link = "https://www.bbc.com/news/world-middle-east-68831408"
url = "https://api.diffbot.com/v3/analyze?url=" + link + "&token=" + str(os.getenv("DIFFBOT_API_KEY"))
headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
json_response = response.json()

convert_to_csv(json_response)

