"""Milvus database utility"""

import os
from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    utility,
)
from dotenv import load_dotenv


class MilvusUtility:
    """
    Utility class สำหรับจัดการ Milvus Database
    """

    def __init__(self):
        # โหลดค่าการตั้งค่าจาก .env
        load_dotenv()
        self.host = os.getenv("MILVUS_HOST", "localhost")
        self.port = os.getenv("MILVUS_PORT", "19530")
        self.connected = False

    def open(self):
        """เปิดการเชื่อมต่อกับ Milvus"""
        if not self.connected:
            connections.connect(alias="default", host=self.host, port=self.port)
            self.connected = True
            print(f"Connected to Milvus at {self.host}:{self.port}")

    def close(self):
        """ปิดการเชื่อมต่อ"""
        if self.connected:
            connections.disconnect(alias="default")
            self.connected = False
            print("Disconnected from Milvus")

    def create_collection(self, collection_name, schema_fields, description=None):
        """
        สร้าง Collection ใหม่

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการสร้าง
            schema_fields (list): รายการของ schema field แต่ละอันต้องประกอบด้วย
                'name', 'dtype', และ option เช่น 'is_primary', 'description'
            description (str, optional): คำอธิบายสำหรับ Collection (ถ้าไม่มีจะใช้ค่าเริ่มต้น)
        """
        if utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' already exists.")
            return

        fields = [
            FieldSchema(
                name=f["name"],
                dtype=f["dtype"],
                is_primary=f.get("is_primary", False),
                description=f.get("description", ""),
            )
            for f in schema_fields
        ]
        schema = CollectionSchema(
            fields=fields,
            description=description or f"Collection for {collection_name}",
        )
        Collection(name=collection_name, schema=schema)
        print(f"Collection '{collection_name}' created successfully!")

    def delete_collection(self, collection_name):
        """
        ลบ Collection

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการลบ
        """
        if utility.has_collection(collection_name):
            Collection.drop(collection_name)
            print(f"Collection '{collection_name}' deleted successfully.")
        else:
            print(f"Collection '{collection_name}' does not exist.")

    def insert_data(self, collection_name, data):
        """
        แทรกข้อมูลเข้าไปใน Collection

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการแทรกข้อมูล
            data (list): ข้อมูลที่ต้องการแทรกในรูปแบบ list ของ record
        """
        if not utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' does not exist.")
            return
        collection = Collection(collection_name)
        collection.insert(data)
        print("Data inserted successfully!")

    def delete_data(self, collection_name, expr):
        """
        ลบข้อมูลจาก Collection โดยใช้ Expression

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการลบข้อมูล
            expr (str): เงื่อนไข (expression) ที่ใช้ระบุข้อมูลที่จะลบ เช่น "id in [1, 2, 3]"
        """
        if not utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' does not exist.")
            return
        collection = Collection(collection_name)
        collection.delete(expr)
        print(f"Data deleted from '{collection_name}' where {expr}")

    def search_data(
        self,
        collection_name,
        query_vectors,
        anns_field,
        top_k=5,
        metric_type="L2",
        params=None,
    ):
        """
        ค้นหาข้อมูลใน Collection

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการค้นหา
            query_vectors (list): เวกเตอร์ที่ใช้ในการค้นหา
            anns_field (str): ชื่อฟิลด์ใน Collection ที่เก็บเวกเตอร์
            top_k (int, optional): จำนวนผลลัพธ์สูงสุดที่ต้องการ (ค่าเริ่มต้นคือ 5)
            metric_type (str, optional):
                วิธีการวัดระยะห่างของเวกเตอร์ เช่น "L2" หรือ "IP" (ค่าเริ่มต้นคือ "L2")
            params (dict, optional):
                พารามิเตอร์เพิ่มเติมสำหรับการค้นหา เช่น {"nprobe": 10} (ค่าเริ่มต้นคือ None)

        Returns:
            list: ผลลัพธ์การค้นหาในรูปแบบ list
        """
        if not utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' does not exist.")
            return []

        collection = Collection(collection_name)
        search_params = {"metric_type": metric_type, "params": params or {"nprobe": 10}}
        results = collection.search(
            data=query_vectors, anns_field=anns_field, param=search_params, limit=top_k
        )
        print(f"Search results: {len(results)} items found.")
        return results
