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
        backgroundColor: "#1d6b71",
        borderWidth: 0
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "#2f2b24"
        }
      },
      title: {
        display: true,
        text: "Image Histogram",
        color: "#9f3f07",
        font: {
          size: 18
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#4a4740"
        },
        grid: {
          color: "rgba(31,29,25,0.12)"
        }
      },
      y: {
        ticks: {
          color: "#4a4740"
        },
        grid: {
          color: "rgba(31,29,25,0.12)"
        }
      }
    }
  };

  return (
    <div
      style={{
        width: "100%",
        marginTop: "18px",
        background: "#fff",
        padding: "20px",
        borderRadius: "14px",
        border: "1px solid #d3c8ae"
      }}
    >
      <Bar data={chartData} options={options} />
    </div>
  );
}

export default Histogram;