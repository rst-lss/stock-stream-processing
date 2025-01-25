import { useEffect, useState, useRef } from "react";
import * as echarts from "echarts/core";
import { LineChart, CandlestickChart } from "echarts/charts";
import { TitleComponent, LegendComponent } from "echarts/components";
import { GridComponent } from "echarts/components";
import { DataZoomComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import logo from "./logo.svg";
import "./App.css";
import generateDataArray from "./generateData";

echarts.use([CandlestickChart, TitleComponent, GridComponent, DataZoomComponent, LegendComponent, CanvasRenderer]);
const upColor = "#ec0000";
const upBorderColor = "#8A0000";
const downColor = "#00da3c";
const downBorderColor = "#008F28";
function App() {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  useEffect(() => {
    const data = generateDataArray();
    // Each item: open，close，lowest，highest
    const generatedData = generateDataArray();
    let rawData = [];
    generatedData.map((item, i) => {
      rawData.push([item.open, item.close, item.low, item.high]);
    });
    console.log(JSON.stringify(generatedData, null, 2));
    console.log(echarts.init, "echarts");
    chartInstance.current = echarts.init(chartRef.current);
    const option = {
      title: {
        text: "Candlestick Chart Example",
      },
      tooltip: {
        trigger: "item", // Changed from 'axis' to 'item'
        axisPointer: {
          type: "cross", // Optional: allows for crosshair on hover
        },
        formatter: (params) => {
          console.log(params);
          const [item] = params;
          if (item) {
            // Ensure item exists
            return `Date: ${new Date(item.data[0]).toLocaleDateString()}<br/>
                        Open: ${item.data[1]}<br/>
                        Close: ${item.data[2]}<br/>
                        Low: ${item.data[3]}<br/>
                        High: ${item.data[4]}`;
          }
          return "";
        },
      },
      dataZoom: [
        {
          show: true,
          type: "slider",
          // top: "90%",
          start: 0,
          end: 100,
        },
      ],
      xAxis: {
        type: "time",
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        scale: true,
        splitArea: {
          show: true,
        },
      },
      series: [
        {
          name: "Candlestick",
          type: "candlestick",
          data: data,
          itemStyle: {
            color: "#00da3c",
            color0: "#ec0000",
            borderColor: "#00da3c",
            borderColor0: "#ec0000",
          },
        },
      ],
    };
    chartInstance.current.setOption(option);
    return () => {
      chartInstance.current.dispose();
    };
  }, []);
  const addData = (data) => {
    // dataExample = [...,[timestamp * 1000, open, close, low, high],...]
    chartInstance.current.setOption({
      series: [{ data: data }],
    });
  };
  useEffect(() => {}, []);
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <div style={{ height: "5vh", backgroundColor: "gray" }}>
        <button
          onClick={(e) => {
            addData(generateDataArray());
          }}
        >
          Change Data
        </button>
      </div>
      <div style={{ height: "95vh", width: "100vw", backgroundColor: "black" }} ref={chartRef}></div>
    </div>
  );
}

export default App;
