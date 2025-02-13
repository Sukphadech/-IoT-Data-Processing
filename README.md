# IoT Data Processing 📡

## 🌟 Features
- 📊 **Real-time visualization** of sensor data (Vue.js + Chart.js)
- ⚙️ **Backend API** for data processing (FastAPI + SQLite)
- ⚠️ **Anomaly detection** using IQR (Interquartile Range)
- 📂 **CSV Upload & Data Storage**

---

## 🛠️ ติดตั้งและใช้งาน  

### 1️⃣ Clone โปรเจค  
```sh
git clone https://github.com/Sukphadech/-IoT-Data-Processing.git
cd IoT-Data-Processing




2️⃣ ติดตั้ง Backend (FastAPI)

cd backend
pip install -r requirements.txt  # ✅ ต้องติดตั้ง Python 3.8+ ก่อนใช้งาน


3️⃣ ติดตั้ง Frontend (Vue 3 + TypeScript)

cd ../frontend
npm install  # ✅ ต้องติดตั้ง Node.js 18+ ก่อนใช้งาน


4️⃣ รัน Backend Server

cd ../backend
uvicorn main:app --reload

📡 FastAPI จะรันที่: http://127.0.0.1:8000

5️⃣ รัน Frontend (Vue 3)

cd ../frontend
npm run dev

🖥️ Vue.js จะรันที่: http://localhost:5173/

🌐 API Endpoints

Method	Endpoint	Description
POST	/sensor/data	ส่งข้อมูลเซ็นเซอร์ (temperature, humidity, air quality)
GET	/sensor/processed	ดึงข้อมูลที่ทำความสะอาดแล้ว & anomaly detection
GET	/sensor/aggregated?time_window=10m	ดึงค่าสถิติ (Mean, Median, Min, Max)




🐳 ใช้งานผ่าน Docker (ถ้ามี)
1️⃣ Build & Run Docker Containers

docker-compose up --build

✅ ระบบจะรันทั้ง Backend (FastAPI) และ Frontend (Vue.js) อัตโนมัติ



✅ เสร็จเรียบร้อย!
🌍 เปิด http://localhost:5173/ 