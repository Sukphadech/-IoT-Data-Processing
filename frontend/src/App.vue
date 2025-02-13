<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import SensorChart from "./components/SensorChart.vue";

// ✅ กำหนดประเภทของข้อมูล
interface SensorData {
  timestamp: string;
  value: number;
}

interface AggregatedData {
  mean: number;
  median: number;
  std_dev: number;
}

const sensorData = ref<SensorData[]>([]);
const anomalies = ref<SensorData[]>([]);
const aggregatedData = ref<AggregatedData | null>(null);
const timeWindow = ref<string>("1h");
const isLoading = ref<boolean>(false);
const showAnomalies = ref<boolean>(false);

const fetchSensorData = async (): Promise<void> => {
  try {
    console.log("📡 Fetching processed data...");
    const response = await axios.get("http://127.0.0.1:8000/sensor/processed");
    sensorData.value = response.data.cleaned_data;
    anomalies.value = response.data.anomalies;
  } catch (error) {
    console.error("❌ Error fetching sensor data:", error);
  }
};

const fetchAggregatedData = async (): Promise<void> => {
  try {
    console.log("📡 Fetching Aggregated Data...");
    const response = await axios.get(`http://127.0.0.1:8000/sensor/aggregated/?time_window=${timeWindow.value}`);
    
    if (response.data) {
      aggregatedData.value = response.data.aggregated_data;
      console.log("✅ Aggregated Data Received:", aggregatedData.value);
    } else {
      console.error("⚠️ No data received");
    }
  } catch (error) {
    console.error("❌ Error fetching aggregated data:", error);
  }
};

const formatMetric = (metric: string): string => {
  const metricNames: Record<string, string> = {
    temperature: "🌡 อุณหภูมิ (°C)",
    humidity: "💧 ความชื้น (%)",
    air_quality: "🌫 คุณภาพอากาศ"
  };
  return metricNames[metric] || metric;
};

const uploadMessage = ref<string>("");
const selectedFile = ref<File | null>(null);

const handleFileChange = (event: Event): void => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0];
    console.log("📂 File Selected:", selectedFile.value.name);
  } else {
    console.log("❌ No file selected");
  }
};

const uploadFile = async (): Promise<void> => {
  if (!selectedFile.value) {
    uploadMessage.value = "📂 กรุณาเลือกไฟล์ CSV ก่อน!";
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    uploadMessage.value = "📤 กำลังอัปโหลด...";
    
    const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    if (response.data.rows_inserted !== undefined) {
      uploadMessage.value = `✅ อัปโหลดสำเร็จ! ${response.data.rows_inserted} แถวถูกบันทึก`;
    } else {
      uploadMessage.value = "✅ อัปโหลดสำเร็จ แต่ไม่พบจำนวนแถวที่ถูกบันทึก";
    }
  } catch (error: any) {
    uploadMessage.value = "❌ อัปโหลดล้มเหลว: " + error.message;
  }
};

onMounted(fetchSensorData);
/*
import { ref, onMounted } from "vue";
import axios from "axios";
import SensorChart from "./components/SensorChart.vue";

const sensorData = ref([]);   // ข้อมูลจาก /sensor/processed
const anomalies = ref([]);    // ข้อมูล anomaly
const aggregatedData = ref(null); // ข้อมูลจาก /sensor/aggregated
const timeWindow = ref("1h"); // ค่า default คือ 1 ชั่วโมง
const isLoading = ref(false);
const showAnomalies = ref(false); 

const fetchSensorData = async () => {
  try {
    console.log("📡 Fetching processed data...");
    const response = await axios.get("http://127.0.0.1:8000/sensor/processed");
    sensorData.value = response.data.cleaned_data;
    anomalies.value = response.data.anomalies;
  } catch (error) {
    console.error("❌ Error fetching sensor data:", error);
  }
};

const fetchAggregatedData = async () => {
  try {
    console.log("📡 Fetching Aggregated Data...");
    const response = await axios.get(`http://127.0.0.1:8000/sensor/aggregated/?time_window=${timeWindow.value}`);
    
    // ตรวจสอบโครงสร้างข้อมูล
    if (response.data) {
      aggregatedData.value = response.data.aggregated_data;
      console.log("✅ Aggregated Data Received:", aggregatedData.value);
    } else {
      console.error("⚠️ No data received");
    }
  } catch (error) {
    console.error("❌ Error fetching aggregated data:", error);
  }
};

const formatMetric = (metric) => {
  const metricNames = {
    temperature: "🌡 อุณหภูมิ (°C)",
    humidity: "💧 ความชื้น (%)",
    air_quality: "🌫 คุณภาพอากาศ"
  };
  return metricNames[metric] || metric;
};


const uploadMessage = ref("");
const selectedFile = ref(null);

const handleFileChange = (event) => {
  const file = event.target.files[0];  // รับไฟล์ที่เลือก
  if (file) {
    selectedFile.value = file;  /
    console.log("📂 File Selected:", selectedFile.value.name);  
  } else {
    console.log("❌ No file selected");
  }
};

const uploadFile = async () => {
  if (!selectedFile.value) {
    uploadMessage.value = "📂 กรุณาเลือกไฟล์ CSV ก่อน!";
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    uploadMessage.value = "📤 กำลังอัปโหลด...";
    
    const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },  // ✅ ต้องกำหนด Content-Type
    });

    if (response.data.rows_inserted !== undefined) {
      uploadMessage.value = `✅ อัปโหลดสำเร็จ! ${response.data.rows_inserted} แถวถูกบันทึก`;
    } else {
      uploadMessage.value = "✅ อัปโหลดสำเร็จ แต่ไม่พบจำนวนแถวที่ถูกบันทึก";
    }

  } catch (error) {
    uploadMessage.value = "❌ อัปโหลดล้มเหลว: " + error.message;
  }
};




onMounted(fetchSensorData); 
*/
</script>








<template>
  <div>
    <h1>📊 IoT Sensor Data</h1>

    <h2>📂 อัปโหลดไฟล์ CSV</h2>
    <input type="file" accept=".csv" @change="handleFileChange" />
    <div class="upload-container">
      <button @click="uploadFile">Upload</button>
      <p>{{ uploadMessage }}</p>
    </div>

    <!-- ✅ ส่วนที่ 1: ข้อมูล Sensor แบบตาราง + กราฟ -->
    <h2>🔹 Processing Data </h2>
    <SensorChart v-if="sensorData.length > 0" :sensorData="sensorData" />
    <p v-else>📡 กำลังโหลดข้อมูล...</p>
<div class="table-container">
    <table border="1">
      <tr>
        <!--th>ID</!--th-->
        <th>เวลา</th>
        <th>Temperature</th>
        <th>Humidity</th>
        <th>Air Quality</th>
      </tr>
      <tr v-for="sensor in sensorData" :key="sensor.id">
        <!--td>{{ sensor.id }}</+td-->
        <td>{{ new Date(sensor.timestamp).toLocaleTimeString() }}</td> <!-- ✅ แสดงเวลาอย่างเดียว -->
        <td>{{ sensor.temperature }}</td>
        <td>{{ sensor.humidity }}</td>
        <td>{{ sensor.air_quality }}</td>
      </tr>
    </table>
  </div>

  <!-- ✅ ปุ่มกดแสดง/ซ่อนข้อมูลผิดปกติ -->
  <button @click="showAnomalies = !showAnomalies">
      {{ showAnomalies ? "🔄 ซ่อนข้อมูลผิดปกติ" : "⚠️ แสดงข้อมูลผิดปกติ" }}
    </button>
<div class="table-container">
    <!-- ✅ ข้อมูลผิดปกติ (Anomalies) -->
    <h2 v-if="showAnomalies">⚠️ ข้อมูลผิดปกติ (Anomalies)</h2>
    <ul v-if="showAnomalies && anomalies.length > 0">
      <li v-for="anomaly in anomalies" :key="anomaly.id">
        🚨 ID: {{ anomaly.id }} - Temp: {{ anomaly.temperature }}°C - Humidity: {{ anomaly.humidity }}% - Air Quality: {{ anomaly.air_quality }}
      </li>
    </ul>
    <p v-if="showAnomalies && anomalies.length === 0">✅ ไม่มีข้อมูลผิดปกติ</p>
</div>



    <!-- ✅ ส่วนที่ 3: แสดงข้อมูล Aggregated Insights -->
    <h2>📈 Aggregated Data </h2>
    
    <label>เลือกช่วงเวลา:</label>
    <select v-model="timeWindow">
      <option value="10m">10 นาที</option>
      <option value="1h">1 ชั่วโมง</option>
      <option value="24h">24 ชั่วโมง</option>
    </select>
    
    <button @click="fetchAggregatedData" :disabled="isLoading">
      {{ isLoading ? "📡 กำลังโหลด..." : "📊 แสดงข้อมูล" }}
    </button>

    <div v-if="aggregatedData">
      <pre>{{ aggregatedData.aggregated_data }}</pre>
    </div>
    <p v-else>📡 กดปุ่มเพื่อแสดงข้อมูล</p>
    <div v-if="aggregatedData" class="aggregated-container">
      <h3>🕒 ช่วงเวลา: {{ timeWindow }}</h3>
      <div v-if="aggregatedData" class="aggregated-container">
        <div class="aggregated-cards">
            <div v-for="(values, metric) in aggregatedData" :key="metric" class="card">
              <h4>{{ formatMetric(metric) }}</h4>
              <p><strong>ค่าเฉลี่ย:</strong> {{ values.mean.toFixed(2) }}</p>
              <p><strong>ค่ามัธยฐาน:</strong> {{ values.median.toFixed(2) }}</p>
              <p><strong>ค่าน้อยสุด:</strong> {{ values.min.toFixed(2) }}</p>
              <p><strong>ค่ามากสุด:</strong> {{ values.max.toFixed(2) }}</p>
            </div>
        </div>
      </div>
    </div>

  </div>
  


</template>



<style>
/* ✅ ปรับให้กราฟเต็มจอ */
.container {
  max-width: 100%;
  width: 100%;
  margin: auto;
  padding: 20px;
}

.chart-container {
  width: 100%;
  height: 500px; /* ปรับความสูงให้เหมาะสม */
  display: flex;
  justify-content: center;
  align-items: center;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}

h1, h2 {
  color: #333;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
th, td {
  padding: 8px;
  border: 1px solid #ddd;
}
button {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
p {
  text-align: center;
  color: gray;
}

.upload-container {
  display: flex;
  align-items: center; /* จัดให้แนวเดียวกับปุ่ม */
  gap: 10px; /* ระยะห่างระหว่างปุ่มและข้อความ */
}

.upload-container p {
  margin: 0;
  font-weight: bold;
  color: rgb(12, 7, 2); /* สีข้อความ */
}

.table-container {
  max-height: 400px; /* ✅ ปรับความสูงของตาราง */
  overflow-y: auto; /* ✅ เปิดใช้งาน scroll เฉพาะแนวตั้ง */
  border: 1px solid #ddd; /* ✅ เพิ่มเส้นขอบ */
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #f4f4f4;
  position: sticky;
  top: 0; /* ✅ ทำให้ header คงที่ขณะเลื่อน */
  z-index: 2;
}

.aggregated-container {
  width: 90%;
  margin: 20px auto;
  text-align: center;
}

.aggregated-cards {
  display: flex;
  justify-content: flex-start; /* ให้การ์ดเรียงจากซ้ายไปขวา */
  align-items: stretch;
  gap: 20px;
  flex-wrap: nowrap; /* บังคับให้เป็นแนวนอน */
  overflow-x: auto; /* เพิ่มการเลื่อนแนวนอน ถ้ามีการ์ดเยอะเกิน */
  padding-bottom: 10px; /* กันการ์ดติดขอบล่าง */
}

.card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  width: 150;  /* กำหนดความกว้างของแต่ละการ์ด */
  text-align: left;
  flex: 0 0 auto; /* ป้องกันการ์ดบีบตัว */
}

.card h4 {
  text-align: center;
  color: #333;
}

.card p {
  margin: 5px 0;
  font-size: 14px;
}
</style>    


<!-- 


<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import SensorChart from "./components/SensorChart.vue";



const formatTime = (timestamp) => {
  if (!timestamp) return "N/A"; 
  const date = new Date(timestamp);  
  return date.toISOString().split("T")[1].split(".")[0]; // ✅ ได้เวลาแบบ HH:mm:ss
};



const sensorData = ref([]);
const anomalies = ref([]);

const uploadMessage = ref("");
const selectedFile = ref(null);

const handleFileChange = (event) => {
  const file = event.target.files[0];  // รับไฟล์ที่เลือก
  if (file) {
    selectedFile.value = file;  // ✅ อัปเดตค่า selectedFile
    console.log("📂 File Selected:", selectedFile.value.name);  // ✅ Debug ตรวจสอบไฟล์
  } else {
    console.log("❌ No file selected");
  }
};

const uploadFile = async () => {
  if (!selectedFile.value) {
    uploadMessage.value = "📂 กรุณาเลือกไฟล์ CSV ก่อน!";
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    uploadMessage.value = "📤 กำลังอัปโหลด...";
    
    const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },  // ✅ ต้องกำหนด Content-Type
    });

    if (response.data.rows_inserted !== undefined) {
      uploadMessage.value = `✅ อัปโหลดสำเร็จ! ${response.data.rows_inserted} แถวถูกบันทึก`;
    } else {
      uploadMessage.value = "✅ อัปโหลดสำเร็จ แต่ไม่พบจำนวนแถวที่ถูกบันทึก";
    }

  } catch (error) {
    uploadMessage.value = "❌ อัปโหลดล้มเหลว: " + error.message;
  }
};



const fetchSensorData = async () => {
  try {
    console.log("📡 Fetching data from API...");
    const response = await axios.get("http://127.0.0.1:8000/sensor/processed");
    console.log("✅ API Response:", response.data);
    sensorData.value = response.data.cleaned_data;
    anomalies.value = response.data.anomalies;
    console.log("🔍 Updated Sensor Data in Vue:", sensorData.value);
  } catch (error) {
    console.error("❌ Error fetching sensor data:", error);
  }
};





onMounted(fetchSensorData);

</script>


-->

<!--

<template>
  <div>
    <h1>IoT Data Processing </h1>


    <h2>📂 อัปโหลดไฟล์ CSV</h2>
    <input type="file" accept=".csv" @change="handleFileChange" />
    <button @click="uploadFile">Upload</button>
    <p>{{ uploadMessage }}</p>

    <SensorChart v-if="sensorData.length > 0" :sensorData="sensorData" />
    <p v-else>📊 กำลังโหลดข้อมูลกราฟ...</p>

    <h2>Cleaned Data</h2>
  <table border="1">
    <tr>
      <th>Time</th> 
      <th>Temperature</th>
      <th>Humidity</th>
      <th>Air Quality</th>
    </tr>
    <tr v-for="sensor in sensorData" :key="sensor.id">
      <td>{{ formatTime(sensor.timestamp) }}</td> 
      <td>{{ sensor.temperature }}</td>
      <td>{{ sensor.humidity }}</td>
      <td>{{ sensor.air_quality }}</td>
    </tr>
  </table>


    <h2>Anomalies</h2>
    <ul>
      <li v-for="(anomaly, index) in [...new Map(anomalies.map(item => [item.id, item])).values()]" :key="index">
        🚨 ID: {{ anomaly.id }} - Temperature: {{ anomaly.temperature }} - Humidity: {{ anomaly.humidity }} - Air Quality: {{ anomaly.air_quality }}
      </li>
    </ul>

  </div>
</template>  

-->


