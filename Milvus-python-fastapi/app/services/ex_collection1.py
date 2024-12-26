"""
Service API
"""

import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from app.utilitys.milvus_utility import MilvusUtility
from app.models.schemas import SearchByGuidRequest, SearchByRandomIntRequest, InsertRequest, SearchRequest # pylint: disable=C0301:line-too-long

COLLECTION_NAME = "example_collection1"

router = APIRouter()

# API Route สำหรับค้นหาโดย GUID
@router.post("/search/guid")
async def search_by_guid(request: SearchByGuidRequest):
    """
    ค้นหาข้อมูลใน Milvus ด้วย GUID (Primary Key)

    Args:
        request (SearchByGuidRequest): ข้อมูล input ที่ประกอบด้วย guid_list

    Returns:
        List[dict]: ผลลัพธ์ข้อมูลที่ตรงกับ GUID
    """
    milvus = MilvusUtility()
    try:
        # เปิดการเชื่อมต่อกับ Milvus
        milvus.open()

        # เรียก search_by_guid จาก MilvusUtility
        results = milvus.search_by_guid(COLLECTION_NAME, request.guid_list)

        if not results:
            return {"status": "not found", "message": "No records match the provided GUID(s)."}

        # ใช้ jsonable_encoder เพื่อแปลงค่า
        results_encode = jsonable_encoder(results)
        return {"status": "success", "results": results_encode}

    except HTTPException as e:
        # ใช้ e.status_code ได้โดยตรง
        raise HTTPException(status_code=e.status_code, detail=e.detail) # pylint: disable=raise-missing-from
    except Exception as e:
        # ข้อผิดพลาดทั่วไป
        raise HTTPException(status_code=getattr(e, "status_code", 509), detail=str(e)) from e
    finally:
        # ปิดการเชื่อมต่อกับ Milvus
        milvus.close()


# API Route RandomInt
@router.post("/search/randomint")
async def search_by_randomint(request: SearchByRandomIntRequest):
    """
    ค้นหาข้อมูลใน Milvus ด้วย RandomInt (Int)

    Args:
        request (SearchByRandomIntRequest): ข้อมูล input ที่ประกอบด้วย int_list

    Returns:
        List[dict]: ผลลัพธ์ข้อมูลที่ตรงกับ GUID
    """
    milvus = MilvusUtility()
    try:
        # เปิดการเชื่อมต่อกับ Milvus
        milvus.open()

        # เรียก search_by_guid จาก MilvusUtility
        results = milvus.search_by_int(COLLECTION_NAME, request.int_list)

        if not results:
            return {"status": "not found", "message": "No records match the provided int(s)."}

        # ใช้ jsonable_encoder เพื่อแปลงค่า
        results_encode = jsonable_encoder(results)
        return {"status": "success", "results": results_encode}

    except HTTPException as e:
        # ใช้ e.status_code ได้โดยตรง
        raise HTTPException(status_code=e.status_code, detail=e.detail) # pylint: disable=raise-missing-from
    except Exception as e:
        # ข้อผิดพลาดทั่วไป
        raise HTTPException(status_code=500, detail=str(e)) # pylint: disable=raise-missing-from
    finally:
        # ปิดการเชื่อมต่อกับ Milvus
        milvus.close()

@router.post("/search/embedding")
async def search_by_embedding(request: SearchRequest):
    """
    ค้นหาข้อมูลใน Milvus ด้วย Embedding Vector
    """
    milvus = MilvusUtility()

    try:
        # เปิดการเชื่อมต่อ
        milvus.open()

        # ค้นหาด้วย Embedding
        results = milvus.search_by_embedding(
            collection_name=request.collection_name,
            query_vector=request.query_vector,
            anns_field=request.anns_field,
            top_k=request.top_k,
            metric_type=request.metric_type,
            params=request.params,
        )

        # print(results)

        if not results:
            raise HTTPException(status_code=404, detail="No results found.")

        # แปลงผลลัพธ์เป็น JSON
        formatted_results = [
            {
                "id": hit.id,
                "distance": hit.distance,
                # "fields": hit.entity  # ข้อมูลเพิ่มเติมในแต่ละผลลัพธ์
                "text": hit.text
            }
            for result in results
            for hit in result
        ]

        print(formatted_results)

        return {"status": "success", "results": formatted_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}") # pylint: disable=raise-missing-from
    finally:
        # ปิดการเชื่อมต่อกับ Milvus
        milvus.close()

@router.post("/insert/by_list_dict")
async def insert_data(request: InsertRequest):
    """
    เพิ่มข้อมูลใน Milvus โดยระบุ collection_name และข้อมูลของแต่ละคอลัมน์
    """
    milvus = MilvusUtility()
    try:
        # เปิดการเชื่อมต่อ
        milvus.open()

        # เตรียมข้อมูลในรูปแบบของ Milvus
        list_dict_data = [{
                "id": request.id,
                "randomint": request.randomint,
                "embedding": request.embedding,
                "text": request.text,
            }]

        # แทรกข้อมูลลงใน Collection
        result = milvus.insert_data(collection_name=request.collection_name, data=list_dict_data)

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to insert data into Milvus, Insert result is None"
            )

        return {
            "status": "success",
            "message": "Data inserted successfully.",
            "inserted_id": str(result.primary_keys),
        }
    except HTTPException as e:
        # ใช้ e.status_code ได้โดยตรง
        raise HTTPException(status_code=e.status_code, detail=e.detail) # pylint: disable=raise-missing-from
    except Exception as e:
        # ข้อผิดพลาดทั่วไป
        raise HTTPException(status_code=500, detail=str(e)) # pylint: disable=raise-missing-from
    finally:
        # ปิดการเชื่อมต่อกับ Milvus
        milvus.close()


@router.post("/insert/by_data_frame")
async def insert_data1(request: InsertRequest):
    """
    เพิ่มข้อมูลใน Milvus โดยระบุ collection_name และข้อมูลของแต่ละคอลัมน์
    """
    milvus = MilvusUtility()
    try:
        # เปิดการเชื่อมต่อ
        milvus.open()

        # pandas DataFrame
        data_frame = pd.DataFrame({
            "id": [request.id],
            "randomint": [request.randomint],
            "embedding": [request.embedding],
            "text": [request.text]
            })

        # แทรกข้อมูลลงใน Collection
        result = milvus.insert_data(request.collection_name, data_frame)

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to insert data into Milvus, Insert result is None"
            )

        return {
            "status": "success",
            "message": "Data inserted successfully.",
            "inserted_id": str(result.primary_keys),
        }
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) # pylint: disable=raise-missing-from
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # pylint: disable=raise-missing-from
    finally:
        milvus.close()
