import NextAuth from "next-auth";
import { authOptions } from "./options";

// @ts-expect-error Next Auth is pussy library
const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
