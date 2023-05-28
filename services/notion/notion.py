import requests
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": "Bearer " + os.getenv('NOTION_TOKEN'),
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"}


def get_pages(num_pages=None):
    """
    If not num_pages is None, get all pages
    """
    url = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DB_ID')}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    payload = {"page_size": page_size}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # Comment if we want to dump results to json file
    import json
    current_dir = os.path.dirname(os.path.abspath(__file__))  # returns directory for absolute path of file

    with open(os.path.join(current_dir, 'notion.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data['has_more'] and get_all:
        payload = {'page_size': page_size, 'start_cursor': data['next_cursor']}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data['results'])

    return results


def create_page(data: dict):
    create_url = 'https://api.notion.com/v1/pages'

    payload = {
        'parent': {
            'database_id': os.getenv('NOTION_DB_ID')
        },
        'properties': data
    }

    res = requests.post(create_url, headers=headers, json=payload)
    return res


def update_page(data: dict, page_id: str):
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {
        'properties': data
    }

    res = requests.patch(update_url, headers=headers, json=payload)
    return res

