```markdown
# คู่มือการใช้งาน Milvus-Python เบื้องต้น

## คำอธิบาย
Milvus เป็นฐานข้อมูลที่ออกแบบมาเพื่อการค้นหาและจัดการข้อมูลแบบเวกเตอร์อย่างมีประสิทธิภาพ โดยใช้ Python เพื่อเชื่อมต่อและจัดการข้อมูลผ่าน `pymilvus` เราสามารถดำเนินการต่าง ๆ เช่น การแทรกข้อมูล การค้นหา การลบข้อมูล และการลบคอลเล็กชันได้อย่างง่ายดาย

## การติดตั้ง
สร้างไฟล์ `requirements.txt` และติดตั้งแพ็คเกจ:
```bash
pymilvus==2.5.0
python-dotenv>=1.0.1,<2.0.0
```

ติดตั้งแพ็คเกจ:
```bash
pip install -r requirements.txt
```

## การตั้งค่า
กำหนดไฟล์ `.env` สำหรับการเชื่อมต่อ:
```env
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

## การใช้งานหลัก

### 1. การแทรกข้อมูล
ไฟล์: `data_insert.py`  
แทรกข้อมูลหลากหลายรูปแบบ เช่น List of Lists, List of Dictionaries, และ DataFrame:
```python
milvus.insert_data(collection_name, data)
```

### 2. การค้นหาข้อมูล
- **ค้นหาโดยเวกเตอร์ (Embedding):**  
  ไฟล์: `data_search_by_embed.py`  
  ใช้เวกเตอร์สุ่มในการค้นหา:
  ```python
  milvus.search_by_embedding(collection_name, query_vector, top_k=5)
  ```

- **ค้นหาโดย GUID:**  
  ไฟล์: `data_search_by_guid.py`  
  ค้นหาข้อมูลด้วย ID:
  ```python
  milvus.search_by_guid(collection_name, id_list)
  ```

- **ค้นหาโดยตัวเลข (RandomInt):**  
  ไฟล์: `data_search_by_int.py`  
  ค้นหาข้อมูลด้วยค่า RandomInt:
  ```python
  milvus.search_by_int(collection_name, randomint_values)
  ```

### 3. การลบข้อมูล
- **ลบข้อมูลในคอลเล็กชัน:**  
  ไฟล์: `data_delete_by_id.py`  
  ลบข้อมูลด้วยเงื่อนไข:
  ```python
  milvus.delete_data(collection_name, expr)
  ```

- **ลบคอลเล็กชัน:**  
  ไฟล์: `collection_delete.py`  
  ลบคอลเล็กชันทั้งหมด:
  ```python
  milvus.delete_collection(collection_name)
  ```

### 4. Utility Class
ไฟล์: `milvus_utility.py`  
จัดการการเชื่อมต่อและการดำเนินการต่าง ๆ:
- เปิดการเชื่อมต่อ:
  ```python
  milvus.open()
  ```
- ปิดการเชื่อมต่อ:
  ```python
  milvus.close()
  ```

## ตัวอย่างโครงสร้างข้อมูล
- GUID (VARCHAR)
- RandomInt (INT64)
- Embedding (FLOAT_VECTOR)
- Text (VARCHAR)

## หมายเหตุ
อ่านโค้ดในไฟล์ที่แนบเพื่อศึกษาเพิ่มเติมเกี่ยวกับวิธีการปรับแต่งตามความต้องการของคุณ
```