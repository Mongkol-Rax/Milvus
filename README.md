# Milvus Database
Learn Database Milvus

# 1. Introduction to Milvus

## 1.1 What is Milvus?
**Milvus** เป็นฐานข้อมูลแบบ **Open-Source** สำหรับการจัดการข้อมูลเวกเตอร์  
- ถูกออกแบบมาเพื่อรองรับการค้นหาที่ซับซ้อน เช่น การค้นหาภาพ, วิดีโอ, และข้อความ  
- เหมาะสำหรับงานที่เกี่ยวข้องกับ AI และ Machine Learning เช่น  
   - **Recommendation System**  
   - **Search Engine**  
   - **Data Mining**

## 1.2 Why Use Milvus?
- **ประสิทธิภาพสูง:** รองรับการจัดการข้อมูลเวกเตอร์ขนาดใหญ่  
- **การค้นหาที่แม่นยำ:** รองรับการค้นหา **Approximate Nearest Neighbor (ANN)**  
- **รองรับการขยายระบบ (Scalability):** ใช้ได้ทั้งแบบ **Standalone** และ **Cluster**  

---

# 2. Key Features of Milvus

## 2.1 Data Storage
- รองรับการจัดการข้อมูลเวกเตอร์แบบโครงสร้าง  
- รองรับการจัดเก็บข้อมูลแบบไบนารีและเวกเตอร์เชิงตัวเลข  

## 2.2 Indexing Options
- **IVF_FLAT:** เหมาะสำหรับข้อมูลขนาดเล็กถึงกลาง  
- **IVF_SQ8:** ลดขนาดเวกเตอร์เพื่อประหยัดหน่วยความจำ  
- **HNSW:** เหมาะสำหรับงานที่ต้องการความแม่นยำสูงและเวลาในการค้นหาสั้น  

## 2.3 Real-Time Processing
- รองรับการอัปเดตข้อมูลเวกเตอร์และ Query แบบเรียลไทม์  

## 2.4 Distributed System
- รองรับการกระจายข้อมูลและสามารถขยายขนาดระบบได้อย่างมีประสิทธิภาพ  

---

# 3. Architecture Overview

## 3.1 Key Components
- **ETCD:** จัดการ Configuration และ Cluster Metadata  
- **MinIO:** จัดเก็บข้อมูลแบบ Object Storage  
- **Milvus Standalone/Cluster:** ประมวลผลและจัดการข้อมูลเวกเตอร์
- **Attu:** เป็น IDE จัดการแบบง่านในรูปบบ web application  

## 3.2 System Workflow
1. **การรับข้อมูลเวกเตอร์**  
2. **จัดเก็บใน MinIO**  
3. **สร้างดัชนีใน Milvus**  
4. **Query และค้นหาข้อมูล**

---

# 4. Installation and Configuration

## 4.1 Installation Using Docker Compose

สำหรับการติดตั้ง **Milvus** อย่างรวดเร็ว สามารถใช้ **Docker Compose** โดยมีบริการหลักที่เกี่ยวข้องดังนี้:

### **ไฟล์ `docker-compose.yml` ประกอบด้วย:**

1. **ETCD**  
   - ดูแล Metadata ของระบบ  

2. **MinIO**  
   - จัดเก็บไฟล์ข้อมูลแบบ **Object Storage**  

3. **Milvus Standalone**  
   - บริหารจัดการและประมวลผลข้อมูลเวกเตอร์  

4. **Attu**  
   - Web UI สำหรับการจัดการและตรวจสอบข้อมูลใน Milvus  

---
