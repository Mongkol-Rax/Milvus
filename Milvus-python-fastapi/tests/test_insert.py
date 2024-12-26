"""
Test Call API Insert Data
"""

from datetime import datetime
import random
import uuid
import requests
from app.utilitys.embed_text import Embeded # pylint: disable=import-error,no-name-in-module

def insert_record_by_data_frame():
    """
    Test call api and insert by data_frame # pylint: skip-file
    """

    start_time = datetime.now()

    # URL ของ API ที่รันด้วย Uvicorn
    api_url = "http://127.0.0.1:8000/milvus/insert/by_data_frame"

    random_int = random.randint(1, 100)
    text_data = f"text to embed data : {random_int}"
    embed_instance = Embeded()

    # Payload ของข้อมูลที่จะส่ง
    payload = {
        "collection_name": "example_collection1",
        "id": str(uuid.uuid4()),
        "randomint": random_int,
        "embedding": embed_instance.embeded_text_by_lm(f"text to embed data : {random_int}"), 
        "text": text_data
    }

    # ส่งคำขอ POST ไปยัง API
    try:
        # Post
        response = requests.post(api_url, json=payload, timeout=15)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # ตรวจสอบสถานะของคำขอ
        if response.status_code == 200:
            print(f"Insert successful time: {processing_time}s, response: {response.json()}")
        else:
            print(f"Failed to insert status code: {response.status_code}, response text: {response.text}") # pylint: disable=C0301:line-too-long
    except Exception as e: # pylint: disable=w0718
        print("Error occurred:", str(e))

def insert_record_by_list_dict():
    """
    Test call api and insert by list dictionary
    """

    start_time = datetime.now()

    # URL ของ API ที่รันด้วย Uvicorn
    api_url = "http://127.0.0.1:8000/milvus/insert/by_list_dict"

    random_int = random.randint(1, 100)
    text_data = f"text to embed data : {random_int}"
    embed_instance = Embeded()

    # Payload ของข้อมูลที่จะส่ง
    payload = {
        "collection_name": "example_collection1",
        "id": str(uuid.uuid4()),
        "randomint": random_int,
        "embedding": embed_instance.embeded_text_by_lm(text_data), 
        "text": text_data
    }

    # ส่งคำขอ POST ไปยัง API
    try:
        response = requests.post(api_url, json=payload, timeout=15)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # ตรวจสอบสถานะของคำขอ
        if response.status_code == 200:
            print(f"Insert successful time: {processing_time}s, response: {response.json()}")
        else:
            print(f"Failed to insert status code: {response.status_code}, response text : {response.text}") # pylint: disable=C0301:line-too-long
    except Exception as e:  # pylint: disable=w0718
        print("Error occurred:", str(e))

if __name__ == "__main__":
    insert_record_by_data_frame()
    insert_record_by_list_dict()
