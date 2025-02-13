# IoT Sensor Data Dashboard 

## 📌 Overview
This project is an IoT sensor data dashboard that visualizes temperature, humidity, and air quality data. It also detects anomalies in sensor readings.

## 🚀 Features
- 📊 Real-time visualization of sensor data (Vue.js + Chart.js)
- 🛠️ Backend API for data processing (FastAPI + SQLite)
- ⚠️ Anomaly detection using IQR (Interquartile Range)
- 📂 CSV Upload & Data Storage

## 🔧 Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/iot-sensor-dashboard.git
cd iot-sensor-dashboard



# Install Python dependencies
pip install -r backend/requirements.txt

# Install Vue dependencies
cd frontend
npm install


# Start the backend (FastAPI)
cd backend
uvicorn main:app --reload


# Start the frontend (Vue.js)
cd frontend
npm run dev


# API Endpoints
Method	Endpoint	Description
POST	/sensor/data	Upload raw sensor data
GET	/sensor/processed	Fetch cleaned & anomaly-detected data
GET	/sensor/aggregated	Fetch aggregated statistics




