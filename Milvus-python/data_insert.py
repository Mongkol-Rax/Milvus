"""
Insert data into a collection in Milvus using predefined schema.
"""

import random
import uuid
import pandas as pd
from milvus_utility import MilvusUtility

def generate_data(num_records=3, dim=384):
    """
    สร้างข้อมูลสำหรับเพิ่มในคอลเล็กชัน
    """
    data = []
    for i in range(num_records):
        record = [
            str(uuid.uuid4()),                              # id (GUID)
            random.randint(1, 100),                         # randomint (INT64)
            [random.random() for _ in range(dim)],          # embedding (FLOAT_VECTOR)
            f"Sample text {random.randint(300, 1000) + i}"  # text (VARCHAR)
        ]
        data.append(record)
    return data

def generate_data2(num_records=3, dim=384):
    """
    สร้างข้อมูลสำหรับเพิ่มในคอลเล็กชัน
    """
    data = []
    for i in range(num_records):
        record = [
            str(uuid.uuid4()),                              # id (GUID)
            random.randint(1, 100),                         # randomint (INT64)
            [random.random() for _ in range(dim)],          # embedding (FLOAT_VECTOR)
            f"Sample text {random.randint(300, 1000) + i}"  # text (VARCHAR)
        ]
        data.append(record)

    return (
        [item[0] for item in data],
        [item[1] for item in data],
        [item[2] for item in data],
        [item[3] for item in data]
    )

def main():
    """
    Main function for data insertion into Milvus.
    """

    # ชื่อคอลเล็กชัน
    collection_name = "example_collection1"

    # สร้าง MilvusUtility instance
    milvus = MilvusUtility()

    # เปิดการเชื่อมต่อ
    milvus.open()

    #Insert tuple (Error but message have recommend)
    milvus.insert_data(collection_name, generate_data2(num_records=5, dim=384))
    print("\r\n")

    # สร้างข้อมูล
    gen_data1 = generate_data(num_records=5, dim=384)

    #Fill to parameter by column
    ids = [item[0] for item in gen_data1]
    randomints = [item[1] for item in gen_data1]
    embeddings = [item[2] for item in gen_data1]
    texts = [item[3] for item in gen_data1]

    # List of List1
    list_data = [
        ids,
        randomints,
        embeddings,
        texts
    ]

    # Insert List of List -----
    result = milvus.insert_data(collection_name, list_data)

    # แสดงผลลัพธ์
    if result:
        print(f"Inserted List of List IDs: {result.primary_keys}\r\n")


    gen_data2 = generate_data2(num_records=5, dim=384)
    # list of dictionaries -----
    dict_data = [
        {
            "id": id_,
            "randomint": randomint,
            "embedding": embedding,
            "text": text
        }
        for id_, randomint, embedding, text in zip(
                gen_data2[0],
                gen_data2[1],
                gen_data2[2],
                gen_data2[3]
            )
    ]

    # Insert list of dictionaries
    result = milvus.insert_data(collection_name, dict_data)

    # แสดงผลลัพธ์
    if result:
        print(f"Inserted list of dictionaries IDs: {result.primary_keys}\r\n")


    gen_data3 = generate_data2(num_records=10, dim=384)

    # Data frame pandas -----
    data_frame = pd.DataFrame({
        "id": gen_data3[0],
        "randomint": gen_data3[1],
        "embedding": gen_data3[2],
        "text": gen_data3[3]
    })

    # Insert Data frame pandas
    result = milvus.insert_data(collection_name, data_frame)

    # แสดงผลลัพธ์
    if result:
        print(f"Inserted Data frame pandas IDs: {result.primary_keys}\r\n")


    # ปิดการเชื่อมต่อ
    milvus.close()


if __name__ == "__main__":
    main()
