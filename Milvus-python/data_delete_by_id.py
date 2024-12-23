"""
Delete specific data from a collection in Milvus using MilvusUtility.
"""

from milvus_utility import MilvusUtility

def main():
    """
    Delete specific data by ID from a Milvus collection.
    """
    # ชื่อคอลเล็กชัน
    collection_name = "example_collection1"

    # สร้าง MilvusUtility instance
    milvus = MilvusUtility()

    # เปิดการเชื่อมต่อ
    milvus.open()

    # IDs ที่ต้องการลบ
    ids_to_delete = ["1e10ff1d-2912-41a4-bbbe-f17de185aa9f", "35ba6cb9-f278-4d90-9337-42e6b55febb8"]

    # Expression สำหรับการลบ
    expr = f"id in {ids_to_delete}"

    # เรียกฟังก์ชันลบข้อมูล
    milvus.delete_data(collection_name, expr)

    # ปิดการเชื่อมต่อ
    milvus.close()

if __name__ == "__main__":
    main()
