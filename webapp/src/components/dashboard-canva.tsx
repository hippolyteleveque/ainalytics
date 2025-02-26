"use client";
import React, { useEffect, useState } from "react";
import ChartDisplay from "@/components/chart-display";

type ChartDataEntry = {
  name: string;
  value: number;
  color?: string;
};

type Chart = {
  id: number;
  data: ChartDataEntry[];
  type: string;
};

export default function DashboardCanva() {
  const [charts, setCharts] = useState<Chart[]>([]);
  const numCharts = charts.length;

  useEffect(() => {
    const fetchCarts = async () => {
      const url = "http://127.0.0.1:8000/charts";
      const response = await fetch(url, {
        method: "GET",
      });
      const data = await response.json();
      setCharts(data.charts);
    };

    fetchCarts();
  }, []);

  // Calculate dimensions based on the number of charts
  const getChartDimensions = () => {
    if (numCharts <= 2) {
      return { width: "100%", height: "50%" };
    } else if (numCharts <= 4) {
      return { width: "50%", height: "50%" };
    } else {
      return { width: "33.33%", height: "33.33%" };
    }
  };

  const removeChart = async (id: number) => {
    const url = `http://127.0.0.1:8000/charts/${id}`;
    // TODO handle error
    await fetch(url, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
    setCharts((prev) => prev.filter((chart) => chart.id != id));
  };

  const chartDimensions = getChartDimensions();

  return (
    <div className="w-full rounded-md p-4 flex flex-wrap">
      {charts.map((chartData) => (
        <div
          key={chartData.id}
          style={{
            width: chartDimensions.width,
            height: chartDimensions.height,
          }}
          className="p-2 box-border"
        >
          <ChartDisplay
            chartData={chartData}
            pin={false}
            dimensions={chartDimensions}
            onRemoveChart={() => removeChart(chartData.id)}
          />
        </div>
      ))}
    </div>
  );
}
