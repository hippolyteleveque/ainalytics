import DataAnalysisChat from "@/components/data-analysis-chat";
import { getServerSession } from "next-auth";
import { authOptions } from "../api/auth/[...nextauth]/options";
import { AuthProvider } from "@/components/auth-provider";

export default async function Canvas() {
  // @ts-expect-error Next Auth is pussy library
  const session = await getServerSession(authOptions);
  return (
    <main className="container p-4 mx-auto flex flex-col flex-grow">
      <h1 className="text-2xl font-bold mb-4">Ainalytics</h1>
      <div className="flex-grow">
        <AuthProvider session={session}>
          <DataAnalysisChat />
        </AuthProvider>
      </div>
    </main>
  );
}
