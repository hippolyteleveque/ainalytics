const API_URL = process.env.API_URL;

export async function fetchCharts(): Promise<ChartData[]> {
  const url = `${API_URL}/charts`;
  const response = await fetch(url, {
    method: "GET",
  });
  const data = await response.json();
  return data.charts;
}

// export async function postChart(token: string) {
//   const url = `${API_URL}/charts`;
//   const response = await fetch(url, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       Authorization: `Bearer ${token}`,
//     },
//   });
//   const data = await response.json();
//   return data.charts;
// }
