import pandas as pd
import logging
from fastapi import FastAPI, Query,Depends, UploadFile, File
from datetime import datetime, timedelta 
from sqlalchemy.orm import Session
from database import SessionLocal, SensorData, engine
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO


# ✅ สร้างตารางในฐานข้อมูล (ถ้ายังไม่มี)
from database import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ ตั้งค่า Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ เปิดให้ Frontend ที่รันบน http://localhost:5173 เข้าถึง API ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Dependency สำหรับดึง database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/sensor/processed")
def get_cleaned_data(db: Session = Depends(get_db)):
    data = db.query(SensorData).all()
    if not data:
        return {"message": "No data available", "cleaned_data": [], "anomalies": []}

    df = pd.DataFrame([d.__dict__ for d in data])
    df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")
    df.drop_duplicates(inplace=True)

    df["timestamp"] = df["timestamp"].apply(lambda x: x.isoformat() + "Z" if isinstance(x, datetime) else None)

    anomalies = detect_anomalies_iqr(df)
    # ✅ กรอง anomalies ออกจาก cleaned_data
    anomaly_ids = {row["id"] for row in anomalies}
    cleaned_data = df[~df["id"].isin(anomaly_ids)]
    
    cleaned_data = cleaned_data.sort_values(by="timestamp", ascending=True)


    return {
        "cleaned_data": cleaned_data.to_dict(orient="records"),  # ✅ ใช้ to_dict(orient="records")
        "anomalies": anomalies
    }





# ✅ ฟังก์ชันตรวจจับ Anomalies โดยใช้ IQR (Interquartile Range)
def detect_anomalies_iqr(df):
    anomalies = []
    for col in ["temperature", "humidity", "air_quality"]:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        anomaly_rows = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        anomalies.extend(anomaly_rows.to_dict(orient="records"))
    
    return anomalies

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        df = pd.read_csv(StringIO(decoded))

        # ✅ ตรวจสอบคอลัมน์ในไฟล์ CSV
        expected_columns = {"timestamp", "temperature", "humidity", "air_quality"}
        if not expected_columns.issubset(df.columns):
            return {"error": "❌ ไฟล์ CSV ต้องมีคอลัมน์: timestamp, temperature, humidity, air_quality"}

        # ✅ แปลง timestamp ให้เป็น datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # ✅ กำจัดแถวที่มี timestamp เป็น NaT (ถ้าแปลงไม่สำเร็จ)
        df = df.dropna(subset=["timestamp"])

        # ✅ กำจัด NaN ในค่าอื่น ๆ
        df.fillna({"temperature": 0, "humidity": 0, "air_quality": 0}, inplace=True)

        # ✅ แปลงข้อมูลให้เป็น SensorData แล้วบันทึกลง Database
        data_to_insert = [
            SensorData(
                timestamp=row["timestamp"].to_pydatetime(),  # ✅ แปลงเป็น datetime
                temperature=row["temperature"],
                humidity=row["humidity"],
                air_quality=row["air_quality"],
            )
            for _, row in df.iterrows()
        ]
        db.add_all(data_to_insert)
        db.commit()
        rows_inserted = len(data_to_insert)

        return {"message": "✅ อัปโหลดสำเร็จ!", "rows_inserted": rows_inserted}

    except Exception as e:
        return {"error": f"❌ อัปโหลดล้มเหลว: {str(e)}"}
    


@app.get("/sensor/aggregated")
def get_aggregated_data(
    time_window: str = Query("1h", description="ช่วงเวลาที่ต้องการ: เช่น '10m', '1h', '24h'"),
    db: Session = Depends(get_db)
):
    print(f"📡 ได้รับ time_window: {time_window}")  # ✅ Debug

    unit = time_window[-1]
    value = int(time_window[:-1])
    if unit == "m":
        delta = timedelta(minutes=value)
    elif unit == "h":
        delta = timedelta(hours=value)
    elif unit == "d":
        delta = timedelta(days=value)
    else:
        print("❌ ค่าของ time_window ไม่ถูกต้อง!")
        return {"error": "❌ time_window ต้องเป็น 10m, 1h, 24h"}

    latest_time = db.query(SensorData.timestamp).order_by(SensorData.timestamp.desc()).first()
    if not latest_time:
        print("📭 ไม่มีข้อมูลใน Database")
        return {"message": "📭 ไม่มีข้อมูล"}

    start_time = latest_time[0] - delta
    print(f"📊 ค้นหาข้อมูลช่วง: {start_time} - {latest_time[0]}")

    data = db.query(SensorData).filter(SensorData.timestamp >= start_time).all()
    if not data:
        print("📭 ไม่มีข้อมูลในช่วงเวลานี้")
        return {"message": "📭 ไม่มีข้อมูลในช่วงเวลานี้"}

    df = pd.DataFrame([d.__dict__ for d in data])
    df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")

    aggregated = {
        "temperature": {
            "mean": df["temperature"].mean(),
            "median": df["temperature"].median(),
            "min": df["temperature"].min(),
            "max": df["temperature"].max()
        },
        "humidity": {
            "mean": df["humidity"].mean(),
            "median": df["humidity"].median(),
            "min": df["humidity"].min(),
            "max": df["humidity"].max()
        },
        "air_quality": {
            "mean": df["air_quality"].mean(),
            "median": df["air_quality"].median(),
            "min": df["air_quality"].min(),
            "max": df["air_quality"].max()
        }
    }

    print(f"✅ ค่าที่คำนวณได้: {aggregated}")  # ✅ Debug
    return {"time_window": time_window, "aggregated_data": aggregated}