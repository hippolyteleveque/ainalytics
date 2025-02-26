"use client";

import { getSession } from "next-auth/react";
import { useEffect, useState } from "react";

export default function ProtectedPage() {
  const [session, setSession] = useState(null);

  useEffect(() => {
    const fetchSession = async () => {
      const session = await getSession();
      if (!session) {
        window.location.href = "/api/auth/signin";
      } else {
        // @ts-expect-error Next Auth is pussy library
        setSession(session);
      }
    };

    fetchSession();
  }, []);

  if (!session) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Protected Page</h1>
      {/* @ts-expect-error Next Auth is pussy library  */}
      <p>Welcome, {session.user.email}! </p>
    </div>
  );
}
