import { getToken } from "next-auth/jwt";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });

  if (!token) {
    // Redirect to sign-in page if not authenticated
    return NextResponse.redirect(new URL("/api/auth/signin", request.url));
  }

  // Allow the request to continue if authenticated
  return NextResponse.next();
}

// Specify which routes should be protected
export const config = {
  matcher: ["/", "/canvas", "/dashboard"], // Add paths you want to protect
};
