import DashboardCanva from "@/components/dashboard-canva";
import { getServerSession } from "next-auth";
import { authOptions } from "../api/auth/[...nextauth]/options";
import { AuthProvider } from "@/components/auth-provider";

export default async function Dashboard() {
  // @ts-expect-error Next Auth is pussy library
  const session = await getServerSession(authOptions);
  return (
    <main className="container p-4 mx-auto">
      <h1 className="text-2xl font-bold mb-4">Ainalytics</h1>
      <AuthProvider session={session}>
        <DashboardCanva />
      </AuthProvider>
    </main>
  );
}
