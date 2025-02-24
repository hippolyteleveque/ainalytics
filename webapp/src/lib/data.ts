type Chart = {
  id: number;
  data: any[];
  type: string;
};

export async function fetchCharts(): Promise<Chart[]> {
  const url = "http://127.0.0.1:8000/charts";
  const response = await fetch(url, {
    method: "GET",
  });
  const data = await response.json();
  return data.charts;
}
