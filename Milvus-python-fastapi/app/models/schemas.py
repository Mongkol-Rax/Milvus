"""
Schemas of api
"""

from typing import List, Optional
from pydantic import BaseModel

class SearchByGuidRequest(BaseModel):
    """
    For schema input data list string (GUID)
    """

    guid_list: List[str]

class SearchByRandomIntRequest(BaseModel):
    """
    For schema input data list int
    """
    int_list: List[int]

class InsertRequest(BaseModel):
    """
    Insert data to Database
    """
    collection_name: str  # ชื่อของ Collection
    id: str               # GUID หรือ Primary Key
    randomint: int        # ค่าตัวเลขสุ่ม
    embedding: List[float]  # เวกเตอร์
    text: str             # ข้อความ

class SearchResponse(BaseModel):
    """
    For schema input data int
    """
    id: str
    randomint: int
    text: str
    distance: Optional[float] = None

class SearchRequest(BaseModel):
    """
    For schema input data embeded
    """
    collection_name: str
    query_vector: List[float]  # Embedding vector ที่จะใช้ค้นหา
    anns_field: str = "embedding"
    top_k: int = 5
    metric_type: str = "L2"
    params: dict = {"nprobe": 10}
