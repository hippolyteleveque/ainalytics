"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import ChartDisplay from "@/components/chart-display";
import Spinner from "./spinner";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type ChartData = {
  type: string;
  data: any;
};

export default function DataAnalysisChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [waitData, setWaitData] = useState<Boolean>(false);
  const [threadId, setThreadId] = useState<number | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setWaitData(true);
    try {
      const url = threadId
        ? `http://127.0.0.1:8000/agent/${threadId}`
        : "http://127.0.0.1:8000/agent";
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      // const response = await fetch("/api/analyze", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({ message: input }),
      // });
      if (!response.ok) {
        throw new Error("Failed to get response from the server");
      }

      const data = await response.json();
      const newMessage: Message = {
        role: "assistant",
        content: data.query,
      };
      setMessages((prev) => [...prev, newMessage]);
      setChartData(data);
      if (!threadId) setThreadId(data.id);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, there was an error processing your request.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setWaitData(false);
    }
  };

  return (
    <div className="flex w-full h-[800px]">
      <div className="w-1/2 flex flex-col mr-4">
        <ScrollArea className="flex-grow border rounded-md p-4 mb-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className="mb-2"
              style={{
                color: `hsl(${
                  message.role === "user" ? "var(--chart-2)" : "var(--chart-3)"
                })`,
              }}
            >
              <strong>
                {message.role === "user" ? "You: " : "Assistant: "}
              </strong>
              {message.content}
            </div>
          ))}
        </ScrollArea>
        <form onSubmit={handleSubmit} className="flex">
          <Input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a data analysis question..."
            className="flex-grow mr-2"
          />
          <Button type="submit">Send</Button>
        </form>
      </div>
      <div className="w-1/2 border rounded-md p-4">
        {waitData ? <Spinner /> : <ChartDisplay chartData={chartData} />}
      </div>
    </div>
  );
}
