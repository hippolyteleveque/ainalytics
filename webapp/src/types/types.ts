type ChartDataEntry = {
  name: string;
  value: number;
  color?: string;
};

type ChartData = {
  type: string;
  data: ChartDataEntry[];
  id?: number;
  query?: string;
};
