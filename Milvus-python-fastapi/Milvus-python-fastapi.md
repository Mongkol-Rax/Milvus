# คู่มือการใช้งานระบบ Milvus API

## รายละเอียดไฟล์ในโปรเจกต์

### 1. `requirements.txt`
ไฟล์สำหรับจัดการ dependencies ที่จำเป็น:
- **pymilvus**: ใช้เชื่อมต่อและจัดการฐานข้อมูล Milvus
- **python-dotenv**: ใช้โหลดค่าตัวแปรจากไฟล์ `.env`

### 2. `schemas.py`
ประกอบด้วย Schema สำหรับการใช้งาน API โดยใช้ **Pydantic**:
- `InsertRequest`: Schema สำหรับการเพิ่มข้อมูล
- `SearchRequest`: Schema สำหรับการค้นหาด้วย Embedding Vector
- `SearchByGuidRequest`, `SearchByRandomIntRequest`: Schema สำหรับค้นหา GUID และ RandomInt

### 3. `embed_text.py`
โมดูลสำหรับสร้าง Embedding ของข้อความ:
- ใช้ `SentenceTransformer` สร้าง Vector จากข้อความ
- รองรับโมเดล เช่น `all-MiniLM-L6-v2`, `multi-qa-MiniLM-L6-cos-v1`

### 4. `.env`
เก็บค่าตั้งค่า:
- `MILVUS_HOST`: Host ของ Milvus (ค่าเริ่มต้น: `localhost`)
- `MILVUS_PORT`: Port ของ Milvus (ค่าเริ่มต้น: `19530`)

### 5. `milvus_utility.py`
คลาส Utility สำหรับจัดการ Milvus:
- ฟังก์ชันเปิด/ปิดการเชื่อมต่อ (`open`, `close`)
- การสร้าง/ลบ Collection (`create_collection`, `delete_collection`)
- การแทรกข้อมูล (`insert_data`)
- การค้นหาข้อมูลด้วย GUID, RandomInt, หรือ Embedding Vector

### 6. `ex_collection1.py`
Service API โดยใช้ **FastAPI**:
- `POST /search/guid`: ค้นหาข้อมูลด้วย GUID
- `POST /search/randomint`: ค้นหาข้อมูลด้วย RandomInt
- `POST /search/embedding`: ค้นหาด้วย Embedding Vector
- `POST /insert/by_list_dict`: เพิ่มข้อมูลจาก List of Dictionary
- `POST /insert/by_data_frame`: เพิ่มข้อมูลจาก DataFrame

### 7. `test_insert.py`
สคริปต์สำหรับทดสอบ API การเพิ่มข้อมูล:
- ทดสอบเพิ่มข้อมูลด้วย DataFrame หรือ List of Dictionary
- ใช้ **requests** ส่งคำขอ POST

### 8. `test_search_embed.py`
สคริปต์สำหรับทดสอบ API การค้นหาด้วย Embedding:
- ใช้ฟังก์ชัน `search_embedding_api` เพื่อค้นหาข้อมูล
- แสดงผลลัพธ์ที่ค้นพบพร้อมระยะทาง (distance)

### 9. `main.py`
ไฟล์เริ่มต้นของระบบ:
- รวม **FastAPI** Router สำหรับ API ของ Milvus
- Endpoint พื้นฐาน `GET /` ส่งข้อความต้อนรับ

---

## วิธีการติดตั้งและใช้งาน

1. **ติดตั้ง Dependencies**:
   ```bash
   pip install -r requirements.txt

2. **ตั้งค่าไฟล์ .env**
   ```bash
   MILVUS_HOST=localhost
   MILVUS_PORT=19530

3. **Run Server API**

   - Runserver
   ```bash
   uvicorn main:app --reload
   
   - API Documentation
   ```bash
   http://127.0.0.1:8000/docs

4. **เรียกใช้งาน API**

   ทดสอบเพิ่มข้อมูลด้วย test_insert.py , test_search_embed.py

   ```bash
   python -m tests.test_insert

   python -m tests.test_search_embed