import DataAnalysisChat from "@/components/data-analysis-chat";

export default function Home() {
  return (
    <main className="container p-4 mx-auto flex flex-col flex-grow">
      <h1 className="text-2xl font-bold mb-4">Ainalytics</h1>
      <div className="flex-grow">
        <DataAnalysisChat />
      </div>
    </main>
  );
}
