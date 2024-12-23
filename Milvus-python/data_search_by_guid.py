"""
Search for data by ID in Milvus using MilvusUtility.
"""

from milvus_utility import MilvusUtility

def main():
    """
    ค้นหาข้อมูลในคอลเล็กชันด้วย GUID ในที่นี้ก็คือค้นหาด้วย varchar.
    """
    # ชื่อคอลเล็กชัน
    collection_name = "example_collection1"

    # สร้าง MilvusUtility instance
    milvus = MilvusUtility()

    # เปิดการเชื่อมต่อ
    milvus.open()

    # รายการ ID ที่ต้องการค้นหา
    # id_list = ["11e5337b-12b8-4fb7-b32a-6fcc8efd4450"]
    id_list = ["35c89831-ce87-48ae-aa8f-b867702d3a17"
               , "6bedf9c1-63d1-41a7-965a-555d893f8694"
               , "700cfdfb-2ddd-4b6f-ae97-c790b69dac2d"]

    # ค้นหาข้อมูลด้วย ID
    results = milvus.search_by_guid(collection_name, id_list)

    # แสดงผลลัพธ์
    for record in results:
        print(record)

    # ปิดการเชื่อมต่อ
    milvus.close()

if __name__ == "__main__":
    main()
