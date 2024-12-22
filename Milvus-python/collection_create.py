"""
Create a collection in Milvus using predefined schema.
"""

from pymilvus import DataType, FieldSchema, CollectionSchema
from milvus_utility import MilvusUtility


def main():
    """
    Create a new collection in Milvus using a schema.
    """

    # Define Collection Name
    collection_name = "example_collection1"

    # Define field properties
    field1 = FieldSchema(
        name="id",
        dtype=DataType.VARCHAR,     # ใช้ VARCHAR สำหรับ GUID
        is_primary=True,            # กำหนดให้เป็น Primary Key
        max_length=50,              # GUID
        description="Primary Key as GUID"
    )
    field2 = FieldSchema(
        name="randomint",
        dtype=DataType.INT64,
        description="For Random data 1-100"
    )
    field3 = FieldSchema(
        name="embedding",
        dtype=DataType.FLOAT_VECTOR,
        dim=384,
        description="Test as Vector"
    )
    field4 = FieldSchema(
        name="text",
        dtype=DataType.VARCHAR,
        max_length=2048,
        description="Real test not Vector"
    )
    # Define the schema : add field to schema, set description
    schema = CollectionSchema(fields=[field1, field2, field3, field4]
                              , description="Example collection for Milvus.")

    # Define the milvus as MilvusUtility()
    milvus = MilvusUtility()

    # Open connection
    milvus.open()
    # Call function for create collection
    milvus.create_collection(collection_name, schema)  # ใช้ schema ที่กำหนดไว้
    #Close connetion
    milvus.close()

if __name__ == "__main__":
    main()
