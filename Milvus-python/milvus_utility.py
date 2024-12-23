"""Milvus database utility"""

import os
from pymilvus import (
    connections,
    Collection,
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

    def create_collection(self, collection_name, schema, index):
        """
        สร้าง Collection ใหม่โดยรับ Schema โดยตรง

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการสร้าง
            schema (CollectionSchema): Schema ของ Collection ที่ต้องการสร้าง
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return

        if utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' already exists.")
            return

        try:
            collection = Collection(name=collection_name, schema=schema)

            # สร้าง Index
            if "field_name" in index and "index_params" in index:
                collection.create_index(
                    field_name=index["field_name"],
                    index_params=index["index_params"],
                    index_name=index["index_name"],
                )
                print(f"Index created successfully on field '{index['field_name']}'!")
            else:
                print("Index configuration is missing 'field_name' or 'index_params'.")

            print(f"Collection '{collection_name}' created successfully!")
        except Exception as e:  # pylint: disable=W0718
            print(f"Error creating collection: {e}")

    def delete_collection(self, collection_name):
        """
        ลบ Collection

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการลบ
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return

        # ตรวจสอบว่าคอลเล็กชันมีอยู่หรือไม่
        if utility.has_collection(collection_name):
            try:
                utility.drop_collection(collection_name)
                print(f"Collection '{collection_name}' deleted successfully.")
            except Exception as e:  # pylint: disable=W0718
                print(f"Error deleting collection '{collection_name}': {e}")
        else:
            print(f"Collection '{collection_name}' does not exist.")

    def insert_data(self, collection_name, data):
        """
        แทรกข้อมูลเข้าไปใน Collection

        Args:
            collection_name (str): ชื่อของ Collection ที่ต้องการแทรกข้อมูล
            data (list): ข้อมูลที่ต้องการแทรกในรูปแบบ list ของ record
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return

        # ตรวจสอบว่าคอลเล็กชันมีอยู่หรือไม่
        if not utility.has_collection(collection_name):
            print(f"Collection '{collection_name}' does not exist.")
            return

        try:
            collection = Collection(collection_name)  # เปิดคอลเล็กชัน
            result = collection.insert(data)  # แทรกข้อมูล
            collection.flush()  # บังคับบันทึกข้อมูลลง storage
            print(f"Data inserted into collection '{collection_name}' successfully.")
            return result
        except Exception as e:  # pylint: disable=W0718
            print(f"Error inserting data into collection '{collection_name}': {e}")
            return None

    def delete_data(self, collection_name, expr):
        """
        ลบข้อมูลในคอลเล็กชันตามเงื่อนไข

        Args:
            collection_name (str): ชื่อของคอลเล็กชัน
            expr (str): Expression ที่ใช้ลบข้อมูล เช่น "id in ['id1', 'id2']"
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return

        collection = Collection(collection_name)
        try:
            collection.delete(expr)
            print(f"Data deleted from collection '{collection_name}' where {expr}")
        except Exception as e:  # pylint: disable=W0718
            print(f"Error deleting data: {e}")

    def search_by_guid(self, collection_name, id_list):
        """
        ค้นหาข้อมูลในคอลเล็กชันด้วย GUID (Primary Key)

        Args:
            collection_name (str): ชื่อของคอลเล็กชัน
            id_list (list): รายการ GUID (String) ที่ต้องการค้นหา

        Returns:
            list: ข้อมูลที่ค้นพบในรูปแบบ list ของ dictionary
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return

        try:
            # โหลดคอลเล็กชัน
            collection = Collection(collection_name)

            # สร้าง Expression
            formatted_ids = ", ".join(
                f"'{guid}'" for guid in id_list
            )  # ใส่เครื่องหมายคำพูดรอบ GUID
            expr = f"id in [{formatted_ids}]"

            # ค้นหาข้อมูล
            results = collection.query(expr=expr, output_fields=["*"])

            print(f"Found {len(results)} record(s) matching the given GUID(s).")
            return results
        except Exception as e:  # pylint: disable=W0718
            print(f"Error searching by GUID: {e}")
            return []

    def search_by_int(self, collection_name, randomint_values):
        """
        ค้นหาข้อมูลในคอลเล็กชันด้วยค่า randomint

        Args:
            collection_name (str): ชื่อของคอลเล็กชัน
            randomint_values (list): รายการค่า randomint ที่ต้องการค้นหา

        Returns:
            list: ข้อมูลที่ค้นพบในรูปแบบ list ของ dictionary
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return []

        try:
            # โหลดคอลเล็กชัน
            collection = Collection(collection_name)

            # สร้าง Expression สำหรับค้นหา randomint
            expr = f"randomint in {randomint_values}"

            # ค้นหาข้อมูล
            results = collection.query(expr=expr, output_fields=["*"])

            print(
                f"Found {len(results)} record(s) matching the given randomint values."
            )
            return results
        except Exception as e:  # pylint: disable=W0718
            print(f"Error searching by randomint: {e}")
            return []

    def search_by_embedding(
        self,
        collection_name,
        query_vector,
        anns_field="embedding",
        top_k=5,
        metric_type="L2",
        params=None,
    ):
        """
        ค้นหาข้อมูลในคอลเล็กชันด้วย embedding (Vector Search)

        Args:
            collection_name (str): ชื่อของคอลเล็กชัน
            query_vector (list): เวกเตอร์ที่ต้องการใช้ในการค้นหา
            anns_field (str): ชื่อฟิลด์ที่เก็บเวกเตอร์ (ค่าเริ่มต้น: "embedding")
            top_k (int): จำนวนผลลัพธ์สูงสุดที่ต้องการ (ค่าเริ่มต้น: 5)
            metric_type (str): วิธีการวัดระยะห่าง (ค่าเริ่มต้น: "L2")
            params (dict): พารามิเตอร์เพิ่มเติมสำหรับการค้นหา (ค่าเริ่มต้น: None)

        Returns:
            list: ผลลัพธ์การค้นหาในรูปแบบ list
        """
        if not self.connected:
            print("Not connected to Milvus. Please call open() first.")
            return []

        try:
            # โหลดคอลเล็กชัน
            collection = Collection(collection_name)

            # กำหนดพารามิเตอร์สำหรับ Vector Search
            search_params = {
                "metric_type": metric_type,
                "params": params or {"nprobe": 10},
            }

            # ค้นหาเวกเตอร์
            results = collection.search(
                data=[query_vector],  # เวกเตอร์ที่ใช้ค้นหา
                anns_field=anns_field,  # ฟิลด์ที่เก็บเวกเตอร์
                param=search_params,  # พารามิเตอร์
                limit=top_k,  # จำนวนผลลัพธ์สูงสุด
                output_fields=["*"],  # ข้อมูลเพิ่มเติมที่ต้องการแสดง
            )

            return results
        except Exception as e:  # pylint: disable=W0718
            print(f"Error searching by embedding: {e}")
            return []
