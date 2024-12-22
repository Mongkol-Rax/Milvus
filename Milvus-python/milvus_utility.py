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

    def create_collection(self, collection_name, schema):
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
            Collection(name=collection_name, schema=schema)
            print(f"Collection '{collection_name}' created successfully!")
        except Exception as e: # pylint: disable=W0718
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
