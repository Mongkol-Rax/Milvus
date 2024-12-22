"""
Delete a collection in Milvus using MilvusUtility.
"""

from milvus_utility import MilvusUtility


def main():
    """
    Delete a collection in Milvus by name.
    """

    # Define Collection Name
    collection_name = "example_collection1"

    # Define the milvus as MilvusUtility()
    milvus = MilvusUtility()

    # Open connection
    milvus.open()

    # Call function for delete collection
    milvus.delete_collection(collection_name)

    # Close connection
    milvus.close()


if __name__ == "__main__":
    main()
