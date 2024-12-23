"""
Search for data by embedding (vector) in Milvus using MilvusUtility.
"""

import random
from milvus_utility import MilvusUtility

def main():
    """
    Search for data by embedding (vector)
    """

    collection_name = "example_collection1"

    # สร้าง MilvusUtility instance
    milvus = MilvusUtility()

    # เปิดการเชื่อมต่อ
    milvus.open()

    # สร้างเวกเตอร์จำลองเพื่อใช้ค้นหา (ขนาดต้องตรงกับ schema)
    query_vector = [random.random() for _ in range(384)]

    # ค้นหาข้อมูลด้วย embedding
    results = milvus.search_by_embedding(
        collection_name=collection_name,
        query_vector=query_vector,
        top_k=5,
        metric_type="L2",  # ใช้ระยะทาง L2
        params={"nprobe": 10}  # พารามิเตอร์เพิ่มเติม
    )

    # แสดงผลลัพธ์
    if results and len(results) > 0:
        print(f"Found {len(results[0])} result(s) for the given embedding.")
        for hit in results[0]:  # Results[0] คือ Hits object
            print(f"ID: {hit.id}, Distance: {hit.distance}")
    else:
        print("No results found.")

    # ปิดการเชื่อมต่อ
    milvus.close()

if __name__ == "__main__":
    main()
