"""
Test Call API Search Vector
"""

from datetime import datetime
import requests
from app.utilitys.embed_text import Embeded # pylint: disable=import-error,no-name-in-module

def search_embedding_api(   # pylint: disable= dangerous-default-value
    api_url: str,
    collection_name: str,
    query_vector: list,
    anns_field: str = "embedding",
    top_k: int = 5,
    metric_type: str = "L2",
    params: dict = {"nprobe": 10},
):
    """
    เรียก API เพื่อค้นหาข้อมูลด้วย embedding ใน Milvus

    Args:
        api_url (str): URL ของ API
        collection_name (str): ชื่อ Collection ใน Milvus
        query_vector (list): Embedding Vector ที่ต้องการค้นหา
        anns_field (str): ชื่อฟิลด์ที่เก็บ embedding (default: "embedding")
        top_k (int): จำนวนผลลัพธ์สูงสุดที่ต้องการ (default: 5)
        metric_type (str): วิธีวัดระยะทาง (default: "L2")
        params (dict): พารามิเตอร์เพิ่มเติม (default: {"nprobe": 10})

    Returns:
        dict: ผลลัพธ์จาก API
    """

    # เตรียม payload สำหรับคำขอ API
    payload = {
        "collection_name": collection_name,
        "query_vector": query_vector,
        "anns_field": anns_field,
        "top_k": top_k,
        "metric_type": metric_type,
        "params": params,
    }

    try:
        # ส่งคำขอ POST ไปยัง API
        response = requests.post(api_url, json=payload, timeout=30)

        # ตรวจสอบสถานะคำขอ
        if response.status_code == 200:
            return response.json()  # ส่งคืนผลลัพธ์จาก API
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:  # pylint: disable=w0718
        print(f"Error occurred: {str(e)}")
        return None

def main():
    """
    Main function
    """

    while True:
        # รับข้อความจากผู้ใช้
        text = input("Enter the text to search (or type 'exit' to quit): ").strip()

        # ตรวจสอบเงื่อนไขการออก
        if text.lower() == "exit":
            print("Exiting the program. Goodbye!")
            return

        if not text:
            print("No text entered. Please try again.")
            continue


        # Start capture time
        start_time = datetime.now()

        embed_instance = Embeded()

        # URL ของ API
        api_url = "http://127.0.0.1:8000/milvus/search/embedding"

        # ตัวอย่าง embedding vector สำหรับการค้นหา
        # text = "text to embed data : 3"
        query_vector = embed_instance.embeded_text_by_lm(text) # ขนาดต้องตรงกับ Collection schema

        # ชื่อ Collection
        collection_name = "example_collection1"

        # เรียกฟังก์ชันเพื่อค้นหา
        results = search_embedding_api(
            api_url=api_url,
            collection_name=collection_name,
            query_vector=query_vector,
            top_k=3,
            metric_type="L2",
            params={"nprobe": 10},
        )

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # แสดงผลลัพธ์
        if results:
            print(f"Search word: [{text}], search time {processing_time}s :")
            for result in results["results"]:
                print(f"ID: {result['id']}, Distance: {result['distance']}, Text: {result['text']}")

            print("")
        else:
            print("No results found or an error occurred.")

if __name__ == "__main__":
    main()
