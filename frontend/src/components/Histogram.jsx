import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Histogram({ data }) {

  if (!data) return null;

  const chartData = {
    labels: Array.from({ length: 256 }, (_, i) => i),
    datasets: [
      {
        label: "Pixel Intensity",
        data: data,
        backgroundColor: "#3b82f6",   // blue bars
        borderWidth: 0
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#e2e8f0"   // legend text color
        }
      },
      title: {
        display: true,
        text: "Image Histogram",
        color: "#60a5fa",
        font: {
          size: 18
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#cbd5f5"   // x-axis text
        },
        grid: {
          color: "rgba(255,255,255,0.1)"  // light grid
        }
      },
      y: {
        ticks: {
          color: "#cbd5f5"   // y-axis text
        },
        grid: {
          color: "rgba(255,255,255,0.1)"
        }
      }
    }
  };

  return (
    <div
      style={{
        width: "700px",
        background: "#020617",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0px 0px 15px rgba(59,130,246,0.4)"
      }}
    >
      <Bar data={chartData} options={options} />
    </div>
  );
}

export default Histogram;