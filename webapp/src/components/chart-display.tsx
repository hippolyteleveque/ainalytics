"use client";
import {
  Bar,
  BarChart,
  Line,
  LineChart,
  Pie,
  PieChart,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { Button } from "@/components/ui/button";
import { PinIcon, CheckIcon } from "lucide-react";
import { useState } from "react";

type ChartData = {
  type: string;
  data: any;
  id?: number;
  query?: string;
};

type ChartDisplayProps = {
  chartData: ChartData | null;
  pin: boolean;
  dimensions: { width: string; height: string };
};

export default function ChartDisplay({
  chartData,
  pin,
  dimensions,
}: ChartDisplayProps) {
  const [pinned, setPinned] = useState(false);
  const handlePinChart = async () => {
    setPinned(true);
    const url = "http://127.0.0.1:8000/charts";
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: chartData?.type, query: chartData?.query! }),
    });
    if (!response.ok) {
      throw new Error("Failed to get response from the server");
    }
  };

  if (!chartData) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        No chart data available
      </div>
    );
  }

  const { type, data } = chartData;

  const colors = [
    "hsl(var(--chart-1))",
    "hsl(var(--chart-2))",
    "hsl(var(--chart-3))",
    "hsl(var(--chart-4))",
    "hsl(var(--chart-5))",
  ];

  const usedData = data.map((entry: any, index: number) => ({
    ...entry,
    fill: colors[index % colors.length],
    label: entry.name,
  }));

  const renderChart = () => {
    switch (type) {
      case "bar":
        return (
          <BarChart
            data={data}
            width={dimensions.width}
            height={dimensions.height}
          >
            <CartesianGrid vertical={false} />
            <XAxis dataKey="name" />
            <YAxis />
            <Bar dataKey="value" fill="hsl(var(--chart-3))" />
          </BarChart>
        );
      case "line":
        return (
          <LineChart
            data={data}
            width={dimensions.width}
            height={dimensions.height}
          >
            <CartesianGrid vertical={false} />
            <XAxis dataKey="name" />
            <YAxis />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Line
              type="natural"
              dataKey="value"
              dot={true}
              stroke="hsl(var(--chart-3))"
              strokeWidth={3}
              fill="hsl(var(--chart-3))"
            />
          </LineChart>
        );
      case "pie":
        return (
          <PieChart width={dimensions.width} height={dimensions.height}>
            <Pie
              data={usedData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            />
            <ChartLegend content={<ChartLegendContent nameKey="name" />} />
          </PieChart>
        );
      default:
        return <div>Unsupported chart type</div>;
    }
  };

  const renderPin = () => (
    <Button
      className="absolute top-2 right-2 p-2"
      variant="outline"
      size="sm"
      onClick={handlePinChart}
    >
      {pinned ? (
        <CheckIcon className="h-4 w-4 text-green-500" />
      ) : (
        <PinIcon className="h-4 w-4" />
      )}
    </Button>
  );

  const config: Record<string, { label: string; color: string }> = {};
  data.forEach((entry: any) => {
    config[entry.name] = { label: entry.name, color: entry.color };
  });

  return (
    <div className="relative h-full w-full">
      <ChartContainer
        config={config}
        className="h-full w-full flex items-center justify-center"
      >
        {renderChart()}
      </ChartContainer>

      {pin && renderPin()}
    </div>
  );
}
