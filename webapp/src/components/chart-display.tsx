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

type ChartData = {
  type: string;
  data: any;
};

type ChartDisplayProps = {
  chartData: ChartData | null;
};

export default function ChartDisplay({ chartData }: ChartDisplayProps) {
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
          <BarChart data={data} width={500} height={300}>
            <CartesianGrid vertical={false} />
            <XAxis dataKey="name" />
            <YAxis />
            <Bar dataKey="value" fill="hsl(var(--chart-3))" />
          </BarChart>
        );
      case "line":
        return (
          <LineChart data={data} width={500} height={300}>
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
          <PieChart width={500} height={300}>
            <Pie
              data={usedData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            />
            <ChartLegend
              content={<ChartLegendContent nameKey="name" />}
            />
          </PieChart>
        );
      default:
        return <div>Unsupported chart type</div>;
    }
  };
  const config: Record<string, { label: string; color: string }> = {};
  data.forEach((entry: any) => {
    config[entry.name] = { label: entry.name, color: entry.color };
  });

  return (
    <ChartContainer config={config} className="h-full w-full">
      {renderChart()}
    </ChartContainer>
  );
}
