import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const { question } = await request.json();

  // This is a mock response. Replace this with your actual backend logic.
  const mockResponse = {
    query: `SELECT * FROM Fake;`,
    type: "pie",
    data: [
      { name: "A", value: 10 },
      { name: "B", value: 20 },
      { name: "C", value: 15 },
      { name: "D", value: 25 },
    ],
  };

  return NextResponse.json(mockResponse);
}
