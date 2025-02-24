import React from "react";
import ChartDisplay from "@/components/chart-display";
import { fetchCharts } from "@/lib/data";

export default async function DashboardCanva() {
  const charts = await fetchCharts();
  const numCharts = charts.length;

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
          />
        </div>
      ))}
    </div>
  );
}
