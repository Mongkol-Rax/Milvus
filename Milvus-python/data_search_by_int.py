"""
Search for data by randomint in Milvus using MilvusUtility.
"""

from milvus_utility import MilvusUtility

def main():
    """
    Search for data by randomint in Milvus using MilvusUtility.
    """

    # ชื่อคอลเล็กชัน
    collection_name = "example_collection1"

    # สร้าง MilvusUtility instance
    milvus = MilvusUtility()

    # เปิดการเชื่อมต่อ
    milvus.open()

    # ค่า randomint ที่ต้องการค้นหา
    randomint_values = [72, 95, 6]

    # ค้นหาข้อมูล
    results = milvus.search_by_int(collection_name, randomint_values)

    # แสดงผลลัพธ์
    for record in results:
        print(record)

    # ปิดการเชื่อมต่อ
    milvus.close()

if __name__ == "__main__":
    main()
