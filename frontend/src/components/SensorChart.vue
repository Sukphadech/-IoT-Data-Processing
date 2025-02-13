<script setup lang="ts">
import { computed, ref, defineProps } from "vue";
import { Chart as ChartJS, registerables, Filler } from "chart.js";
import { Line } from "vue-chartjs";
import axios from "axios";

ChartJS.register(...registerables, Filler);

interface SensorData {
  timestamp: string;
  temperature: number;
  humidity: number;
  air_quality: number;
}

const formatTime = (timestamp: string): string => {
  if (!timestamp) return "N/A";
  return new Date(timestamp).toISOString().split("T")[1].split(".")[0]; // ได้รูปแบบ HH:mm:ss
};

const props = defineProps<{ sensorData: SensorData[] }>();

const chartData = computed(() => ({
  labels: props.sensorData.map((data) => formatTime(data.timestamp)),
  datasets: [
    {
      label: "Temperature (°C)",
      data: props.sensorData.map((data) => data.temperature),
      borderColor: "red",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      fill: true,
    },
    {
      label: "Humidity (%)",
      data: props.sensorData.map((data) => data.humidity),
      borderColor: "blue",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      fill: true,
    },
    {
      label: "Air Quality",
      data: props.sensorData.map((data) => data.air_quality),
      borderColor: "green",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      fill: true,
    },
  ],
}));

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
}));

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
  console.log("📢 Upload Button Clicked!");

  if (!selectedFile.value) {
    uploadMessage.value = "📂 กรุณาเลือกไฟล์ CSV ก่อน!";
    console.log("📢 Upload Message:", uploadMessage.value);
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  console.log("📤 FormData Content:", formData.get("file"));

  try {
    uploadMessage.value = "📤 กำลังอัปโหลด...";
    console.log("📢 Upload Message:", uploadMessage.value);
    
    const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    uploadMessage.value = `✅ อัปโหลดสำเร็จ! ${response.data.rows_inserted} แถวถูกบันทึก`;
    console.log("✅ Upload Success:", response.data);
  } catch (error: any) {
    uploadMessage.value = "❌ อัปโหลดล้มเหลว: " + error.message;
    console.error("❌ Upload Error:", error);
  }
};
</script>

/* import { defineProps, computed } from "vue";
import { Chart as ChartJS, registerables, Filler } from "chart.js";
import { Line } from "vue-chartjs";


// ลงทะเบียน Chart.js Modules รวมถึง Filler
ChartJS.register(...registerables, Filler);
//ChartJS.register(LineController, LineElement, PointElement, LinearScale, Title, Tooltip, Legend, Filler);

const formatTime = (timestamp) => {
  if (!timestamp) return "N/A";
  return new Date(timestamp).toISOString().split("T")[1].split(".")[0]; // ได้รูปแบบ HH:mm:ss
};


const props = defineProps(["sensorData"]);

const chartData = computed(() => ({
  labels: props.sensorData.map((data) => formatTime(data.timestamp)),

  
  datasets: [
    {
      label: "Temperature (°C)",
      data: props.sensorData.map((data) => data.temperature),
      borderColor: "red",
      backgroundColor: "rgba(255, 99, 132, 0.2)",
      fill: true,
    },
    {
      label: "Humidity (%)",
      data: props.sensorData.map((data) => data.humidity),
      borderColor: "blue",
      backgroundColor: "rgba(54, 162, 235, 0.2)",
      fill: true,
    },
    {
      label: "Air Quality",
      data: props.sensorData.map((data) => data.air_quality),
      borderColor: "green",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      fill: true,
    },
  ],
}));
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
};

const uploadFile = async () => {
  console.log("📢 Upload Button Clicked!"); 

  if (!selectedFile.value) {
    uploadMessage.value = "📂 กรุณาเลือกไฟล์ CSV ก่อน!";
    console.log("📢 Upload Message:", uploadMessage.value);
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  console.log("📤 FormData Content:", formData.get("file")); // ✅ ตรวจสอบไฟล์ที่ถูกส่ง

  try {
    uploadMessage.value = "📤 กำลังอัปโหลด...";
    console.log("📢 Upload Message:", uploadMessage.value);
    
    const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    uploadMessage.value = "✅ อัปโหลดสำเร็จ! " + response.data.rows_inserted + " แถวถูกบันทึก";
    console.log("✅ Upload Success:", response.data);
  } catch (error) {
    uploadMessage.value = "❌ อัปโหลดล้มเหลว: " + error.message;
    console.error("❌ Upload Error:", error);
  }
};*/


<template>
  <div>
    <h2>Sensor Data Trends</h2>
    <div v-if="chartData" style="height: 400px;">
      <Line :data="chartData" :options="chartOptions" />
      
    </div>
    <p v-else>📊 กำลังโหลดข้อมูลกราฟ...</p>
  </div>
</template>

<style>
h2 {
  color: #333;
  text-align: center;
  margin-bottom: 10px;
}
p {
  text-align: center;
  color: gray;
}
</style>
