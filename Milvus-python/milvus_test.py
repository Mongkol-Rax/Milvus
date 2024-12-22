"""
Example usage of MilvusUtility class.
"""

from pymilvus import DataType
from milvus_utility import MilvusUtility


def main():
    """
    Main function to demonstrate the usage of MilvusUtility.
    """
    # Define the schema
    fields = [
        {
            "name": "id",
            "dtype": DataType.INT64,
            "is_primary": True,
            "description": "Primary Key",
        },
        {
            "name": "vector",
            "dtype": DataType.FLOAT_VECTOR,
            "description": "Feature Vector",
        },
    ]

    # Collection name
    collection_name = "example_collection"

    # Initialize MilvusUtility
    milvus = MilvusUtility()

    # Open connection
    milvus.open()

    # Create a collection
    milvus.create_collection(
        collection_name, fields, description="Example collection for Milvus."
    )

    # Insert data
    data = [
        [1, [0.1, 0.2, 0.3, 0.4]],
        [2, [0.2, 0.3, 0.4, 0.5]],
        [3, [0.3, 0.4, 0.5, 0.6]],
    ]
    milvus.insert_data(collection_name, data)

    # Search data
    query_vectors = [[0.1, 0.2, 0.3, 0.4]]
    anns_field = "vector"
    results = milvus.search_data(collection_name, query_vectors, anns_field, top_k=2)

    # Print search results
    print("Search Results:")
    for result in results:
        for hit in result:
            print(f"ID: {hit.id}, Distance: {hit.distance}")

    # Delete specific data
    milvus.delete_data(collection_name, "id in [1, 2]")

    # Drop the collection
    milvus.delete_collection(collection_name)

    # Close the connection
    milvus.close()


if __name__ == "__main__":
    main()
