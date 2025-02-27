"use client";
import { SessionProvider } from "next-auth/react";
import type { PropsWithChildren } from "react";

type Props = PropsWithChildren & {
  session?: any;
};

export const AuthProvider = ({ children, session }: Props) => {
  return <SessionProvider session={session}>{children}</SessionProvider>;
};
